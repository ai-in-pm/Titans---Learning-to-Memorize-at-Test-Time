# Titans Demonstration Platform

This platform implements seven AI agents demonstrating key concepts from the paper "Titans: Learning to Memorize at Test Time". Each agent specializes in a different aspect of the architecture and works collaboratively to provide a comprehensive understanding.

The development of the Github Repository was inspired by the "Titans: Learning to Memorize at Test Time" paper. To read the full paper, visit https://arxiv.org/pdf/2501.00663v1

## Agents

1. **OpenAI Agent (Neural Memory Module)**
   - Demonstrates memory mechanisms
   - Real-time decay simulation
   - Interactive memory retrieval

2. **Anthropic Agent (Memory as Context)**
   - Historical context integration
   - Language modeling demonstrations

3. **Mistral Agent (Memory as Gate)**
   - Short-term/long-term memory gating
   - Efficiency demonstrations

4. **Groq Agent (Memory as Layer)**
   - Neural network layer integration
   - Architecture comparisons

5. **Gemini Agent (Experimental Validation)**
   - Scalability demonstrations
   - Information retrieval tasks

6. **Cohere Agent (Innovations)**
   - Memory design principles
   - Real-world applications

7. **Emergence Agent (Analysis)**
   - Architecture analysis
   - Scalability discussions

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   - OPENAI_API_KEY
   - ANTHROPIC_API_KEY
   - MISTRAL_API_KEY
   - GROQ_API_KEY
   - GOOGLE_API_KEY
   - COHERE_API_KEY
   - EMERGENCE_API_KEY

3. Run the platform:
   ```bash
   python main.py
   ```

## Usage

1. Access the web interface at `http://localhost:8000`
2. View demonstrations via `/demonstrate` endpoint
3. Interact with agents through WebSocket connections
4. View real-time visualizations and metrics

## Features

- Real-time demonstrations
- Interactive agent communication
- Dynamic visualizations
- Performance metrics
- Collaborative analysis

## Architecture

The platform uses a modular architecture where each agent implements the base TitansAgent interface. The main orchestrator manages agent interactions and provides a unified API for demonstrations and user interactions.
