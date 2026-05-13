import os
import shutil
import glob
import re
import json

base_dir = r"c:\2024-2028\Semester 4\Pengembangan Sumbeer Belajar Inovatif\projek-psbi"
template_dir = os.path.join(base_dir, "dashboard", "templates", "dashboard")

# Restore dist files
dist_files = glob.glob(os.path.join(base_dir, "dist", "*.html"))
for f in dist_files:
    shutil.copy(f, template_dir)

# Recover login, register, forgot-password from log
log_file = r"C:\Users\Zamzami\.gemini\antigravity\brain\14fedb23-1563-4f03-affa-8bb845eb409e\.system_generated\logs\overview.txt"
with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line.strip())
            if data.get('type') == 'PLANNER_RESPONSE' and data.get('source') == 'MODEL':
                tool_calls = data.get('tool_calls', [])
                for tc in tool_calls:
                    if tc.get('name') == 'write_to_file':
                        args = tc.get('args', {})
                        target = args.get('TargetFile', '').strip('"')
                        if target and target.endswith('.html') and 'dashboard' not in target:
                            content = args.get('CodeContent', '').strip('"')
                            content = content.encode('utf-8').decode('unicode_escape')
                            dest = os.path.join(template_dir, os.path.basename(target))
                            with open(dest, 'w', encoding='utf-8') as out_f:
                                out_f.write(content)
        except Exception as e:
            pass

# Run conversion
import subprocess
subprocess.run(["python", "convert_html.py"], cwd=base_dir)
subprocess.run(["python", "update_auth_templates.py"], cwd=base_dir)

# Fix backslashes properly
for f in glob.glob(os.path.join(template_dir, "*.html")):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace("\\'", "'")
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Recovery and cleanup completed successfully.")
