
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

class LLMDecisionEngine:
    def __init__(self):
        # Strictly use Groq as requested
        groq_key = os.getenv("GROQ_API_KEY")
        
        if groq_key:
             print("[LLM] Using Groq (Llama-3-70b/8b)")
             self.llm = ChatGroq(
                 model="llama-3.3-70b-versatile", 
                 temperature=0.7,
                 api_key=groq_key
             )
        else:
             print("WARNING: GROQ_API_KEY not found. LLM will fail.")
             self.llm = None

    def decide(self, observation, history):
        """
        Asks the LLM what to do next based on observation and history.
        """
        if not self.llm:
            return {"type": "STOP", "reason": "No API Key available"}

        # Construct Prompt
        system_prompt = """You are a semi-autonomous web agent. 
        Goal: Explore the website, interact with it, and identify confusing or broken flows.
        
        You will receive the current page state (url, buttons, inputs, text summary) and history.
        Decide the next action.
        
        Available Actions:
        - {{"type": "CLICK", "target": "id or text of element", "reason": "..."}}
        - {{"type": "TYPE", "target": "id or name of input", "value": "text to type", "reason": "..."}}
        - {{"type": "NAVIGATE", "url": "full url", "reason": "..."}}
        - {{"type": "STOP", "reason": "..."}}
        
        Return ONLY a JSON object representing the action. Do not wrap in markdown.
        """
        
        # Construct User Message carefully
        user_content = f"""
        Current URL: {observation.get('url')}
        Page Summary: {observation.get('page_text_summary')}
        Interactive Elements:
        - Buttons: {str(observation.get('buttons')[:10])} ... (truncated)
        - Inputs: {str(observation.get('inputs'))}
        - Links: {str(observation.get('links')[:10])} ... (truncated)
        
        History (Last 3 steps): {str(history[-3:])}
        
        What should I do next?
        """

        try:
            # Use a simple template where we inject the user content as a variable
            # This avoids LangChain trying to parse the JSON in user_content as variables
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", "{user_input}")
            ])
            chain = prompt | self.llm
            response = chain.invoke({"user_input": user_content})
            
            content = response.content.strip()
            # Clean up markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            action = json.loads(content)
            return action
        except Exception as e:
            print(f"[LLM Error] {e}")
            return {"type": "STOP", "reason": f"LLM Error: {e}"}
