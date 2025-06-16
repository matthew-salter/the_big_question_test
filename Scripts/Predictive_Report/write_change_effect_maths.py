import uuid
import json
import yaml
from threading import Thread
from Engine.Files.write_supabase_file import write_supabase_file

def extract_summary_text(prompt_1_thinking: dict) -> str:
    output_lines = []

    for section_key in sorted(prompt_1_thinking.keys()):
        if not section_key.lower().startswith("section "):
            continue
        section = prompt_1_thinking[section_key]
        section_title = section.get("Section Title", "").strip()
        section_makeup = section.get("Section MakeUp", "").strip()
        output_lines.append(f"{section_key}:")
        output_lines.append(f"Section Title: {section_title}")
        output_lines.append(f"Section MakeUp: {section_makeup}")

        for sub_key in sorted(section.keys()):
            if not sub_key.lower().startswith("sub-section "):
                continue
            sub = section[sub_key]
            sub_title = sub.get("Sub-Section Title", "").strip()
            sub_makeup = sub.get("Sub-Section MakeUp", "").strip()
            sub_change = sub.get("Sub-Section Change", "").strip()
            output_lines.append(f"{sub_key}:")
            output_lines.append(f"Sub-Section Title: {sub_title}")
            output_lines.append(f"Sub-Section MakeUp: {sub_makeup}")
            output_lines.append(f"Sub-Section Change: {sub_change}")

    return "\n".join(output_lines)

def background_task(run_id: str, raw_data: dict):
    filename = f"{run_id}.txt"
    supabase_path = f"Predictive_Report/Ai_Responses/Change_Effect_Maths/{filename}"

    try:
        raw_prompt = raw_data.get("prompt_1_thinking", "")
        prompt_data = yaml.safe_load(raw_prompt)  # ✅ correct for YAML-style text
        summary = extract_summary_text(prompt_data)
    except Exception as e:
        summary = f"Failed to parse data: {str(e)}"

    write_supabase_file(supabase_path, summary)

def run_prompt(data):
    run_id = str(uuid.uuid4())
    Thread(target=background_task, args=(run_id, data)).start()
    return {"run_id": run_id}
