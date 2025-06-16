import json
import os
import uuid
from logger import logger
from threading import Thread
from Engine.Files.write_supabase_file import write_supabase_file

def background_task(run_id: str):
    filename = f"{run_id}.txt"
    supabase_path = f"Predictive_Report/Ai_Responses/Change_Effect_Maths/{filename}"
    write_supabase_file(supabase_path, "TEST FILE")

def run_prompt(data):
    run_id = str(uuid.uuid4())
    Thread(target=background_task, args=(run_id,)).start()
    return {"run_id": run_id}
