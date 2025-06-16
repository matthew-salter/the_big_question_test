import os
import json
import uuid
from Engine.Files.write_supabase_file import write_supabase_file
from datetime import datetime
from threading import Thread

def background_task(prompt_payload, filename, subdirectory):
    content = "TEST FILE"
    write_supabase_file(subdirectory, filename, content)

def run_prompt(data):
    # Generate UUID for this run
    run_id = str(uuid.uuid4())

    # Extract payload info
    prompt_payload = data.get("prompt", "")
    filename = data.get("filename", f"{run_id}.txt")
    subdirectory = data.get("subdirectory", "Predictive_Report/Ai_Responses/Change_Effect_Maths")

    # Trigger Supabase write in background
    Thread(target=background_task, args=(prompt_payload, filename, subdirectory)).start()

    # Return UUID immediately to Zapier
    return {"run_id": run_id}
