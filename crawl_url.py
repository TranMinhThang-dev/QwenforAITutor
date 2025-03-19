import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_href_from_div(url):

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the specific div element with class "scroll-slider scroll-off"
        scroll_div = soup.select_one('div.scroll-slider.scroll-off')
        
        # Extract all href attributes from a tags within this element
        hrefs = []
        if scroll_div:
            for a_tag in tqdm(scroll_div.find_all('a'),desc="DIV:", ncols=75):
                href = a_tag.get('href')
                if href:
                    hrefs.append(href)
        
        return hrefs
    else:
        print(f"DIV: Request failed with status code: {response.status_code}")

def get_href_from_ul(url):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the specific ul element
        scroll_box = soup.select_one('ul.list-unstyled.scroll-box.content-table')

        # Extract all href attributes from a tags within this element
        hrefs = []    
        if scroll_box:
            for a_tag in tqdm(scroll_box.find_all('a'), desc="UL: "):
                href = a_tag.get('href')
                if href.startswith("https"):
                    hrefs.append(href)
                    hrefs_from_div = get_href_from_div(href)
                    hrefs.extend(hrefs_from_div[1:])

        print(len(set(hrefs)))
        return hrefs
    else:
        print(f"UL: Request failed with status code: {response.status_code}")
        

urls = [
        "https://khoahoc.vietjack.com/thi-online/2025-moi-de-thi-on-tap-thpt-mon-toan-co-dap-an-de-so-1/145302", # de thi THPT
        
        # Lop 12
        "https://khoahoc.vietjack.com/thi-online/5920-cau-trac-nghiem-tong-hop-mon-toan-2023-co-dap-an/117070", # trac nghiem tong hop lop 12
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-12-canh-dieu-bai-1-tinh-don-dieu-cua-ham-so-co-dap-an/136002", # giai sbt+sgk canh dieu 12
        "https://khoahoc.vietjack.com/thi-online/20-cau-trac-nghiem-toan-12-canh-dieu-bai-1-tinh-don-dieu-cua-ham-so-co-dap-an/146828", # cau trac nghiem canh dieu 12
        "https://khoahoc.vietjack.com/thi-online/20-cau-trac-nghiem-toan-12-ket-noi-tri-thuc-bai-1-tinh-don-dieu-va-cuc-tri-cua-ham-so-co-dap-an/146778", # cau trac nghiem ket noi tri thuc 12
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-12-kntt-bai-1-tinh-don-dieu-va-cuc-tri-cua-ham-so-co-dap-an/135349", # giai sbt+sgk ket noi tri thuc 12
        "https://khoahoc.vietjack.com/thi-online/20-cau-trac-nghiem-toan-12-chan-troi-sang-tao-bai-1-tinh-don-dieu-va-cuc-tri-cua-ham-so-co-dap-an/146914", # cau trac nghiem chan troi sang tao 12
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-12-ctst-bai-1-tinh-don-dieu-va-cuc-tri-cua-ham-so-co-dap-an/135915",# giai sbt chan troi sang tao 12
        "https://khoahoc.vietjack.com/thi-online/53-cau-bai-tap-ve-tinh-don-dieu-cua-ham-so-co-loi-giai/11704", # cau trac nghiem chuong trinh cu 12
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-12-bai-2-cuc-tri-cua-ham-so/33681", # giai sbt+sgk chuong trinh cu 12
        
        # Lop 11
        "https://khoahoc.vietjack.com/thi-online/bai-tap-hinh-hoc-khong-gian-lop-11-co-ban-nang-cao-co-loi-giai/12411", # de tong hop
        "https://khoahoc.vietjack.com/thi-online/38-cau-trac-nghiem-toan-11-ket-noi-tri-thuc-logarit-co-dap-an/161013",# de tong hop kttt
        "https://khoahoc.vietjack.com/thi-online/10-bai-tap-tinhsbien-co-hop-cua-hai-bien-co-bat-ki-bang-cach-su-dung-cong-thuc-cong-xac/154718", # de tong hop ctst
        "https://khoahoc.vietjack.com/thi-online/12-cau-trac-nghiem-toan-11-ket-noi-tri-thuc-gia-tri-luong-giac-cua-goc-luong-giac-co-dap-an/131995", # cau trac nghiem ket noi tri thuc 11
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-11-kntt-bai-1-gia-tri-luong-giac-cua-goc-luong-giac-co-dap-an/123227", # giai sbt+sgk ket noi tri thuc 11
        "https://khoahoc.vietjack.com/thi-online/10-bai-tap-bai-toan-thuc-tien-lien-qsssuan-den-gia-tri-luong-giac-cua-goc-luong-giac-co-loi-giai/154739", # cau trac nghiem canh dieu
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-11-canh-dieu-goc-luong-giac-gia-tri-luong-giac-cua-goc-luong-giac-co-dap-an/123416", # giai sbt canh dieu
        "https://khoahoc.vietjack.com/thi-online/10-bai-tap-biseu-dien-goc-luong-giac-tren-duong-tron-luong-giac-co-loi-giai/154507", # cau trac nghiem ctst
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-11-ctst-bai-1-goc-luong-giac-co-dap-an/124334", # giai bai tap ctst
        
        # Lop 10
        "https://khoahoc.vietjack.com/thi-online/13-cau-trac-nghiem-tich-cua-vecto-voi-mot-so-co-dap-an-thong-hieu/63257",# de tong hop
        "https://khoahoc.vietjack.com/thi-online/12-bai-tap-ung-dung-cua-ham-so-bac-hai-de-giai-bai-toan-thuc-te-co-loi-giai/100589", # de tong hop kntt
        "https://khoahoc.vietjack.com/thi-online/10-bai-tap-cach-xet-tsinh-dung-sai-cua-menh-de-co-loi-giai/154232", # de tong hop canh dieu
        "https://khoahoc.vietjack.com/thi-online/16-cau-trac-nghiem-toan-10-ket-noi-tri-thuc-menh-de-co-dap-an/93522", # cau tn kntt
        "https://khoahoc.vietjack.com/thi-online/bai-tap-menh-de-co-dap-an/80489", # giai bt kntt
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-10-canh-dieu-menh-de-toan-hoc-co-dap-an/88895",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-menh-de-toan-hoc-co-dap-an/78395",
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-10-chan-troi-sang-tao-menh-de-co-dap-an/93380",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-menh-de-co-dap-an-1/82703",
        "https://khoahoc.vietjack.com/thi-online/28-cau-trac-nghiem-menh-de-co-dap-an/50024",
        "https://khoahoc.vietjack.com/thi-online/toan-10-bai-1-menh-de-co-dap-an/24310"
        
        # Lop 9
        ]
hrefs = []
for url in urls:
    hrefs.extend(get_href_from_ul(url))
    
hrefs = list(set(hrefs))
print("number of url: ",len(hrefs))

