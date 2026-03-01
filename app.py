import streamlit as st
import requests
import plotly.graph_objects as go
import json

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Titanic Data Analysis",
    page_icon="⚓",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Titanic Dataset Analysis")
st.write("Ask questions about the Titanic dataset in natural language")

with st.sidebar:
    st.header("Dataset Information")
    try:
        response = requests.get(f"{API_URL}/dataset-info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            st.metric("Total Records", f"{info['rows']:,}")
            st.metric("Data Fields", len(info["columns"]))
    except:
        st.warning("API not connected")
    
    st.divider()
    st.subheader("Example Questions")
    st.write("- What percentage of passengers were male?")
    st.write("- Show me a histogram of passenger ages")
    st.write("- What was the average ticket fare?")
    st.write("- How many passengers embarked from each port?")
    
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "chart" in message and message["chart"]:
            try:
                fig = go.Figure(json.loads(message["chart"]))
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"query": prompt},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.write(data["answer"])
                    
                    chart_data = None
                    if data.get("chart"):
                        try:
                            fig = go.Figure(json.loads(data["chart"]))
                            st.plotly_chart(fig, use_container_width=True)
                            chart_data = data["chart"]
                        except Exception as e:
                            st.error(f"Chart error: {str(e)}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["answer"],
                        "chart": chart_data
                    })
                else:
                    error_msg = f"Error: Status {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            except requests.exceptions.ConnectionError:
                error_msg = "Cannot connect to API on port 8000"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
