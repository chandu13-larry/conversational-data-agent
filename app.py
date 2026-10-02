import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import re
import io

# 1. Page Configuration
st.set_page_config(page_title="Conversational Data Agent", layout="wide")
st.title("📊 Conversational Data Agent & Analytics Dashboard")

# 2. Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# 3. File Uploader in Sidebar
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"File uploaded successfully! ({len(df)} rows)")

    # Data preview expander
    with st.expander("Preview Uploaded Data"):
        st.dataframe(df.head(10))

    # --- ADVANCED VISUALIZATIONS DASHBOARD ---
    st.write("---")
    st.subheader("📈 Automated Visual Analytics")

    col1, col2 = st.columns(2)

    # Chart 1: Top 5 Impacted Industries
    with col1:
        if "industry" in df.columns and "total_laid_off" in df.columns:
            st.markdown("#### Top 5 Industries by Layoffs")
            industry_data = df.groupby("industry")["total_laid_off"].sum().dropna().nlargest(5)

            fig1, ax1 = plt.subplots(figsize=(6, 4))
            industry_data.plot(kind="bar", color="#4C72B0", ax=ax1)
            ax1.set_ylabel("Total Laid Off")
            ax1.set_xlabel("Industry")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close(fig1)

    # Chart 2: Top 10 Impacted Companies
    with col2:
        if "company" in df.columns and "total_laid_off" in df.columns:
            st.markdown("#### Top 10 Companies by Layoffs")
            company_data = df.groupby("company")["total_laid_off"].sum().dropna().nlargest(10)

            fig2, ax2 = plt.subplots(figsize=(6, 4))
            company_data.plot(kind="barh", color="#C44E52", ax=ax2)
            ax2.set_xlabel("Total Laid Off")
            ax2.set_ylabel("Company")
            ax2.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

    st.write("---")

else:
    st.warning("Please upload a CSV file in the sidebar to get started.")
    st.stop()

# 4. Chat Interface Setup (Upgraded to handle Image rendering)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "image":
            st.image(message["content"])
            if "text" in message:
                st.markdown(message["text"])
        else:
            st.markdown(message["content"])

# 5. Handle User Queries (Dynamic Python Execution for Text & Charts)
if prompt := st.chat_input("Ask a question or request a chart..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})

    # Strict prompt directing Gemini to create either `fig` or `result`
    code_prompt = f"""
You are a senior data analyst. You have a pandas DataFrame `df`.
Dataset columns and types: 
{df.dtypes.to_string()}

User Request: {prompt}

Task:
Write executable Python code to fulfill the user's request.
1. For CHARTS/VISUALIZATIONS: Use `matplotlib.pyplot as plt` to create a figure. YOU MUST assign the final plot to a variable named `fig` (e.g., `fig, ax = plt.subplots()`). Do NOT use `plt.show()`.
2. For TEXT/MATH/TABLE questions: Store the final answer in a variable named `result`.
3. Clean strings or drop NaNs if necessary for calculations.
4. Return ONLY valid Python code enclosed in ```python and ```. No explanations.
"""

    with st.chat_message("assistant"):
        with st.spinner("Writing and executing analytical code..."):
            try:
                # 1. Ask Gemini for the code
                response = model.generate_content(code_prompt)
                raw_text = response.text
                
                # Extract Python block
                code_match = re.search(r"```python\s*(.*?)\s*```", raw_text, re.DOTALL)
                generated_code = code_match.group(1) if code_match else raw_text.strip()

                with st.expander("Show Generated Python Code"):
                    st.code(generated_code, language="python")

                # 2. Execute local code against the dataframe
                local_vars = {"df": df, "pd": pd, "plt": plt}
                exec(generated_code, globals(), local_vars)

                # 3. Detect and display what the AI built (a figure or a result)
                if "fig" in local_vars:
                    # Convert matplotlib figure to image bytes for crash-proof rendering
                    fig = local_vars["fig"]
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)
                    img_bytes = buf.getvalue()
                    
                    st.image(img_bytes)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": img_bytes, 
                        "type": "image", 
                        "text": "Here is your visualization!"
                    })
                    plt.close(fig) # Prevent memory leaks

                elif "result" in local_vars:
                    result = local_vars["result"]
                    st.markdown(str(result))
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": str(result),
                        "type": "text"
                    })
            except Exception as e:
                st.error(f"Error during analysis: {e}")