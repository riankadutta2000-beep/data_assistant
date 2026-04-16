import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile, os


# Insight function
def generate_insight(result, title):
    if isinstance(result, pd.Series):
        top = result.idxmax()
        return f"{top} is performing best in {title}."
    return "No insight available."

# Assistant logic
def data_assistant(query, df):
    query = query.lower()

    if "product" in query:
        result = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
        st.write(result)

        fig, ax = plt.subplots()
        result.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        st.success(generate_insight(result, "Product Revenue"))

    elif "region" in query:
        result = df.groupby("Region")["Revenue"].sum()
        st.write(result)

        fig, ax = plt.subplots()
        result.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        st.success(generate_insight(result, "Region Revenue"))

    elif "trend" in query or "monthly" in query:
        result = df.groupby(df["Date"].dt.month)["Revenue"].sum()
        st.write(result)

        fig, ax = plt.subplots()
        result.plot(kind="line", ax=ax)
        st.pyplot(fig)

    else:
        st.warning("Try asking about product, region, or trend.")

# UI
st.title("💬 AI Data Assistant (Free Version)")

query = st.text_input("Ask your question:")



uploaded_files = st.file_uploader(
    "Upload Chat File(s)",
    type=["csv"],
    accept_multiple_files=False,
    help="Select one or more Zoom/Webinar chat export files (.csv)"
)

if uploaded_files:
    #st.success(f"✅ {len(uploaded_files)} file(s) uploaded: {', '.join([f.name for f in uploaded_files])}")
    
    
    if st.button("🚀 Process Files", type="primary"):
        
        with tempfile.TemporaryDirectory() as tmpdir:
             
            file_path = os.path.join(tmpdir, uploaded_files.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_files.read())
            with open(file_path, "rb+") as f:
                # Load data
                if query:
                    df = pd.read_csv(file_path)
                    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
                    data_assistant(query, df)
                    
    

    
# from pyngrok import ngrok

# ngrok.set_auth_token("3COXNHvdVu2OwBPx0Sb9rzVLRef_rqoW8JQDnhj6bUFfCicm")

# public_url = ngrok.connect(8501)
