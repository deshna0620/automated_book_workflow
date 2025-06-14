from playwright.sync_api import sync_playwright
import openai
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import chromadb
from chromadb.utils import embedding_functions

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize ChromaDB
client = chromadb.Client()
collection = client.create_collection("book_versions")

def scrape_and_screenshot(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        content = page.content()
        with open('chapter1.html', 'w', encoding='utf-8') as f:
            f.write(content)

        page.screenshot(path='chapter1.png', full_page=True)
        browser.close()
    
    return content

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = "\n".join([para.get_text() for para in paragraphs])
    return text

def ai_spin(content):
    prompt = f"Spin and rephrase this content for clarity and simplicity:\n\n{content[:3000]}"
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
    
    return spun_content

def human_review(ai_text):
    print("\n--- AI SPUN TEXT ---\n")
    print(ai_text)
    print("\n--- Human-in-the-Loop Editing ---\n")
    choice = input("Do you want to edit this text? (y/n): ")

    if choice.lower() == 'y':
        print("Type your edited version below. End input with a blank line:")
        lines = []
        while True:
            line = input()
            if line == '':
                break
            lines.append(line)
        human_text = "\n".join(lines)
    else:
        human_text = ai_text

    with open('chapter1_human_edited.txt', 'w', encoding='utf-8') as f:
        f.write(human_text)

    return human_text

def save_to_chromadb(doc_id, content, version_name):
    collection.add(
        documents=[content],
        metadatas=[{"version": version_name}],
        ids=[doc_id]
    )

def retrieve_latest_version():
    result = collection.get(include=["documents", "metadatas"])
    if result and result['documents']:
        latest_doc = result['documents'][-1]
        latest_meta = result['metadatas'][-1]
        print("\n--- Latest Version Retrieved from ChromaDB ---\n")
        print(f"Version: {latest_meta['version']}")
        print(f"Content:\n{latest_doc}")

if __name__ == "__main__":
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    
    html_content = scrape_and_screenshot(url)
    plain_text = extract_text_from_html(html_content)
    ai_spun_text = ai_spin(plain_text)
    human_version = human_review(ai_spun_text)

    # Save to ChromaDB
    save_to_chromadb("v1_original", plain_text, "original")
    save_to_chromadb("v2_ai_spun", ai_spun_text, "ai_spun")
    save_to_chromadb("v3_human", human_version, "human_edited")

    # Retrieve latest version for verification
    retrieve_latest_version()

    print("\nChromaDB Versioning Complete.")