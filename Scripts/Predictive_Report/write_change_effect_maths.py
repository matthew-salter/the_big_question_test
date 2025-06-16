import json
import os
import uuid
from threading import Thread
from logger import logger
from Engine.Files.write_supabase_file import write_supabase_file

def background_task(run_id: str):
    subdirectory = "Predictive_Report/Ai_Responses/Change_Effect_Maths"
    filename = f"{run_id}.txt"
    content = "TEST FILE"

    # Write "TEST FILE" to correct path using correct name
    write_supabase_file(subdirectory, filename, content)

def run_prompt(data):
    # Generate UUID
    run_id = str(uuid.uuid4())

    # Start background file write
    Thread(target=background_task, args=(run_id,)).start()

    # Return UUID immediately to Zapier
    return {"run_id": run_id}
