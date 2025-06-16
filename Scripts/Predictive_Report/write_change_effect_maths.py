import json
import os
import uuid
from threading import Thread
from logger import logger
from Engine.Files.write_supabase_file import write_supabase_file

def background_task(run_id: str, subdirectory: str):
    filename = f"{run_id}.txt"
    content = "TEST FILE"
    write_supabase_file(subdirectory, filename, content)

def run_prompt(data):
    # Generate UUID for filename and response
    run_id = str(uuid.uuid4())
    filename = f"{run_id}.txt"

    # Always write to correct target directory
    subdirectory = "Predictive_Report/Ai_Responses/Change_Effect_Maths"

    # Run background write
    Thread(target=background_task, args=(run_id, subdirectory)).start()

    # Return UUID to Zapier immediately
    return { "run_id": run_id }
