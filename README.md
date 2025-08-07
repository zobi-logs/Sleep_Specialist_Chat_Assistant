Sleep_Specialist_Chat_Assistant/>
ÃÄÄ faiss_db/                    # prebuilt FAISS vectorstore
ÃÄÄ images/                      # UI screenshots
|   ÃÄÄ 01.png
|   ÀÄÄ 02.png
ÃÄÄ app.py                       # main Streamlit RAG chatbot
ÃÄÄ app_local.py                 # local-only variant (no RAG)
ÃÄÄ create_faiss_db.py           # build the FAISS DB
ÃÄÄ extract_pdf.py               # ingest PDFs into FAISS
ÃÄÄ icd11_full_20250331.xlsx     # source data
ÃÄÄ icd11_sleep.py               # sleep-specific ingestion
ÀÄÄ Requirements.txt             # Python dependencies
```

## ?? Installation

1. **Clone this repo**  

```bash
git clone https://github.com/zobi-logs/Sleep_Specialist_Chat_Assistant.git
cd Sleep_Specialist_Chat_Assistant
```


```bash
python -m venv .venv
REM Linux/macOS:
source .venv/bin/activate
REM Windows:
.venv\Scripts\activate
```

3. **Install dependencies**  

```bash
pip install -r Requirements.txt
```

4. **Build (or load) your FAISS database**  

```bash
python create_faiss_db.py --input pdfs/ --output faiss_db
```

5. **Set your DeepSeek API key**  
In `app.py`, replace:
```python
DEEPSEEK_API_KEY = "^<YOUR_API_KEY^>" 
```

## ?? Run

```bash
streamlit run app.py
```

> **Note:** PDF data (books/research papers) are not included in this repository.

