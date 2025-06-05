import os
import requests
from datetime import datetime
from pathlib import Path
from logger import logger
from Engine.Files.write_supabase_file import write_supabase_file

# --- ENV VARS ---
client_field_id = os.getenv("CLIENT_FIELD_ID")
question_context_field_id = os.getenv("QUESTION_CONTEXT_FIELD_ID")
logo_field_id = os.getenv("LOGO_FIELD_ID")

# --- HELPERS ---
def download_file(url: str) -> bytes:
    """Downloads a file from a given URL and returns its binary content, with Typeform auth if needed."""
    headers = {}

    # Apply Bearer token auth for Typeform-hosted files
    if "api.typeform.com/responses/files" in url:
        typeform_token = os.getenv("TYPEFORM_TOKEN")
        if not typeform_token:
            raise EnvironmentError("TYPEFORM_TOKEN not set in environment variables")
        headers["Authorization"] = f"Bearer {typeform_token}"

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.content

# --- MAIN FUNCTION ---
def process_typeform_submission(data):
    """Extracts client, context, and logo file from Typeform and writes to Supabase."""
    try:
        answers = data.get("form_response", {}).get("answers", [])
        client = None
        question_context_url = None
        logo_url = None
        logo_ext = None

        for answer in answers:
            field_id = answer["field"]["id"]

            if field_id == client_field_id:
                client = answer["text"].strip().replace(" ", "_")

            elif field_id == question_context_field_id:
                question_context_url = answer["file_url"]

            elif field_id == logo_field_id:
                logo_url = answer["file_url"]
                logo_filename = logo_url.split("/")[-1]
                logo_ext = Path(logo_filename).suffix.lstrip(".")
                if not logo_ext:
                    raise ValueError(f"Could not determine file extension from logo_url: {logo_url}")

        # 🔍 Log what was parsed
        logger.info(f"🔎 Parsed Typeform fields:\n  client={client}\n  question_context_url={question_context_url}\n  logo_url={logo_url}\n  logo_ext={logo_ext}")

        # 🚨 Guard clause — stops if any field missing
        if not client or not question_context_url or not logo_url:
            raise ValueError("Missing required fields: client, question context file, or logo")

        # 📝 Format filenames and paths
        date_str = datetime.utcnow().strftime("%d-%m-%Y")
        question_context_path = f"Predictive_Report/Question_Context/{client}_question_context_{date_str}.txt"
        logo_path = f"Predictive_Report/Logos/{client}_Logo_{date_str}.{logo_ext}"

        logger.info(f"🧭 Final Supabase paths:\n  Context: {question_context_path}\n  Logo: {logo_path}")

        # 📥 Download and save the question context
        logger.info(f"📥 Downloading question context from: {question_context_url}")
        question_context_data = download_file(question_context_url)

        try:
            decoded_context = question_context_data.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"Failed to decode question context file as UTF-8: {e}")

        write_supabase_file(question_context_path, decoded_context)

        # 📥 Download and save the logo
        logger.info(f"📥 Downloading logo from: {logo_url}")
        logo_data = download_file(logo_url)
        write_supabase_file(logo_path, logo_data)

        logger.info("✅ Files written to Supabase successfully.")

    except Exception:
        logger.exception("❌ Failed to process Typeform submission and save files to Supabase.")
