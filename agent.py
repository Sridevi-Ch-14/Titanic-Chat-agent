import os
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import json

# Load Titanic dataset
def load_titanic_data():
    """Load the Titanic dataset from seaborn"""
    df = sns.load_dataset('titanic')
    return df

# Initialize the dataset globally
titanic_df = load_titanic_data()

# Custom prompt prefix to guide the agent
AGENT_PREFIX = """
You are a data analysis assistant for the Titanic dataset.
Answer questions clearly and concisely using the dataframe.
Provide numerical answers with appropriate precision.
Available columns: {columns}
"""

def create_agent():
    """Initialize the LangChain Pandas DataFrame agent"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = create_pandas_dataframe_agent(
        llm,
        titanic_df,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        allow_dangerous_code=True,
        prefix=AGENT_PREFIX.format(columns=list(titanic_df.columns))
    )
    
    return agent

def generate_chart(query: str, df: pd.DataFrame):
    """Generate Plotly charts based on query keywords"""
    query_lower = query.lower()
    
    # Histogram of ages
    if 'histogram' in query_lower and 'age' in query_lower:
        fig = px.histogram(df, x='age', nbins=30, title='Distribution of Passenger Ages')
        fig.update_layout(xaxis_title='Age', yaxis_title='Count')
        return fig.to_json()
    
    # Bar chart for embarkation ports
    if 'embark' in query_lower or 'port' in query_lower:
        embark_counts = df['embark_town'].value_counts()
        fig = px.bar(x=embark_counts.index, y=embark_counts.values, 
                     title='Passengers by Embarkation Port',
                     labels={'x': 'Port', 'y': 'Number of Passengers'})
        return fig.to_json()
    
    # Survival rate by class
    if 'survival' in query_lower and 'class' in query_lower:
        survival_by_class = df.groupby('pclass')['survived'].mean() * 100
        fig = px.bar(x=survival_by_class.index, y=survival_by_class.values,
                     title='Survival Rate by Passenger Class',
                     labels={'x': 'Class', 'y': 'Survival Rate (%)'})
        return fig.to_json()
    
    return None

def process_query(query: str):
    """Process user query and return response with optional chart"""
    query_lower = query.lower()
    
    # Check if query requires visualization
    viz_keywords = ['histogram', 'chart', 'plot', 'show', 'visualize', 'graph', 'distribution']
    needs_viz = any(keyword in query_lower for keyword in viz_keywords)
    
    if needs_viz:
        # Generate chart directly
        chart_json = generate_chart(query, titanic_df)
        if chart_json:
            return {
                "answer": "Here's the visualization you requested:",
                "chart": chart_json,
                "type": "chart"
            }
    
    # For text-based queries, use the agent
    try:
        agent = create_agent()
        
        # Enhance query for better responses
        enhanced_query = query
        if 'percentage' in query_lower or 'percent' in query_lower:
            enhanced_query += " (provide the answer as a percentage with one decimal place)"
        elif 'average' in query_lower or 'mean' in query_lower:
            enhanced_query += " (provide the numerical answer rounded to 2 decimal places)"
        
        response = agent.invoke(enhanced_query)
        
        # Extract the answer from agent response
        if isinstance(response, dict) and 'output' in response:
            answer = response['output']
        else:
            answer = str(response)
        
        # Check if response suggests a chart
        if needs_viz and not generate_chart(query, titanic_df):
            return {
                "answer": answer,
                "chart": None,
                "type": "text"
            }
        
        return {
            "answer": answer,
            "chart": None,
            "type": "text"
        }
        
    except Exception as e:
        return {
            "answer": f"Error processing query: {str(e)}",
            "chart": None,
            "type": "error"
        }

def get_dataset_info():
    """Return basic information about the dataset"""
    return {
        "rows": len(titanic_df),
        "columns": list(titanic_df.columns),
        "shape": titanic_df.shape
    }
