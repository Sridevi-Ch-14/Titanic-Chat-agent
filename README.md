# 🚢 Titanic Dataset Chat Agent

A conversational AI application that allows users to ask natural language questions about the Titanic dataset and receive both text-based answers and interactive data visualizations.

## 🏗️ Architecture

- **Backend**: FastAPI server handling chat requests
- **Agent**: LangChain Pandas DataFrame Agent for intelligent query processing
- **Frontend**: Streamlit chat interface
- **Visualizations**: Plotly for interactive charts
- **LLM**: OpenAI GPT-3.5-turbo (configurable)

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (or AWS credentials for Bedrock)
- pip package manager

## 🚀 Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd "c:\Users\Surya\Documents\Sridevi\Projects\Titanic project-internshala"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Note**: Get your OpenAI API key from https://platform.openai.com/api-keys

## 🎯 Running the Application

You need to run both the FastAPI backend and Streamlit frontend simultaneously.

### Option 1: Using Two Terminal Windows

**Terminal 1 - Start FastAPI Backend:**
```bash
python api.py
```
The API will start on `http://localhost:8000`

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run app.py
```
The Streamlit app will open in your browser at `http://localhost:8501`

### Option 2: Using Background Process (Windows)

```bash
start python api.py
streamlit run app.py
```

## 📊 Testing the Application

Once both servers are running, try these example queries in the Streamlit chat interface:

### Text-Based Queries:
1. **"What percentage of passengers were male on the Titanic?"**
   - Expected: Text response with percentage (e.g., "65.2% of passengers were male")

2. **"What was the average ticket fare?"**
   - Expected: Text response with the average fare value

3. **"How many passengers survived?"**
   - Expected: Text response with count

### Visualization Queries:
1. **"Show me a histogram of passenger ages"**
   - Expected: Interactive histogram chart showing age distribution

2. **"How many passengers embarked from each port?"**
   - Expected: Bar chart showing passenger counts by embarkation port

3. **"Show me survival rate by class"**
   - Expected: Bar chart showing survival rates for each passenger class

## 📁 Project Structure

```
Titanic project-internshala/
├── agent.py              # LangChain agent logic and chart generation
├── api.py                # FastAPI backend server
├── app.py                # Streamlit frontend application
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create from .env.example)
├── .env.example          # Example environment configuration
└── README.md             # This file
```

## 🔧 Configuration

### Using Different LLM Providers

**Amazon Bedrock (Claude):**

1. Install additional dependency:
```bash
pip install langchain-aws
```

2. Update `agent.py`:
```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="us-east-1"
)
```

3. Configure AWS credentials in `.env`:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### Changing API Port

Edit `api.py` (last line):
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

And update `app.py`:
```python
API_URL = "http://localhost:8000"  # Update port here
```

## 🐛 Troubleshooting

### Issue: "Could not connect to API"
- **Solution**: Ensure FastAPI server is running on port 8000
- Check: `http://localhost:8000` should show API status

### Issue: "OpenAI API key not found"
- **Solution**: Verify `.env` file exists and contains valid `OPENAI_API_KEY`
- Restart the FastAPI server after updating `.env`

### Issue: Charts not displaying
- **Solution**: Check browser console for errors
- Ensure Plotly is installed: `pip install plotly`

### Issue: Agent errors or timeouts
- **Solution**: Check OpenAI API key validity and account credits
- Increase timeout in `app.py` (line with `timeout=30`)

## 📝 API Documentation

Once the FastAPI server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Endpoints:

**GET /** - Health check
```json
{"status": "Titanic Chat Agent API is running"}
```

**GET /dataset-info** - Get dataset information
```json
{
  "rows": 891,
  "columns": ["survived", "pclass", "sex", ...],
  "shape": [891, 15]
}
```

**POST /chat** - Process chat query
```json
Request:
{
  "query": "What percentage of passengers were male?"
}

Response:
{
  "answer": "65.2% of passengers were male",
  "chart": null,
  "type": "text"
}
```

## 🎨 Features

- ✅ Natural language query processing
- ✅ Intelligent text and visualization responses
- ✅ Interactive Plotly charts
- ✅ Persistent chat history
- ✅ Clean, modern UI
- ✅ Error handling and validation
- ✅ RESTful API architecture

## 🔒 Security Notes

- Never commit `.env` file to version control
- Keep API keys secure and rotate regularly
- Use environment variables for all sensitive data
- The agent uses `allow_dangerous_code=True` for pandas operations - use only with trusted queries

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Built with ❤️ using LangChain, FastAPI, and Streamlit**
