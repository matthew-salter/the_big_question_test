import json
from datetime import datetime
from write_supabase_file import write_file_to_supabase

def main():
    # Create test filename and content
    filename = f"change_effect_test_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.txt"
    subdirectory = "The_Big_Question/Predictive_Report/Ai_Responses/Change_Effect_Maths"
    file_content = "TEST FILE"

    # Write file
    success = write_file_to_supabase(subdirectory, filename, file_content)

    if success:
        print(f"✅ File written: {subdirectory}/{filename}")
    else:
        print("❌ Failed to write file.")

if __name__ == "__main__":
    main()
