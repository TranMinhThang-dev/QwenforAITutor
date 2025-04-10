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
from tqdm import tqdm
# from utils import mathml_to_latex
from py_asciimath.translator.translator import MathML2Tex

# Setup Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
import json

global driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

mathml2tex = MathML2Tex()


def extract_flashcard_information(html_content):
    """
    Extract math content from HTML, converting MathJax elements to LaTeX.
    """
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract image URL if present
    img_tag = soup.find('img')
    if img_tag:
        return None
        
    # Find all script tags with type="math/tex"
    math_scripts = soup.find_all('script', {'type': 'math/mml'})
    if math_scripts == []:
        math_scripts = soup.find_all('script', {'type': 'math/tex'})
    
    # if have sub_tag but not have math_scrip => return        
    sub_tags = soup.find_all('sub')
    if len(sub_tags)>0 and len(math_scripts) == 0:
        return None
    
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
        
        # Replace MathJax references with the corresponding LaTeX
        for span in soup.find_all('span', {'id': re.compile(r'MathJax-Element-\d+-Frame')}):
            id_match = re.search(r'MathJax-Element-(\d+)-Frame', span['id'])
            if id_match:
                id_num = id_match.group(1)
                if id_num in latex_by_id:
                    # latex = mathml2tex.translate(latex_by_id[id_num]) 
                    try:
                        if 'xmlns="http://www.w3.org/1998/Math/MathML"' in latex_by_id[id_num]:
                            latex = mathml2tex.translate(latex_by_id[id_num]) 
                        else:
                            latex = latex_by_id[id_num]
                    except:
                        return None
                    # Mark the LaTeX formula in a way that's easy to recognize
                    replacement = f"${latex}$"
                    span.replace_with(replacement)
                    
        for p in question_div.find_all('p'):
            question_text += p.get_text() + "\n"
        
        if question_text == "":
            for span in question_div.find_all('span'):
                question_text += span.get_text() + "\n"
    
    # Extract options
    options = []
    option_divs = soup.find_all('div', {'class': 'mcq-option-content'})
    for i, div in enumerate(option_divs):
        # Replace MathJax references with the corresponding LaTeX
        for span in div.find_all('span', {'id': re.compile(r'MathJax-Element-\d+-Frame')}):
            id_match = re.search(r'MathJax-Element-(\d+)-Frame', span['id'])
            if id_match:
                id_num = id_match.group(1)
                if id_num in latex_by_id:
                    # latex = mathml2tex.translate(latex_by_id[id_num]) 
                    try:
                        if 'xmlns="http://www.w3.org/1998/Math/MathML"' in latex_by_id[id_num]:
                            latex = mathml2tex.translate(latex_by_id[id_num]) 
                        else:
                            latex = latex_by_id[id_num]
                    except:
                        return None
                    # Mark the LaTeX formula in a way that's easy to recognize
                    replacement = f"${latex}$"
                    span.replace_with(replacement)
        option_text = div.get_text().strip()
        options.append(option_text)
    
    # Assemble the result
    result = {
        'question': question_text.strip(),
        'options':options
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
    with open("urls.txt",'r') as f:
        urls = f.readlines()
        
    idx = 1365
    cnt = 800
    for url in tqdm(urls[800:], desc="url",ncols=75):
        """Extract flashcard content using Selenium with XPath"""
        driver.get(url)
        cnt+=1
        with open("count.txt",'a',encoding='utf-8') as f:
            f.write(f"{cnt}\n")
        # Wait for page to fully load
        time.sleep(2)
        for i in range(5):
            try:
                quizz = {}
                front_cards, back_cards = get_flashcards_selenium(url)
                front_extracted_content = extract_flashcard_information(front_cards[0].replace('<div class="flashcard-content flashcard-front">','')[:-6])
                back_extracted_content = extract_flashcard_information(back_cards[0].replace('<div class="flashcard-content flashcard-back">','')[:-6])
                
                if front_extracted_content is None or back_extracted_content is None or front_extracted_content['question'] == "" or back_extracted_content['question'] == '':
                    with open("error_url.txt",'a',encoding='utf-8') as f:
                        f.write(f"{url}\n")
                    continue
                
                quizz['id'] = idx
                quizz['url'] = url
                quizz["question"] = front_extracted_content['question']
                quizz['options'] = front_extracted_content['options']
                quizz['answer'] = back_extracted_content['question']
                idx += 1
                
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-default > i.fas.fa-arrow-right"))
                )
                # Navigate up to the button from the icon
                button = button.find_element(By.XPATH, "..")
                button.click()
                # print("Button click successfull!!") 

                with open("vietjack_latex_data_2.json", 'a', encoding='utf-8') as f:
                    json.dump(quizz, f, indent=4, ensure_ascii=False)
                    f.write(",\n")
                    
                with open("math_2.tex", 'a', encoding='utf-8') as f:
                    f.write(f"========================================================================\n\n")
                    f.write(f"{url}\n\n")
                    f.write("\\textbf{{QUESTION}}\n\n")
                    f.write(quizz["question"] + "\n\n")
                    f.write("\\textbf{{ANSWER}}\n\n")
                    f.write(quizz["answer"] + "\n\n")

            except Exception as e:
                print(f"\nError when handling url: {url} and flashcard {i}")
    driver.quit()