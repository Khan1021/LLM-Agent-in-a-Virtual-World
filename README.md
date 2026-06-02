# Autonomous LLM Routing Agent in a Virtual GridWorld

An autonomous AI agent harness built in Python that connects a custom simulation environment (`GridWorld`) to a Large Language Model (LLM) routing brain. The agent dynamically parses spatial text observations, processes wall boundaries, and navigates from a starting coordinate to a target objective without hardcoded pathfinding algorithms.

## Features
* **Isolated Environment Simulation:** Built a standalone 5x5 `GridWorld` simulation class complete with coordinate logic, edge-of-map collision detection, and win-state triggers.
* **Spatial Context Pre-Processing:** Engineered a dynamic prompt system that calculates wall boundaries *before* querying the LLM, passing real-time proximity alerts to prevent the agent from colliding with walls.
* **Structured Payload Parsing:** Integrated regular expressions (`re`) to clean and isolate bracketed action commands (e.g., `[MOVE_RIGHT]`) out of raw LLM text completions.
* **Modular Code Architecture:** Implemented a standard `if __name__ == "__main__":` entry point to ensure execution safety, scope containment, and component reusability.

## Tech Stack & Dependencies
* **Language:** Python 3.x
* **AI Orchestration:** OpenAI SDK / Groq SDK (LLM integration)
* **Model Used:** `gpt-4o-mini` (or `llama-3.3-70b-versatile`)
* **Environment Management:** Python Virtual Environments (`.venv`)

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/LLM-Agent-in-a-Virtual-World.git](https://github.com/YOUR_GITHUB_USERNAME/LLM-Agent-in-a-Virtual-World.git)
   cd LLM-Agent-in-a-Virtual-World