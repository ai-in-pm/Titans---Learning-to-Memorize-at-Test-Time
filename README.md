# Titans Demonstration Platform
<img width="1913" height="1018" alt="image" src="https://github.com/user-attachments/assets/a1207510-6c37-4a2a-93d3-a6dab0139184" />

This project demonstrates ideas from the paper *Titans: Learning to Memorize at Test Time* using seven specialized AI agents and a native desktop interface.

Paper: https://arxiv.org/pdf/2501.00663v1

## What It Runs

The primary app is now a **native desktop UI**:

- Entry point: `main.py`
- Windows executable: `titans.exe`
- Launcher: `titans.bat`
- UI: agent selection, demonstration runs, collaborative insights, live metrics, and real-time visual interaction

## Agents

1. OpenAI Agent (Neural Memory Module)
2. Anthropic Agent (Memory as Context)
3. Mistral Agent (Memory as Gate)
4. Groq Agent (Memory as Layer)
5. Gemini Agent (Experimental Validation)
6. Cohere Agent (Innovations)
7. Emergence Agent (Analysis)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.sample` to `.env` and fill in the API keys you plan to use.

2. Configure optional provider keys in `.env`:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `MISTRAL_API_KEY`
- `GROQ_API_KEY`
- `GOOGLE_API_KEY`
- `COHERE_API_KEY`
- `EMERGENCE_API_KEY`

Note: The desktop app starts even if some providers are unavailable. Unavailable agents are shown with status/details in the UI.

## Run

Recommended:

```bat
titans.exe
```

Alternative:

```bat
titans.bat
```

Other option:

```bash
python main.py
```

Important: run from the project folder, or use `titans.bat` (it handles path setup automatically).

## Desktop Features

- Native Tkinter desktop interface
- Real-time runtime telemetry and visual panel
- Numeric-series extraction from demonstration output
- Play/scrub chart interaction for time-based behavior
- Output console + agent details pane
- Adjustable split-pane layout with remembered last position

## Troubleshooting

- If the app closes quickly, run with `titans.bat` and read the terminal output.
- If `python main.py` fails from `D:\GitHub\Titans`, switch to the project directory first.
- `google.generativeai` deprecation warnings are non-fatal warnings.

## Project Files

- `main.py`: Desktop application
- `titans.exe`: Packaged Windows executable for desktop launch
- `titans.bat`: Robust launcher for Windows
- `main.pygui`: GUI Pie metadata file (not the runtime entrypoint)
- `agents/`: Provider-specific agent implementations
