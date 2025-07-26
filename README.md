# assignment-10min

## How to Use

### 0. Set up environment variables

You must provide a `.env` file with your Hugging Face API token, or the model will not work.

Example `.env`:

```
HUGGINGFACEHUB_API_TOKEN = "your_huggingface_token_here"
```

Replace `your_huggingface_token_here` with your actual token from https://huggingface.co/settings/tokens

---

### 1. Install system dependencies (Windows)

Before running `pip install -r requirements.txt`, you must install Poppler and Tesseract OCR on your system for PDF and image processing to work.

#### Install Poppler

1. Download Poppler for Windows from:
   https://github.com/oschwartz10612/poppler-windows/releases
2. Add `C:\poppler\Library\bin` to your system PATH:
   - Open Start Menu, search Environment Variables → Edit the system environment variables
   - Click Environment Variables
   - Under System Variables, find and select Path → Click Edit
   - Click New and add: `C:\poppler\Library\bin`
   - Click OK to save and exit
3. Restart your terminal/IDE to load the updated PATH

#### Install Tesseract OCR

1. Download and install from:
   https://github.com/UB-Mannheim/tesseract/wiki
2. After installation, make sure `C:\Program Files\Tesseract-OCR\tesseract.exe` is in your system PATH
3. If needed, tell `pytesseract` where to find tesseract in your code

---

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate the vector store (required, run once)

Before running `app.py`, you must run `generate_vector_store.py` once to generate and save the vector store locally. Without this, `app.py` will not work.

```bash
python generate_vector_store.py
```

### 3. Run the FastAPI server

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000/`

### 4. Chat with the bot

Send a POST request to `/chat` with a JSON body:

## Q&A: Key Technical Decisions and Challenges

```
{
  "message": "Your question here"
}
```

Example using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"message": "Hello"}'
```

#### Using FastAPI Interactive Docs

FastAPI provides interactive API documentation at `/docs` (Swagger UI) and `/redoc` (ReDoc).

1. Open your browser and go to `http://127.0.0.1:8000/docs`.
2. Find the `/chat` endpoint in the list.
3. Click on it, then click "Try it out".
4. Enter your message in the `message` field and click "Execute".
5. You will see the response from the API below.

This is a quick way to manually test and explore your API without writing any code.

### 5. Customization

- Add your data to the `data/` folder.
- Update system prompt in `src/config/config.py`.

### 6. Frontend (optional)

If you want to use a web frontend, serve your static files and connect to the `/chat` endpoint.

---

For more details, see the code and comments in `app.py` and the `src/` folder.

---

### 7. Debugging and Logs

---

## Tools, Libraries, and Packages Used

- **FastAPI**: Web API framework for Python
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI
- **LangChain**: Framework for building LLM-powered applications
- **langchain_huggingface**: HuggingFace integration for LangChain
- **langchain_community**: Community integrations for LangChain
- **huggingface_hub**: Access Hugging Face models and datasets
- **faiss-cpu**: Vector database for efficient similarity search
- **sentence-transformers**: Pretrained models for sentence embeddings
- **pdfplumber**: PDF text extraction
- **pdf2image**: Convert PDF pages to images
- **pytesseract**: OCR for extracting text from images
- **python-dotenv**: Load environment variables from .env files

Other internal modules:

- `src/components/`: Data processing, vector DB, LLM model
- `src/utils/`: Logging, helpers, custom exceptions

---

---

---

## Example: Input and Output

After preprocessing the PDF data, you can check the processed data in the `data` folder, file name `book_data.json`.

Below is an example of how the input and output look in the FastAPI docs:

![API Example](img/example_api.png)

**Sample Input (request):**

```json
{
  "message": "অনুপমের বাবা কী করে জীবিকা নির্বাহ করতেন?"
}
```

**Sample Output (response):**

```json
{
  "reply": "অনুপমের বাবা ওকালতি করে জীবিকা নির্বাহ করতেন."
}
```

You can see the full processed data in `data/book_data.json`.

```
assignment-10min/
├── app.py
├── generate_vector_store.py
├── requirements.txt
├── setup.py
├── README.md
├── LICENSE
├── .env
├── template.py
├── data/
│   ├── book_data.json
│   └── HSC26-Bangla1st-Paper.pdf
├── logs/
│   └── log_2025-07-26.log
├── vectore_store/
│   ├── index.faiss
│   └── index.pkl
├── research/
│   └── research.ipynb
├── src/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_prepocessing.py
│   │   ├── llm_model.py
│   │   └── vector_database.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py
│   └── utils/
│       ├── __init__.py
│       ├── custom_exception.py
│       ├── helper.py
│       └── logger.py
└── 10Min_Rag_Application.egg-info/
```

## Q&A: Key Technical Decisions and Challenges

**1. What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?**

- I initially tried standard PDF reading libraries, but they did not provide good results and had formatting issues with the content.
- To overcome this, I used `pdf2image` to convert PDF pages to images, then `pytesseract` for OCR to extract text from images. For tables, I used `pdfplumber` to extract structured data.
- This image-based approach was chosen because the PDF contains both text and tables, and OCR is more robust for Bangla/English mixed content.
- Formatting challenges: OCR can introduce noise, and table extraction requires special handling for specific pages. Standard PDF libraries often fail to preserve layout and structure, especially for complex or scanned documents.

**2. What chunking strategy did you choose (e.g. paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?**

- Used `RecursiveCharacterTextSplitter` with a character limit (`CHUNK_SIZE`) and overlap (`CHUNK_OVERLAP`), splitting on paragraphs, newlines, spaces.
- This strategy ensures chunks are neither too large nor too small, preserving semantic context and improving retrieval relevance.

**3. What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?**

- Used `l3cube-pune/bengali-sentence-similarity-sbert` via `sentence-transformers` and `langchain_huggingface`.
- Chosen for its effectiveness in Bangla semantic similarity tasks; SBERT models capture sentence meaning by mapping text to dense vectors.

**4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?**

- Used FAISS for vector storage and similarity search; queries and chunks are embedded and compared using cosine similarity.
- FAISS is fast and scalable for large vector databases, and cosine similarity is standard for semantic retrieval.

**5. How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?**

- Both queries and chunks are embedded using the same model, ensuring meaningful comparison in vector space.
- If the query is vague or lacks context, retrieval may return less relevant chunks; results depend on embedding quality and chunk granularity.

**6. Do the results seem relevant? If not, what might improve them (e.g. better chunking, better embedding model, larger document)?**

- Right now, Bangla models are not that mature, and I used open-source embedding and LLM models which might not understand Bangla very well. I faced many challenges embedding data because not all models gave appropriate results, so I had to research a lot to find some Bangla embedding models. I think for Bangla language, available models are still developing. Maybe OpenAI or other paid service models might provide better output.
- Improvements: Adjust chunk size/overlap, use a more advanced or paid embedding model, or provide more/better formatted source documents.
