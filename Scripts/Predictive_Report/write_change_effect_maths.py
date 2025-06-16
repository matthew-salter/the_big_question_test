import uuid
import json
from logger import logger
from datetime import datetime
from Engine.Files.write_supabase_file import write_supabase_file

def run_prompt(data):
    # Pull data from Zapier webhook payload
    payload_str = data.get("prompt", "TEST FILE")  # fallback to test text if none
    filename = data.get("filename", f"change_effect_test_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.txt")
    subdirectory = data.get("subdirectory", "The_Big_Question/Predictive_Report/Ai_Responses/Change_Effect_Maths")

    # Write file to Supabase using your existing util
    success = write_supabase_file(subdirectory, filename, payload_str)

    return {
        "status": "success" if success else "failed",
        "filename": filename,
        "path": f"{subdirectory}/{filename}",
    }
