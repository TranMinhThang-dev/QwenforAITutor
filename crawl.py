import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Setup Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

global driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def extract_flashcard_information(html_content):
    """
    Extract math content from HTML, converting MathJax elements to LaTeX.
    """
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all script tags with type="math/tex"
    math_scripts = soup.find_all('script', {'type': 'math/tex'})
    
    # Create a dictionary to store LaTeX by ID
    latex_by_id = {}
    
    # Extract the LaTeX content and ID
    for script in math_scripts:
        latex_content = script.string
        id_attr = script.get('id')
        if id_attr:
            # Extract the number from the ID (MathJax-Element-XXX)
            id_num = id_attr.split('-')[-1]
            latex_by_id[id_num] = latex_content
    
    # Extract the question content
    question_div = soup.find('div', {'class': 'mcq-content'})
    if question_div:
        # Extract the question text
        question_text = ""
        for p in question_div.find_all('p'):
            question_text += p.get_text() + "\n"
        
        if question_text == "":
            for span in question_div.find_all('span'):
                question_text += span.get_text() + "\n"
        
        # Replace MathJax references with the corresponding LaTeX
        for span in soup.find_all('span', {'id': re.compile(r'MathJax-Element-\d+-Frame')}):
            id_match = re.search(r'MathJax-Element-(\d+)-Frame', span['id'])
            if id_match:
                id_num = id_match.group(1)
                if id_num in latex_by_id:
                    latex = latex_by_id[id_num]
                    # Mark the LaTeX formula in a way that's easy to recognize
                    replacement = f"$${latex}$$"
                    span.replace_with(replacement)
    
    # Extract options
    options = []
    option_divs = soup.find_all('div', {'class': 'mcq-option-content'})
    for i, div in enumerate(option_divs):
        option_text = div.get_text().strip()
        # Replace MathJax references with the corresponding LaTeX
        for span in div.find_all('span', {'id': re.compile(r'MathJax-Element-\d+-Frame')}):
            id_match = re.search(r'MathJax-Element-(\d+)-Frame', span['id'])
            if id_match:
                id_num = id_match.group(1)
                if id_num in latex_by_id:
                    latex = latex_by_id[id_num]
                    # Mark the LaTeX formula in a way that's easy to recognize
                    replacement = f"$${latex}$$"
                    span.replace_with(replacement)
        options.append(option_text)
    
    # Extract image URL if present
    image_url = None
    img_tag = soup.find('img')
    if img_tag and 'src' in img_tag.attrs:
        image_url = img_tag['src']
    
    # Assemble the result
    result = {
        'question': question_text.strip(),
        'options': options,
        'image_url': image_url
    }
    
    return result

def get_flashcards_selenium(url):
    
    # Find elements using XPath
    front_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'flashcard-content') and contains(@class, 'flashcard-front')]")
    back_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'flashcard-content') and contains(@class, 'flashcard-back')]")
    
    # Extract HTML
    front_html = [card.get_attribute('outerHTML') for card in front_cards]
    back_html = [card.get_attribute('outerHTML') for card in back_cards]
    
    return front_html, back_html

# Usage example
if __name__ == "__main__":
    urls = ["https://khoahoc.vietjack.com/thi-online/de-thi-giua-ki-1-toan-12-canh-dieu-co-dap-an/146534"]


    for url in urls:
        """Extract flashcard content using Selenium with XPath"""
        driver.get(url)
        
        # Wait for page to fully load
        time.sleep(3)
        for i in range(5):
            
            front_cards, back_cards = get_flashcards_selenium(url)
            
            front_extracted_content = extract_flashcard_information(front_cards[0].replace('<div class="flashcard-content flashcard-front">','')[:-6])
            back_extracted_content = extract_flashcard_information(back_cards[0].replace('<div class="flashcard-content flashcard-back">','')[:-6])
            
            # Print the extracted content in a nice format
            print("="*10,"FRONT CARD","="*10)
            print("Question:")
            print(front_extracted_content['question'])
            print("\nOptions:", front_extracted_content['options'])
            print("\nImage URL:")
            print(front_extracted_content['image_url'])
            
            print("="*10,"BACK CARD","="*10)
            print(back_extracted_content['question'])
            
            print(f"Found {len(front_cards)} front cards and {len(back_cards)} back cards")
            
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-default > i.fas.fa-arrow-right"))
            )
            # Navigate up to the button from the icon
            button = button.find_element(By.XPATH, "..")
            button.click()
            print("Button click successfull!!")    
        driver.quit()
            