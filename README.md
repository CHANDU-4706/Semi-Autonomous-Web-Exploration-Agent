# Oyesense Semi-Autonomous Web Agent

This repository contains a **Semi-Autonomous Web Interaction Agent** built for the Oyesense Challenge.

## 🚀 Overview

The agent is designed to navigate a website, observe its content, and make decisions on how to interact with it. It focuses on testing **Aurick.ai** and uses a **Hybrid Architecture** combining deterministic **Rules** for safety/speed and **LLM Reasoning** (Groq/Llama-3) for complex decision-making.

### Key Features

- **Hybrid Brain**: Rules for obvious actions (forms, errors), LLM for uncertain flows.
- **Robust Observation**: Scans the DOM for interactive elements (buttons, inputs, links).
- **Self-Correction**: Detects loops and errors.
- **Insight Logging**: Tracks every step, reason, and result in `insights.json`.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Browser Automation**: Playwright
- **Reasoning**: LangChain + Groq (Llama-3)
- **Testing**: PyTest

## 📂 Project Structure

- `main.py`: Entry point. Orchestrates the agent loop.
- `src/`:
  - `browser_controller.py`: Manages Playwright instance.
  - `page_observer.py`: Parses the page into structured observations.
  - `rule_engine.py`: Hard-coded heuristics.
  - `llm_decision_engine.py`: AI-based decision maker.
  - `action_executor.py`: Translates decisions into Playwright actions.
  - `insight_logger.py`: Records session data.
- `reports/`:
  - `generate_report.py`: Script to generate REPORT.md.
  - `insights.json`: Raw session logs.
  - `REPORT.md`: Human-readable report.
- `requirements.txt`: Dependencies.

## 🏃 How to Run

1.  **Clone the Repository**

    ```bash
    git clone <repo_url>
    cd Oyesense
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3.  **Configure Environment**
    Create a `.env` file and add your Groq API Key:

    ```
    GROQ_API_KEY=
    ```

4.  **Run the Agent**
    ```bash
    python main.py
    ```
    The agent automatically targets `https://www.aurick.ai`.

## 🧠 Decision Logic

The agent follows this loop:

1.  **Observe**: Capture URL, Title, Buttons, Inputs, Text.
2.  **Rule Check**:
    - _Is there an error?_ -> Log it.
    - _Is there an obvious form?_ -> Fill it.
    - _Are actions failing repeatedly?_ -> **Escape Hatch** (Stops to prevent loops).
    - _Are we stuck in a loop?_ -> Stop.
3.  **LLM Check** (if no rule applies):
    - Send State + History to Llama-3 (via Groq).
    - Ask: "What should I do next to explore effectively?"
4.  **Act**: Click, Type, or Navigate.

## 📊 Outputs

- Console logs showing real-time reasoning.
- `insights.json`: Detailed log of the session.
- `REPORT.md`: Automatically generated, human-readable summary of the run.

## ✅ Challenge Compliance

This project meets all core expectations of the **Oyesense Challenge**:

1.  **Browser Interaction**: Uses **Playwright** to open a real browser and interact with dynamic elements (Login, Inventory).
2.  **Decision-Making**: A **Hybrid Architecture** ensures decisions are made at runtime (LLM) while keeping core flows safe (Rules).
3.  **Reasoning**: The agent "thinks" before acting (see console logs & `insights.json`).
4.  **Output**: Generates a detailed `REPORT.md` and structured `insights.json`.

## 🔮 Future Improvements

1.  **Vision Capabilities (Multimodal AI)**:

    - Integrate vision models (like Llama-3-Vision) to "see" layout issues, popups, and visual bugs that code-only analysis misses.

2.  **Self-Healing Selectors**:

    - If a selector fails (like the email input issue), automatically feed the HTML to the LLM to generate a new, valid selector on the fly.

3.  **Knowledge Graph Navigation**:

    - Build a state machine graph (URL nodes, Action edges) to remember the site map and prevent circular navigation in complex apps.

4.  **CI/CD Integration**:
    - Containerize with Docker and run as a GitHub Action to post the `REPORT.md` as a PR comment automatically.
