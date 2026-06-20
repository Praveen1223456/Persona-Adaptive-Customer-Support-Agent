# Persona Support Agent

A starter repository for a persona-aware support assistant with RAG retrieval and escalation handoff.

## Structure

- `data/` - support content and resources
- `src/` - application modules
- `app.py` - main CLI/interactive entrypoint
- `requirements.txt` - Python dependencies
- `.env` - local environment variables

## Setup

1. Create a Python virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

## Architecture

1. `src/config.py` loads configuration and thresholds.
2. `src/classifier.py` determines user persona from input.
3. `src/rag_pipeline.py` chunks documents and retrieves relevant context.
4. `src/generator.py` creates prompts for an LLM and simulates generation.
5. `src/escalator.py` decides when to escalate to a human specialist.

## Notes

- The `data/password_reset_guide.pdf` file is included as a required PDF placeholder.
- `.env` is intended for local secrets and should be gitignored.
