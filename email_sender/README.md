# Email Sender Application

This is a small example script that demonstrates how you can send your
application documents to companies via Gmail. The script uses the
OpenAI API to help generate email text and then sends the email using
Gmail's SMTP server.

## Requirements

- Python 3.8+
- `openai` Python package

Optional dependencies:
- `python-dotenv` for loading environment variables from a `.env` file

Install them with:

```bash
pip install openai python-dotenv
```

## Configuration

Set the following environment variables before running the script:

- `OPENAI_API_KEY` – your OpenAI API key for generating text.
- `GMAIL_USER` – your Gmail address used to send the emails.
- `GMAIL_APP_PASSWORD` – an App Password generated in your Google account. Gmail
  requires an App Password when using SMTP with two-factor authentication.

Create a `companies.json` file in the same directory with an array of
objects containing company information. Example:

```json
[
    {"name": "Musterfirma", "email": "kontakt@musterfirma.de", "field": "IT", "location": "Berlin"},
    {"name": "Beispiel AG", "email": "jobs@beispiel.de", "field": "Buchhaltung", "location": "Hamburg"}
]
```

Place your résumé or other documents in this folder and update the
`ATTACHMENTS` list in `application_sender.py` accordingly.

## Running

```bash
python application_sender.py
```

The script generates a custom email for each company using the OpenAI
API and sends it through Gmail with your attachments.
