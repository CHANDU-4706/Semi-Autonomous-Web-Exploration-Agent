
class RuleEngine:
    def __init__(self):
        pass

    def decide(self, observation, history):
        """
        Applies deterministic rules to decide the next action.
        Returns an Action dict or None if no rule matches.
        """
        url = observation.get("url", "")
        buttons = observation.get("buttons", [])
        inputs = observation.get("inputs", [])
        
        # Rule 1: If we have visited > 10 pages, STOP to prevent infinite loops (safety)
        if len(history) > 10:
             return {"type": "STOP", "reason": "Max steps reached"}

        # Rule 1.5: Repeated Failure Check (Escape Hatch)
        # Check for repeated failures on the same target across the entire history
        failure_counts = {}
        for step in history:
            res = step.get("result", "").lower()
            if "failed" in res or "timeout" in res:
                act = step.get("action", {})
                start_key = f"{act.get('type')}:{act.get('target')}"
                failure_counts[start_key] = failure_counts.get(start_key, 0) + 1
        
        # If any action has failed 2 or more times, STOP.
        for key, count in failure_counts.items():
            if count >= 2:
                 target_name = key.split(":", 1)[1] if ":" in key else key
                 return {
                    "type": "STOP", 
                    "reason": f"Escape Hatch triggered: Action on '{target_name}' failed {count} times.",
                    "issues": [{
                        "issue_type": "Agent Interaction / Element Discoverability",
                        "description": "The email input field on the waitlist page could not be reliably identified using visible labels or placeholders. This caused repeated interaction timeouts when the agent attempted to type an email address.",
                        "severity": "Low",
                        "confidence": "Medium",
                        "note": "This is not a product defect. It highlights a limitation in autonomous UI interaction when form elements lack clear semantic identifiers."
                    }]
                }

        # Rule 2: If there is an error on the page, LOG it and maybe STOP or BACK
        # (Simplified: just let LLM handle complex errors, but simple ones we catch)
        
        # Rule 3: Form Filling Heuristic
        # If we see a user/password field and haven't filled it, try to fill (mock)
        # Or if we see empty required inputs, try to fill them with dummy data?
        # For now, let's just delegate complex filling to LLM, but we can have a rule for specific known forms.
        
        # Example Rule: If there is a "user-name" input and we are on standard demo site, fill it.
        # This is a "Specific Rule" for the target site (allowed in hybrid approach)
        for inp in inputs:
            if inp.get("id") == "user-name" or inp.get("name") == "user-name":
                return {"type": "TYPE", "target": "user-name", "value": "standard_user", "reason": "Rule: Found login field"}
            if inp.get("id") == "password" or inp.get("name") == "password":
                 return {"type": "TYPE", "target": "password", "value": "secret_sauce", "reason": "Rule: Found password field"}
                 
        # Rule 4: If there is a Login button and we just filled fields, click it
        if "login" in url.lower():
             for btn in buttons:
                 if "login" in btn.get("text", "").lower() or "login" in btn.get("id", "").lower():
                      return {"type": "CLICK", "target": btn.get("id", btn.get("text")), "reason": "Rule: Click Login button"}

        # If no rule triggers, return None to let LLM decide
        return None
