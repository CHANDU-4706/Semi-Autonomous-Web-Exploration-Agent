
import json
import time

class InsightLogger:
    def __init__(self):
        self.logs = []
        self.insights = {
            "visited_urls": [],
            "issues": [],
            "steps": []
        }

    def log_step(self, step_num, observation, decision, action_result):
        entry = {
            "step": step_num,
            "timestamp": time.time(),
            "observation": {
                "url": observation.get("url"),
                "summary": observation.get("page_text_summary")
            },
            "decision": decision,
            "result": action_result
        }
        self.logs.append(entry)
        self.insights["steps"].append(entry)
        
        # Track visited URLs
        url = observation.get("url")
        if url and url not in self.insights["visited_urls"]:
            self.insights["visited_urls"].append(url)

        # Track explicitly logged issues
        if "issues" in decision: # If decision engine found issues
             self.insights["issues"].extend(decision["issues"])
             
        # Also check if observation had errors
        if observation.get("errors"):
             for err in observation["errors"]:
                 self.insights["issues"].append({"type": "observed_error", "details": err, "url": url})

        print(f"[Logger] Step {step_num} logged.")

    def save_insights(self, filepath="reports/insights.json"):
        with open(filepath, "w") as f:
            json.dump(self.insights, f, indent=2)
        print(f"[Logger] Insights saved to {filepath}")
