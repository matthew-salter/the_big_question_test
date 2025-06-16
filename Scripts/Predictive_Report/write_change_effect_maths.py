import json
import os
import uuid
from logger import logger
from threading import Thread
from Engine.Files.write_supabase_file import write_supabase_file

def background_task(run_id: str):
    supabase_root = os.getenv("SUPABASE_ROOT_FOLDER")
    relative_path = f"Predictive_Report/Ai_Responses/Change_Effect_Maths/{run_id}.txt"
    full_path = f"{supabase_root}/{relative_path}"
    content = "TEST FILE"

    # FINAL: write the full relative path to Supabase
    write_supabase_file(full_path, None, content)

def run_prompt(data):
    run_id = str(uuid.uuid4())
    Thread(target=background_task, args=(run_id,)).start()
    return {"run_id": run_id}
