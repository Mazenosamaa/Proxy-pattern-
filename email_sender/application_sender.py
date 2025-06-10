import json
import os
import smtplib
import mimetypes
from email.message import EmailMessage

import openai
from typing import List

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

ATTACHMENTS = [
    "resume.pdf",  # replace with the path to your résumé
]


def load_companies(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_email(company: dict) -> str:
    """Use OpenAI to create a German email for the given company."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")

    openai.api_key = OPENAI_API_KEY
    field = company.get("field", "")
    location = company.get("location", "")
    name = company.get("name", "")
    prompt = (
        "Formuliere eine professionelle Bewerbungsemail auf Deutsch, in der nach"
        f" einer Ausbildungsstelle im Bereich {field} in {location} gefragt wird."
        f" Das Unternehmen heißt {name}. Bitte sei höflich und fasse dich kurz."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()


def create_message(to_addr: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = "Bewerbung um einen Ausbildungsplatz"
    msg.set_content(body)

    for path in ATTACHMENTS:
        if not os.path.isfile(path):
            continue
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(path, "rb") as fp:
            msg.add_attachment(
                fp.read(),
                maintype=maintype,
                subtype=subtype,
                filename=os.path.basename(path),
            )
    return msg


def send_message(message: EmailMessage):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise RuntimeError("GMAIL_USER or GMAIL_APP_PASSWORD not set")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(message)


def main():
    companies = load_companies("companies.json")
    for company in companies:
        email_body = generate_email(company)
        msg = create_message(company["email"], email_body)
        send_message(msg)
        print(f"Sent application to {company['name']}")


if __name__ == "__main__":
    main()
