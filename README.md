# 🛌 Sleep Specialist Chat Assistant

**Author:** Zubair Akbar

A Streamlit-based RAG chatbot for personalized sleep recommendations, combining a FAISS vectorstore with the DeepSeek LLM API.
![Screenshot 1](images/01.png)
![Screenshot 2](images/02.png)


## 🚀 Features

- **Retrieval-Augmented Generation** using FAISS + DeepSeek  
- **Streamlit UI**: simple chat interface with source citations  
- Easy local or cloud deployment  

## 📂 Project Structure

<pre markdown> ```text Sleep_Specialist_Chat_Assistant/ ├── faiss_db/ ├── images/ │ ├── 01.png │ └── 02.png ├── app.py ├── app_local.py ├── create_faiss_db.py ├── extract_pdf.py ├── icd11_full_20250331.xlsx ├── icd11_sleep.py └── Requirements.txt ``` </pre>
## ⚙️ Installation

1. **Clone this repo**  
   ```bash
   git clone https://github.com/<your-username>/Sleep_Specialist_Chat_Assistant.git
   cd Sleep_Specialist_Chat_Assistant
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
pip install -r Requirements.txt
python create_faiss_db.py --input pdfs/ --output faiss_db


DEEPSEEK_API_KEY = "YOUR_API_KEY"
streamlit run app.py

Note PDF data(Books/Research papers) are not included.  