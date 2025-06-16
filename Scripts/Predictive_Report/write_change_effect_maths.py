import json
import os
import uuid
from logger import logger
from threading import Thread
from Engine.Files.write_supabase_file import write_supabase_file

def background_task(run_id: str):
    # Manual pathing logic — exact match to working version
    supabase_root = os.getenv("SUPABASE_ROOT_FOLDER")
    sub_path = "Predictive_Report/Ai_Responses/Change_Effect_Maths"
    full_path = f"{supabase_root}/{sub_path}"
    filename = f"{run_id}.txt"
    file_content = "TEST FILE"

    # Pass manually composed path and file content
    write_supabase_file(full_path, filename, file_content)

def run_prompt(data):
    run_id = str(uuid.uuid4())

    # Spawn background thread with correct run_id
    Thread(target=background_task, args=(run_id,)).start()

    # Return UUID to Zapier immediately
    return {"run_id": run_id}
