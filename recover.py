import json

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
                            # these were written to root originally
                            content = args.get('CodeContent', '').strip('"')
                            # The content in JSON log has escaped newlines like \n
                            content = content.encode('utf-8').decode('unicode_escape')
                            print(f"Recovering {target}...")
                            with open(target, 'w', encoding='utf-8') as out_f:
                                out_f.write(content)
        except Exception as e:
            pass

print("Recovery finished.")
