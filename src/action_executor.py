
import time

class ActionExecutor:
    def __init__(self, browser_controller):
        self.browser = browser_controller

    def execute(self, action):
        """
        Executes the given action dict on the browser.
        Returns a result string.
        """
        if not action:
            return "No action to execute"
            
        action_type = action.get("type", "").upper()
        target = action.get("target")
        page = self.browser.get_page()

        print(f"[Executor] Executing: {action_type} on {target}")

        try:
            if action_type == "CLICK":
                # Try to click by text first, then selector
                # Playwright's "text=" is powerful
                try:
                    page.click(f"text={target}", timeout=2000)
                except:
                    # Fallback to generic selector if it looks like an ID or Selector
                    page.click(target)
                return "Clicked successfully"

            elif action_type == "TYPE":
                value = action.get("value", "")
                # Try to fill by placeholder or name or id
                try:
                    page.fill(f"input[name='{target}']", value, timeout=2000)
                except:
                     try:
                        page.fill(f"input[id='{target}']", value, timeout=2000)
                     except:
                        page.fill(target, value) # generic selector
                return f"Typed '{value}'"

            elif action_type == "NAVIGATE":
                url = action.get("url")
                self.browser.navigate(url)
                return f"Navigated to {url}"

            elif action_type == "STOP":
                return "Stopped by agent"

            else:
                return f"Unknown action type: {action_type}"

        except Exception as e:
            return f"Action execution failed: {str(e)}"
