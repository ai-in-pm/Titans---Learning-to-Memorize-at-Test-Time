import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict, List, Any
import uvicorn
from agents.openai_agent import NeuralMemoryAgent
from agents.anthropic_agent import MemoryContextAgent
from agents.mistral_agent import MemoryGateAgent
from agents.groq_agent import MemoryLayerAgent
from agents.gemini_agent import ExperimentalAgent
from agents.cohere_agent import InnovationsAgent
from agents.emergence_agent import AnalysisAgent
import plotly.graph_objects as go
import os

app = FastAPI(title="Titans Demonstration Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class TitansOrchestrator:
    def __init__(self):
        self.agents = {
            "openai": NeuralMemoryAgent(),
            "anthropic": MemoryContextAgent(),
            "mistral": MemoryGateAgent(),
            "groq": MemoryLayerAgent(),
            "gemini": ExperimentalAgent(),
            "cohere": InnovationsAgent(),
            "emergence": AnalysisAgent()
        }
        self.collaborative_insights = []
        
    async def run_demonstrations(self):
        """Run all agent demonstrations"""
        results = {}
        for name, agent in self.agents.items():
            results[name] = await agent.demonstrate()
            # Generate collaborative insights
            await self._generate_collaborative_insights(name, results[name])
        return {
            "demonstrations": results,
            "collaborative_insights": self.collaborative_insights
        }
        
    async def _generate_collaborative_insights(self, agent_name: str, demo_results: Dict):
        """Generate collaborative insights between agents"""
        insights = []
        for other_name, other_agent in self.agents.items():
            if other_name != agent_name:
                insight = await other_agent.collaborate(demo_results)
                insights.append({
                    "from_agent": other_name,
                    "to_agent": agent_name,
                    "insight": insight
                })
        self.collaborative_insights.extend(insights)
        
    async def handle_interaction(self, agent_name: str, user_input: str):
        """Handle user interaction with specific agent"""
        if agent_name in self.agents:
            response = await self.agents[agent_name].interact(user_input)
            metrics = self.agents[agent_name].get_metrics()
            visualizations = self.agents[agent_name].visualize()
            return {
                "response": response,
                "metrics": metrics,
                "visualizations": visualizations
            }
        return {"error": f"Agent {agent_name} not found"}
        
    def get_combined_metrics(self) -> Dict[str, Any]:
        """Get combined performance metrics from all agents"""
        combined_metrics = {}
        for name, agent in self.agents.items():
            combined_metrics[name] = agent.get_metrics()
        return combined_metrics
        
    def create_combined_visualization(self) -> Dict[str, Any]:
        """Create a combined visualization of all agents' performance"""
        fig = go.Figure()
        
        for name, agent in self.agents.items():
            metrics = agent.get_metrics()
            fig.add_trace(go.Scatterpolar(
                r=list(metrics.values()),
                theta=list(metrics.keys()),
                fill='toself',
                name=name
            ))
            
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Combined Agent Performance"
        )
        
        return fig.to_dict()

orchestrator = TitansOrchestrator()

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse('static/index.html')

@app.get("/demonstrate")
async def demonstrate():
    """Run all demonstrations"""
    return await orchestrator.run_demonstrations()

@app.get("/metrics")
async def get_metrics():
    """Get combined metrics from all agents"""
    return orchestrator.get_combined_metrics()

@app.get("/visualization")
async def get_visualization():
    """Get combined visualization"""
    return orchestrator.create_combined_visualization()

@app.websocket("/ws/{agent_name}")
async def websocket_endpoint(websocket: WebSocket, agent_name: str):
    await websocket.accept()
    try:
        while True:
            user_input = await websocket.receive_text()
            response = await orchestrator.handle_interaction(agent_name, user_input)
            await websocket.send_json(response)
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
