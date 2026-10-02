```markdown
# 📊 Conversational Data Agent & Analytics Dashboard

An interactive, AI-powered data analytics web application built with **Streamlit** and the **Google Gemini API**. Upload any tabular dataset (CSV) to instantly generate automated summary visualizations and interact with a conversational agent capable of writing and executing Python code on the fly to produce ad-hoc calculations, aggregations, and custom visual charts.

---

## 🚀 Live Demo

- **Application URL:** [conversational-data-agent.streamlit.app](https://conversational-data-agent-k3toncpvrnngecc2nokgk5.streamlit.app)
- **Repository:** `chandu13-larry/conversational-data-agent`

---

## ✨ Features

- **Instant Exploratory Dashboards:** Automatically aggregates and generates visual insights (e.g., industry-level breakdowns, company distributions) immediately upon dataset upload.
- **Natural Language Data Querying:** Ask complex data questions in plain English—the agent parses the schema, writes syntactically correct Python/Pandas logic, and executes it in real-time.
- **Dynamic Data Visualizations:** Generates custom Matplotlib figures on demand, rendering them directly in the chat stream via crash-proof byte-stream conversion.
- **Code Transparency:** An expandable code block allows users to inspect the exact Python code generated and executed by the AI.
- **Production-Ready & Secure:** Implements strict secrets management (`st.secrets`) to keep API credentials secure in deployment.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Large Language Model:** [Google Gemini API](https://ai.google.dev/) (`google-generativeai`)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **Data Visualization:** [Matplotlib](https://matplotlib.org/)
- **Deployment:** Streamlit Cloud

---

## 📁 Project Structure

```text
conversational-data-agent/
│
├── app.py                # Main Streamlit application and agent execution logic
├── requirements.txt      # Core Python dependencies
├── README.md             # Project documentation
└── .streamlit/
    └── secrets.toml      # Local secrets (API keys - excluded from Git)

```

---

## ⚙️ Local Setup and Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/chandu13-larry/conversational-data-agent.git](https://github.com/chandu13-larry/conversational-data-agent.git)
cd conversational-data-agent

```

### 2. Set Up a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Your API Key

Create a `.streamlit/secrets.toml` file in the root directory:

```toml
GEMINI_API_KEY = "your_actual_google_gemini_api_key_here"

```

### 5. Run the Application

```bash
streamlit run app.py

```

---

## ☁️ Deployment to Streamlit Cloud

1. Push your repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select **Deploy an app**, point to your repository and `app.py`.
4. Under **Advanced Settings > Secrets**, configure your API key in TOML format:
```toml
GEMINI_API_KEY = "your_api_key_here"

```


5. Click **Deploy**.

---

## 💬 Example Queries

Once your CSV is uploaded, try prompts such as:

* *"Show the top 5 industries with the highest layoff counts in a horizontal bar chart."*
* *"What is the median number of employees affected across all records?"*
* *"Create a pie chart showing the distribution of funding stages."*
* *"Plot a time series of layoffs per month over the past two years."*

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

```

```
