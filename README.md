<div align="center">

# 🧠 Titans: Learning to Memorize at Test Time

[![Stars](https://img.shields.io/github/stars/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time?style=for-the-badge&logo=github&color=FFD700)](https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time/stargazers)
[![Forks](https://img.shields.io/github/forks/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time?style=for-the-badge&logo=github&color=blue)](https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![arXiv](https://img.shields.io/badge/arXiv-2501.00663-b31b1b?style=for-the-badge&logo=arxiv)](https://arxiv.org/abs/2501.00663)

**An interactive multi-agent demonstration platform for the landmark *Titans* architecture — the first neural network to learn how to memorize at test time.**

<img src="https://github.com/user-attachments/assets/a1207510-6c37-4a2a-93d3-a6dab0139184" width="900" alt="Titans Demonstration Platform" />

</div>

---

## ✨ What Makes This Special

The [Titans paper](https://arxiv.org/abs/2501.00663) introduces a groundbreaking memory architecture that **learns what to remember during inference** — no more fixed context windows. This repository brings those ideas to life with:

- **7 specialized AI agents**, each embodying a different perspective on the Titans architecture
- **Native desktop UI** with real-time telemetry, interactive charts, and live visualization
- **Side-by-side agent collaboration** — watch how GPT-4, Claude, Mistral, Groq, Gemini, Cohere, and Emergence reason about the same memory problem
- **Zero-friction setup** — runs with a single command, even if only one API key is configured

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time.git
cd Titans---Learning-to-Memorize-at-Test-Time

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
cp .env.sample .env
# Edit .env and add your API keys (only the providers you want to use)

# 4. Launch
python main.py
```

> **Windows users:** Run `titans.bat` (handles path setup automatically) or launch `titans.exe` for a bundled, dependency-free experience.

---

## 🤖 The Seven Agents

Each agent explores a distinct component of the Titans architecture through a different LLM lens:

| # | Agent | Provider | Titans Role |
|---|-------|----------|-------------|
| 1 | **Neural Memory Module** | OpenAI (GPT-4) | Core long-term memory model |
| 2 | **Memory as Context** | Anthropic (Claude) | Attention-based context memory |
| 3 | **Memory as Gate** | Mistral | Gating mechanism for memory flow |
| 4 | **Memory as Layer** | Groq | Per-layer memory integration |
| 5 | **Experimental Validation** | Google Gemini | Benchmarking & ablation analysis |
| 6 | **Innovations** | Cohere | Novel extensions & improvements |
| 7 | **Analysis** | Emergence | Cross-agent synthesis & insights |

---

## 🖥️ Desktop Features

The native Tkinter interface provides a rich interactive environment:

- **Agent selector panel** — choose which agents participate in each run
- **Live demonstration console** — real-time streamed output from each agent
- **Runtime telemetry** — per-agent timing and token usage metrics displayed live
- **Numeric-series chart** — automatically extracted from agent output, with play/scrub interaction
- **Collaborative insights view** — synthesized cross-agent analysis panel
- **Adjustable split-pane layout** with remembered position across sessions

---

## 🔑 API Key Configuration

Copy `.env.sample` to `.env` and add the keys for any providers you want to use:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MISTRAL_API_KEY=...
GROQ_API_KEY=...
GOOGLE_API_KEY=...
COHERE_API_KEY=...
EMERGENCE_API_KEY=...
```

You do **not** need all keys — the platform works with any subset and shows a graceful status for unavailable agents.

---

## 🧪 The Science: Titans Architecture

The Titans paper proposes three distinct ways to integrate a **neural long-term memory module** into transformer models:

1. **Memory as Context (MAC)** — memory tokens are prepended to the attention context window, giving the model access to a persistent external memory
2. **Memory as Gate (MAG)** — memory output multiplicatively gates the attention output, controlling information flow
3. **Memory as Layer (MAL)** — the memory module is inserted as a standalone layer within the network stack

The key innovation is **test-time learning of what to memorize**: the memory module updates its parameters during inference based on a surprise metric, allowing the model to adaptively retain information that contradicts its current knowledge — without any additional training.

---

## 📁 Project Structure

```
Titans---Learning-to-Memorize-at-Test-Time/
├── main.py              # Desktop application entry point
├── titans.bat           # Windows launcher (handles path setup automatically)
├── titans.exe           # Pre-built Windows executable (no Python required)
├── requirements.txt     # Python dependencies
├── .env.sample          # API key template
├── agents/              # Provider-specific agent implementations
│   ├── openai_agent.py
│   ├── anthropic_agent.py
│   ├── mistral_agent.py
│   ├── groq_agent.py
│   ├── gemini_agent.py
│   ├── cohere_agent.py
│   └── emergence_agent.py
├── static/              # UI assets
└── Titans Paper.pdf     # The original research paper (arXiv:2501.00663)
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| App closes immediately on launch | Run via `titans.bat` to read the terminal error output |
| `python main.py` fails with path error | `cd` into the project folder first |
| `google.generativeai` deprecation warnings | Non-fatal — the app still works correctly |
| An agent shows "unavailable" | That provider's API key is missing or invalid in `.env` |

---

## 📖 Citation

If this project helps your research or learning, please cite the original paper:

```bibtex
@article{behrouz2025titans,
  title     = {Titans: Learning to Memorize at Test Time},
  author    = {Ali Behrouz and Peilin Zhong and Vahab Mirrokni},
  journal   = {arXiv preprint arXiv:2501.00663},
  year      = {2025},
  url       = {https://arxiv.org/abs/2501.00663}
}
```

---

## 🤝 Contributing

Contributions are warmly welcome! Here's how to get involved:

- 🐛 **Report bugs** by opening an [Issue](https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time/issues)
- 💡 **Request features** via Issues or Discussions
- 🔧 **Submit a Pull Request** with bug fixes, new agents, or UI improvements
- ⭐ **Star this repo** if you find it useful — it helps others discover the project!

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for full details.

---

<div align="center">

Made with ❤️ by [ai-in-pm](https://github.com/ai-in-pm) · Inspired by the [Titans paper](https://arxiv.org/abs/2501.00663)

**Found this useful? Please give it a ⭐ — it really helps!**

</div>
