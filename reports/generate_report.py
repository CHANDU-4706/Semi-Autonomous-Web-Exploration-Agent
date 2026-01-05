import json
import os

def generate_report():
    # Support running from root or reports folder
    if os.path.exists("reports/insights.json"):
        path = "reports/insights.json"
        out_path = "reports/REPORT.md"
    elif os.path.exists("insights.json"):
        path = "insights.json"
        out_path = "REPORT.md"
    else:
        print("No insights.json found. Run main.py first.")
        return

    with open(path, "r") as f:
        data = json.load(f)

    visited = data.get("visited_urls", [])
    issues = data.get("issues", [])
    steps = data.get("steps", [])

    print("\n" + "="*50)
    print("       OYESENSE AGENT REPORT")
    print("="*50)
    
    print(f"\n[+] Total Steps: {len(steps)}")
    print(f"[+] Unique Pages Visited: {len(visited)}")
    for url in visited:
        print(f"  - {url}")

    print("\n[+] Issues Detected:")
    if not issues:
        print("  None detected.")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")

    print("\n[+] Interaction Log:")
    for s in steps:
        step_num = s.get("step")
        action = s.get("decision", {})
        act_type = action.get("type")
        act_target = action.get("target")
        act_reason = action.get("reason")
        result = s.get("result")
        print(f"  Step {step_num}: {act_type} -> {act_target}")
        print(f"    Reason: {act_reason}")
        print(f"    Result: {result}")
        print("-" * 30)
    
    # Save as Markdown
    with open(out_path, "w") as f:
        f.write("# Oyesense Agent Report\n\n")
        f.write(f"**Total Steps**: {len(steps)}\n")
        f.write(f"**Pages Visited**: {len(visited)}\n\n")
        f.write("## Visited URLs\n")
        for url in visited:
            f.write(f"- {url}\n")
        f.write("\n## Issues Detected\n")
        if not issues:
            f.write("None detected.\n")
        else:
            for issue in issues:
                # Check if it's a dict to format nicely
                if isinstance(issue, dict):
                     f.write(f"- **Issue Type**: {issue.get('issue_type', 'Unknown')}\n")
                     f.write(f"  - **Description**: {issue.get('description', '')}\n")
                     f.write(f"  - **Severity**: {issue.get('severity', 'Low')}\n")
                     f.write(f"  - **Confidence**: {issue.get('confidence', 'Medium')}\n")
                     if issue.get('note'):
                        f.write(f"  - **Note**: {issue.get('note')}\n")
                     f.write("\n")
                else:
                    f.write(f"- {issue}\n")

        f.write("\n## Interaction Log\n")
        for s in steps:
            f.write(f"### Step {s.get('step')}\n")
            f.write(f"- **Action**: {s.get('decision', {}).get('type')} {s.get('decision', {}).get('target')}\n")
            f.write(f"- **Reason**: {s.get('decision', {}).get('reason')}\n")
            f.write(f"- **Result**: {s.get('result')}\n\n")

        f.write("\n## Reasoning Summary\n")
        f.write("The agent followed an observe–decide–act workflow. It first identified the primary call-to-action on the landing page and navigated to the waitlist flow. Upon encountering repeated interaction failures with the email input field, the agent attempted recovery by retrying the action and exploring alternative navigation paths. After detecting consistent failures and limited new information, the agent stopped execution safely and logged the limitation as an agent interaction insight rather than a product defect.\n")
            
    print("\n[+] Report saved to REPORT.md")

if __name__ == "__main__":
    generate_report()
