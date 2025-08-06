# 🛌 Sleep Specialist Chat Assistant

**Author:** Zubair Akbar

A Streamlit-based RAG chatbot for personalized sleep recommendations, combining a FAISS vectorstore with the DeepSeek LLM API.

<img src="./images/01.png" alt="Screenshot 1" width="300"/>  
<img src="./images/02.png" alt="Screenshot 2" width="300"/>

## 🚀 Features

- **Retrieval-Augmented Generation** using FAISS + DeepSeek  
- **Streamlit UI**: simple chat interface with source citations  
- Easy local or cloud deployment  

## 📂 Project Structure

Sleep_Specialist_Chat_Assistant/
├── faiss_db/ # prebuilt FAISS vectorstore
├── images/ # UI screenshots
│ ├── 01.png
│ └── 02.png
├── app.py # main Streamlit RAG chatbot
├── app_local.py # local‐only variant (no RAG)
├── create_faiss_db.py # script to build your FAISS db
├── extract_pdf.py # PDF ingestion into FAISS
├── icd11_full_20250331.xlsx # source data
├── icd11_sleep.py # sleep‐specific ingestion
└── Requirements.txt # Python dependencies
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