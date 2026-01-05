
import os
import time
from dotenv import load_dotenv
from src.browser_controller import BrowserController
from src.page_observer import PageObserver
from src.rule_engine import RuleEngine
from src.llm_decision_engine import LLMDecisionEngine
from src.action_executor import ActionExecutor
from src.insight_logger import InsightLogger
from reports.generate_report import generate_report


# Load env variables
load_dotenv()

def main():
    print("--- Oyesense Semi-Autonomous Agent Starting ---")
    
    # 1. Configuration
    target_url = "https://www.aurick.ai"


    max_steps = 15

    # 2. Initialize Components
    browser = BrowserController(headless=False)
    rule_engine = RuleEngine()
    llm_engine = LLMDecisionEngine()
    executor = ActionExecutor(browser)
    logger = InsightLogger()

    if not llm_engine.llm:
        print(" [!] CAUTION: No OpenAI API Key found. Agent will rely only on Rules (very limited).")

    try:
        # 3. Start Browser
        browser.start()
        browser.navigate(target_url)
        page = browser.get_page()
        observer = PageObserver(page)

        history = []
        
        # 4. Agent Loop
        for step in range(1, max_steps + 1):
            print(f"\n--- Step {step} ---")
            
            # Observe
            observation = observer.observe()
            print(f"Current URL: {observation.get('url')}")
            
            # Decide (Hybrid)
            # A. Rule Engine
            action = rule_engine.decide(observation, history)
            decision_source = "RULE"
            
            # B. LLM Engine (if no rule triggered)
            if not action:
                print("No rule triggered. Consulting LLM...")
                action = llm_engine.decide(observation, history)
                decision_source = "LLM"
            
            print(f"Decision ({decision_source}): {action}")
            
            # Execute
            if action:
                result = executor.execute(action)
            else:
                result = "No decision made"
                
            print(f"Result: {result}")

            # Log
            logger.log_step(step, observation, action, result)
            history.append({"step": step, "action": action, "result": result})

            # Check Stop
            if action and action.get("type") == "STOP":
                print("Agent requested to STOP.")
                break
            
            # Small pause for visual debugging
            time.sleep(2)

    except Exception as e:
        print(f"Critical Error: {e}")
    finally:
        # 5. Cleanup & Save
        # 5. Cleanup & Save
        logger.save_insights()
        generate_report()
        browser.close()

        print("--- Agent Session Ended ---")

if __name__ == "__main__":
    main()
