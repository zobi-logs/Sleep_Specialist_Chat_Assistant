
# Sleep Specialist Chat Assistant

**Author:** Zubair Akbar

A Streamlit-based chatbot for sleep recommendations, using a FAISS vector database and the DeepSeek LLM API.  
Relevant sources are cited with every answer.

## Features

- Chatbot powered by DeepSeek API and RAG (Retrieval-Augmented Generation)
- Sleep questions answered with evidence and source snippets
- Simple Streamlit UI

## Screenshots

![Screenshot 1](images/01.png)  
![Screenshot 2](images/02.png)  




## Project Structure
```
Sleep_Specialist_Chat_Assistant/
|-- faiss_db/ # prebuilt FAISS vectorstore
|-- images/ # UI screenshots
| |-- 01.png
| |-- 02.png
|-- app.py # main Streamlit RAG chatbot
|-- app_local.py # local-only variant (no RAG)
|-- create_faiss_db.py # build the FAISS DB
|-- extract_pdf.py # ingest PDFs into FAISS
|-- icd11_full_20250331.xlsx # source data
|-- icd11_sleep.py # sleep-specific ingestion
|-- Requirements.txt # Python dependencies

```


## Installation & Run

```bash
git clone https://github.com/zobi-logs/Sleep_Specialist_Chat_Assistant.git
cd Sleep_Specialist_Chat_Assistant

python -m venv .venv
.venv\Scripts\activate
pip install -r Requirements.txt

python create_faiss_db.py --input pdfs/ --output faiss_db

# Edit app.py and set your DeepSeek API key:
# DEEPSEEK_API_KEY = "YOUR_API_KEY"

streamlit run app.py

Note: Example PDF/books are not included in this repo.
