## Automated Book Publication Workflow

### Objective
A system that fetches content from a web URL, applies an AI-driven "spin" to chapters, allows human-in-the-loop editing, and manages version control using ChromaDB.

---

### Task Requirements Fulfilled

| Task Component | Implemented in this Project |
|----------------|-----------------------------|
| 1. Scraping & Screenshot | Using Playwright to scrape and save content plus a full-page screenshot (`chapter1.html`, `chapter1.png`). |
| 2. AI Writing & Review (LLM) | AI spinning and rephrasing using OpenAI LLM (simulating Gemini). Result stored as `chapter1_spun.txt`. |
| 3. Human-in-the-Loop Editing | Gradio UI allows human review and editing of AI output. Final human version stored as `chapter1_human_edited.txt`. |
| 4. Agentic API Flow | Seamless data flow through Python functions and Gradio interface, simulating agent pipeline. |
| 5. Versioning & Consistency | Version management using ChromaDB. Stores original, AI-spun, and human-edited versions for retrieval. |

---

### Core Technologies Used

- Python
- Playwright
- BeautifulSoup4
- OpenAI LLM (GPT-3.5 Turbo)
- Gradio
- ChromaDB
- dotenv

---

### Setup Instructions

1. Clone the repository:

```
git clone https://github.com/deshna0620/automated_book_workflow.git
cd automated_book_workflow
```

2. Create and activate virtual environment (Windows CMD):

```
python -m venv venv
venv\Scripts\activate
```

3. Install requirements:

```
pip install -r requirements.txt
playwright install
```

4. Setup your `.env` file:

```
cp .env.example .env
```

Then fill your real OpenAI API key in `.env`:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

### Run the Gradio App

```
python gradio_app.py
```

Gradio Web UI will launch in your browser.

---

### Generated Output Files

| File | Description |
|------|-------------|
| chapter1.html | Raw scraped HTML |
| chapter1.png | Full-page screenshot |
| chapter1_spun.txt | AI-spun content (LLM output) |
| chapter1_human_edited.txt | Human-edited version |

---

### Versioning

All versions are stored and retrieved from ChromaDB to meet version control requirements.

---

### Demo Video

Watch the full project demo here:  
[Demo Video Link](https://drive.google.com/file/d/1jKarlCSm4AkUTiGXCHXIQHeGri5DDGdP/view?usp=sharing)  

---

### Notes

- `.env` and `venv/` are excluded from the repository via `.gitignore`.
- Demo video file is not included in the repository. The video is shared separately via the above link.

---

### Author

Deshna Jain  
https://github.com/deshna0620
