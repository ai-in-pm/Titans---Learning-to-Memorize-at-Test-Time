import streamlit as st
import plotly.graph_objects as go
from agents.openai_agent import NeuralMemoryAgent
from agents.anthropic_agent import MemoryContextAgent
from agents.mistral_agent import MemoryGateAgent
from agents.groq_agent import MemoryLayerAgent
from agents.gemini_agent import ExperimentalAgent
from agents.cohere_agent import InnovationsAgent
from agents.emergence_agent import AnalysisAgent
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize agents
class AgentManager:
    def __init__(self):
        self.agents = {
            "OpenAI (Neural Memory)": NeuralMemoryAgent(),
            "Anthropic (Memory Context)": MemoryContextAgent(),
            "Mistral (Memory Gate)": MemoryGateAgent(),
            "Groq (Memory Layer)": MemoryLayerAgent(),
            "Gemini (Experimental)": ExperimentalAgent(),
            "Cohere (Innovations)": InnovationsAgent(),
            "Emergence (Analysis)": AnalysisAgent()
        }

# Create agent manager instance
agent_manager = AgentManager()

# Set page config
st.set_page_config(
    page_title="Titans Demonstration Platform",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 Titans: Learning to Memorize at Test Time")
st.markdown("""
This platform demonstrates key concepts from the Titans paper through seven specialized AI agents.
Each agent focuses on a different aspect of the architecture and works collaboratively to provide
a comprehensive understanding of the system.
""")

# Sidebar for agent selection
st.sidebar.title("Agent Selection")
selected_agent = st.sidebar.selectbox(
    "Choose an agent to interact with:",
    list(agent_manager.agents.keys())
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"🔍 {selected_agent}")
    
    # Input area
    user_input = st.text_area("Enter your query about Titans:", height=100)
    
    if st.button("Run Demonstration"):
        with st.spinner("Running demonstration..."):
            try:
                agent = agent_manager.agents[selected_agent]
                # Run demonstration asynchronously
                demo_result = asyncio.run(agent.demonstrate())
                
                # Display demonstration results
                st.subheader("📊 Demonstration Results")
                
                # Display visualizations if available
                if "visualization" in demo_result:
                    st.plotly_chart(go.Figure(demo_result["visualization"]))
                
                # Display metrics if available
                if "metrics" in demo_result:
                    st.subheader("📈 Performance Metrics")
                    for metric, value in demo_result["metrics"].items():
                        st.metric(
                            label=metric.replace("_", " ").title(),
                            value=f"{value:.2f}"
                        )
                
                # Display any textual results
                if "title" in demo_result:
                    st.subheader(demo_result["title"])
                    st.write(demo_result)
                    
            except Exception as e:
                st.error(f"Error during demonstration: {str(e)}")

with col2:
    st.header("📈 Live Metrics")
    
    # Display agent's current metrics
    agent = agent_manager.agents[selected_agent]
    metrics = agent.get_metrics()
    
    for metric, value in metrics.items():
        st.metric(
            label=metric.replace("_", " ").title(),
            value=f"{value:.2f}"
        )
    
    # Create and display radar chart of metrics
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        name=selected_agent
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Agent Performance Profile"
    )
    
    st.plotly_chart(fig)

# Collaborative Insights Section
st.header("🤝 Collaborative Insights")
if st.button("Generate Collaborative Insights"):
    with st.spinner("Generating insights..."):
        try:
            # Get the current agent
            current_agent = agent_manager.agents[selected_agent]
            
            # Get demonstration results from current agent
            demo_results = asyncio.run(current_agent.demonstrate())
            
            # Generate collaborative insights
            insights = []
            for other_name, other_agent in agent_manager.agents.items():
                if other_name != selected_agent:
                    insight = asyncio.run(other_agent.collaborate(demo_results))
                    insights.append({
                        "from_agent": other_name,
                        "insight": insight
                    })
            
            # Display insights
            for insight in insights:
                with st.expander(f"Insight from {insight['from_agent']}"):
                    st.write(insight["insight"])
                    
        except Exception as e:
            st.error(f"Error generating insights: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
### About Titans
This demonstration platform showcases the key concepts from the paper "Titans: Learning to Memorize at Test Time".
Each agent demonstrates different aspects of the architecture, from memory mechanisms to scalability analysis.

For more information, check out the [paper](https://arxiv.org/abs/titans) and the [source code](https://github.com/your-repo/titans).
""")
