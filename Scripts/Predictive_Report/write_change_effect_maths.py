import uuid
import yaml
from threading import Thread
from decimal import Decimal, ROUND_HALF_UP
from Engine.Files.write_supabase_file import write_supabase_file

def format_percent(value: float) -> str:
    return f"{Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}%"

def compute_summary_text(prompt_1_thinking: dict) -> str:
    output_lines = []

    for section_key in sorted(prompt_1_thinking.keys()):
        if not section_key.lower().startswith("section "):
            continue
        section = prompt_1_thinking[section_key]
        section_title = section.get("Section Title", "").strip()
        section_makeup_str = section.get("Section MakeUp", "0%").strip().replace('%', '')
        try:
            section_makeup = float(section_makeup_str)
        except ValueError:
            section_makeup = 0.0

        output_lines.append(f"{section_key}:")
        output_lines.append(f"Section Title: {section_title}")
        output_lines.append(f"Section MakeUp: {format_percent(section_makeup)}")

        sub_section_effects = []
        sub_section_number = 1

        for sub_key in sorted(section.keys()):
            sub = section[sub_key]
            if (
                isinstance(sub, dict)
                and sub_key.lower().startswith("sub-section ")
                and "Sub-Section Title" in sub
            ):
                sub_title = sub.get("Sub-Section Title", "").strip()
                sub_makeup_str = sub.get("Sub-Section MakeUp", "0%").strip().replace('%', '')
                sub_change_str = sub.get("Sub-Section Change", "0%").strip().replace('%', '')

                try:
                    sub_makeup = float(sub_makeup_str)
                    sub_change = float(sub_change_str)
                    sub_effect = (sub_makeup / 100) * sub_change
                except ValueError:
                    sub_makeup = 0.0
                    sub_change = 0.0
                    sub_effect = 0.0

                sub_section_effects.append(sub_effect)

                output_lines.append(f"Sub-Section {sub_section_number}:")
                output_lines.append(f"Sub-Section Title: {sub_title}")
                output_lines.append(f"Sub-Section MakeUp: {format_percent(sub_makeup)}")
                output_lines.append(f"Sub-Section Change: {format_percent(sub_change)}")
                output_lines.append(f"Sub-Section Effect: {format_percent(sub_effect)}")
                sub_section_number += 1

        section_change = sum(sub_section_effects)
        section_effect = (section_makeup / 100) * section_change

        output_lines.insert(-sub_section_number - 1, f"Section Change: {format_percent(section_change)}")
        output_lines.insert(-sub_section_number - 1, f"Section Effect: {format_percent(section_effect)}")
        output_lines.append("")  # spacer between sections

    return "\n".join(output_lines)

def background_task(run_id: str, raw_data: dict):
    filename = f"{run_id}.txt"
    supabase_path = f"Predictive_Report/Ai_Responses/Change_Effect_Maths/{filename}"

    try:
        raw_prompt = raw_data.get("prompt_1_thinking", "")
        prompt_data = yaml.safe_load(raw_prompt)
        summary = compute_summary_text(prompt_data)
    except Exception as e:
        summary = f"Failed to parse data: {str(e)}"

    write_supabase_file(supabase_path, summary)

def run_prompt(data):
    run_id = str(uuid.uuid4())
    Thread(target=background_task, args=(run_id, data)).start()
    return {"run_id": run_id}
