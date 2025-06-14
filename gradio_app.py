import gradio as gr
from playwright.sync_api import sync_playwright
import openai
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import chromadb

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize ChromaDB
client = chromadb.Client()
collection = client.create_collection("book_versions")

def scrape_and_extract_text():
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        with open('chapter1.html', 'w', encoding='utf-8') as f:
            f.write(content)
        page.screenshot(path='chapter1.png', full_page=True)
        browser.close()
    # Extract clean text only
    soup = BeautifulSoup(content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = "\n".join([p.get_text() for p in paragraphs])
    return text

def ai_spin():
    with open('chapter1.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = "\n".join([p.get_text() for p in soup.find_all('p')])
    prompt = f"Spin and rephrase this content for clarity and simplicity:\n\n{plain_text[:3000]}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        spun_content = response['choices'][0]['message']['content']
    except:
        with open('chapter1_spun.txt', 'r', encoding='utf-8') as f:
            spun_content = f.read()
    with open('chapter1_spun.txt', 'w', encoding='utf-8') as f:
        f.write(spun_content)
    collection.add(documents=[spun_content], metadatas=[{"version": "ai_spun"}], ids=["v2_ai_spun"])
    return spun_content

def human_edit(user_text):
    with open('chapter1_human_edited.txt', 'w', encoding='utf-8') as f:
        f.write(user_text)
    collection.add(documents=[user_text], metadatas=[{"version": "human_edited"}], ids=["v3_human_edit"])
    return "Human-edited version saved in ChromaDB."

def view_all_versions():
    result = collection.get(include=["documents", "metadatas"])
    if result and result['documents']:
        versions = ""
        for idx, doc in enumerate(result['documents']):
            ver = result['metadatas'][idx]['version']
            versions += f"Version: {ver}\n\nContent:\n{doc}\n\n{'-'*50}\n\n"
        return versions
    return "No data available in ChromaDB."

with gr.Blocks() as demo:
    gr.Markdown("""
    # Automated Book Publication Workflow
    **Objective:** A simple automated system for scraping, AI rewriting, human editing, and version storage using ChromaDB.
    ---
    """)

    with gr.Tab("1. Scrape & Extract"):
        scrape_btn = gr.Button("Scrape and Extract Chapter Text")
        scrape_output = gr.Textbox(label="Extracted Chapter Text (Preview)", lines=12, interactive=False)
        scrape_btn.click(scrape_and_extract_text, outputs=scrape_output)

    with gr.Tab("2. AI Spin (LLM)"):
        ai_spin_btn = gr.Button("Generate AI-Spin Version")
        ai_output = gr.Textbox(label="AI-Spun Chapter Text", lines=12, interactive=False)
        ai_spin_btn.click(ai_spin, outputs=ai_output)

    with gr.Tab("3. Human Editing"):
        with gr.Row():
            human_input = gr.Textbox(label="Edit AI-Spun Text Below", lines=12)
            save_btn = gr.Button("Save Human Edited Text")
        human_msg = gr.Textbox(label="Status", interactive=False)
        save_btn.click(human_edit, inputs=human_input, outputs=human_msg)

    with gr.Tab("4. View All ChromaDB Versions"):
        view_btn = gr.Button("Show All Stored Versions")
        view_output = gr.Textbox(label="Stored Versions in ChromaDB", lines=20, interactive=False)
        view_btn.click(view_all_versions, outputs=view_output)

demo.launch()