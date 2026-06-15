# Contributing to Titans: Learning to Memorize at Test Time

Thank you for your interest in contributing! This project demonstrates the [Titans architecture](https://arxiv.org/abs/2501.00663) using seven specialized AI agents. Contributions of all kinds are welcome.

## Ways to Contribute

### 🐛 Reporting Bugs
- Check [existing issues](https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time/issues) before opening a new one
- Use the bug report template and include as much detail as possible
- Attach terminal output or screenshots when relevant

### 💡 Suggesting Features
- Open an [issue](https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time/issues) with the label `enhancement`
- Describe the use case and why it would benefit others

### 🔧 Submitting Pull Requests
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and test them
4. Commit with a clear message: `git commit -m "Add: description of change"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Open a Pull Request against `main`

## Development Setup

```bash
git clone https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time.git
cd Titans---Learning-to-Memorize-at-Test-Time
pip install -r requirements.txt
cp .env.sample .env
# Fill in at least one API key in .env
python main.py
```

## Code Style

- Follow PEP 8 for Python code
- Keep agent implementations consistent with the existing pattern in `agents/`
- Document new agent classes with a short docstring explaining which Titans component they represent

## Adding a New Agent

1. Create `agents/your_provider_agent.py` following the interface of existing agents
2. Register the agent in `main.py`
3. Add the provider's API key to `.env.sample` with a comment
4. Update the agent table in `README.md`

## Questions?

Feel free to open a [Discussion](https://github.com/ai-in-pm/Titans---Learning-to-Memorize-at-Test-Time/discussions) for anything that doesn't fit an issue.

We appreciate every contribution, no matter how small! ⭐
