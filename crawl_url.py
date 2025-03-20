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
            # for a_tag in tqdm(scroll_div.find_all('a'),desc="DIV:", ncols=75):
            for a_tag in scroll_div.find_all('a'):
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
        else:
            # Find the specific div element with class "scroll-slider scroll-off"
            scroll_div = soup.select_one('div.scroll-on')
            
            if scroll_div:
                for a_tag in tqdm(scroll_div.find_all('a'),desc="DIV:", ncols=75):
                    href = a_tag.get('href')
                    if href:
                        hrefs.append(href)
            
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
        "https://khoahoc.vietjack.com/thi-online/bo-5-de-thi-giua-ki-2-toan-9-ket-noi-tri-thuc-co-dap-an/163254",# de tong hop
        "https://khoahoc.vietjack.com/thi-online/trac-nghiem-chuyen-de-toan-9-chuyen-de-5-cac-bai-toan-thuc-te-giai-bang-cach-lap-phuong-trinh-va-he/103993", # de tong hop 
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-9-ket-noi-tri-thuc-bai-1-khai-niem-phuong-trinh-va-he-hai-phuong-trinh-bac-n/146600", # hoc truc tuyen kntt
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-9-kntt-bai-1-khai-niem-phuong-trinh-va-he-phuong-trinh-bac-nhat-hai-an-co-dap-an/134219",
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-9-canh-dieu-bai-1-phuong-trinh-quy-ve-phuong-trinh-bac-nhat-mot-an-co-dap-an/146695",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-9-cd-bai-1-phuong-trinh-quy-ve-phuong-trinh-bac-nhat-mot-an-co-dap-an/134939",
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-9-chan-troi-sang-tao-bai-1-phuong-trinh-quy-ve-phuong-trinh-bac-nhat-mot-an/147022",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-9-ctst-bai-1-phuong-trinh-quy-ve-phuong-trinh-bac-nhat-mot-an-co-dap-an/134321",
        "https://khoahoc.vietjack.com/thi-online/23-cau-trac-nghiem-toan-9-bai-1-can-thuc-bac-hai-co-dap-an/46276",
        "https://khoahoc.vietjack.com/thi-online/giai-bai-tap-sgk-toan-9-tap-1-hay-nhat-bai-1-can-bac-hai/45401",
        
        # Lop 8
        "https://khoahoc.vietjack.com/thi-online/cach-tim-mau-thuc-chung-cuc-hay-nhanh-nhat/49660",
        "https://khoahoc.vietjack.com/thi-online/9-bai-tap-bai-toan-thuc-tie9n-lien-quan-den-phan-thuc-dai-so-co-loi-giai/133140",
        "https://khoahoc.vietjack.com/thi-online/10-bai-tasp-bai-toan-thuc-tien-gan-voi-viec-van-dung-dinh-li-thales-co-loi-giai/153103", # de chung
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-8-ket-noi-tri-thuc-bai-1-don-thuc-co-dap-an/126580",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-8-kntt-bai-1-don-thuc-co-dap-an/119327",
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-8-canh-dieu-bai-1-don-thuc-nhieu-bien-da-thuc-nhieu-bien-co-dap-an/126640",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-8-canh-dieu-bai-1-don-thuc-nhieu-bien-da-thuc-nhieu-bien-co-dap-an/119372",
        "https://khoahoc.vietjack.com/thi-online/15-cau-trac-nghiem-toan-8-chan-troi-sang-tao-bai-1-don-thuc-va-da-thuc-nhieu-bien-co-dap-an/126766",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-8-ctst-bai-1-don-thuc-va-da-thuc-nhieu-bien-co-dap-an/119352",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-nhan-don-thuc-voi-da-thuc-co-loi-giai-chi-tiet/47868",
        "https://khoahoc.vietjack.com/thi-online/cac-dang-bai-tap-toan-8-chuong-2-da-giac-dien-tich-da-giac-co-dap-an/60298"
        
        # Lop 7
        "https://khoahoc.vietjack.com/thi-online/bo-5-de-thi-giua-ki-2-toan-7-canh-dieu-cau-truc-moi-co-dap-an/163297",
        "https://khoahoc.vietjack.com/thi-online/12-bai-tap-mot-so-bai-toan-thuc-te-lien-quan-dai-luong-ti-le-nghich-co-loi-giai/100960",
        "https://khoahoc.vietjack.com/thi-online/de-kiem-tra-giua-hoc-ki-2-toan-lop-7-ctst-co-dap-an/115992", # de tong hop
        "https://khoahoc.vietjack.com/thi-online/bai-tap-toan-7-kntt-bai-1-tap-hop-cac-so-huu-ti-co-dap-an/78936",
        "https://khoahoc.vietjack.com/thi-online/giai-vbt-toan-7-cd-bai-1-tap-hop-cac-so-huu-ti-co-dap-an/107748",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-tap-hop-q-cac-so-huu-ti-co-dap-an-5/77357",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-tap-hop-q-cac-so-huu-ti-co-dap-an/50785",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-on-tap-toan-7-chuong-1-so-huu-ti-so-thuc-co-dap-an/60971",
        
        # Lop 6
        "https://khoahoc.vietjack.com/thi-online/de-kiem-tra-giua-ki-2-toan-6-co-dap-an-moi-nhat/89233",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-chuyen-de-toan-6-dang-2-cac-phep-toan-ve-cong-tru-nhan-chia-phan-so-co-dap-an/107268",
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-lop-6-kntt-bai-1-tap-hop-co-dap-an/114605",
        "https://khoahoc.vietjack.com/thi-online/5-cau-trac-nghiem-toan-6-canh-dieu-bai-1-tap-hop-co-dap-an-nhan-biet/72294",
        "https://khoahoc.vietjack.com/thi-online/10-cau-trac-nghiem-toan-6-chan-troi-sang-tao-bai-1-tap-hop-phan-tu-cua-tap-hop-co-dap-an/71259",
        "https://khoahoc.vietjack.com/thi-online/bai-tap-tap-hop-phan-tu-cua-tap-hop-chon-loc-co-dap-an/47455",
        "https://khoahoc.vietjack.com/thi-online/bai-11-dau-hieu-chia-het-cho-2-cho-5/16023"
        ]
urls = [
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-6-canh-dieu-chuong-5-phan-so-va-so-thap-phan-co-dap-an/109396",
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-6-canh-dieu-chuong-6-hinh-hoc-phang-co-dap-an/109349",
        "https://khoahoc.vietjack.com/thi-online/giai-vbt-toan-6-chuong-3-hinh-hoc-truc-quan-bo-canh-dieu/109259",
        "https://khoahoc.vietjack.com/thi-online/giai-vbt-toan-6-chuong-2-so-nguyen-bo-canh-dieu/109224",
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-6-canh-dieu-chuong-4-mot-so-yeu-to-thong-ke-va-xac-suat-co-dap-an/109186"
        "https://khoahoc.vietjack.com/thi-online/giai-vbt-toan-6-chuong-1-so-tu-nhien-bo-canh-dieu/109082",
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-6-chuong-3-hinh-hoc-truc-quan-bo-canh-dieu/68924",
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-6-chuong-2-so-nguyen-bo-canh-dieu/68906",
        "https://khoahoc.vietjack.com/thi-online/giai-sbt-toan-6-chuong-1-so-tu-nhien-bo-canh-dieu/68887",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-6-chuong-6-hinh-hoc-phang-bo-canh-dieu/68877",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-6-chuong-5-phan-so-va-so-thap-phan-bo-canh-dieu/68864",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-6-chuong-4-mot-so-yeu-to-thong-ke-va-xac-suat-bo-canh-dieu/68856",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-6-chuong-3-hinh-hoc-truc-quan-bo-canh-dieu/68847",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-6-chuong-2-so-nguyen-bo-canh-dieu/68840",
        "https://khoahoc.vietjack.com/thi-online/giai-sgk-toan-6-chuong-1-so-tu-nhien-bo-canh-dieu/68826",
]
hrefs = []
print("number of url: ",len(urls))
for idx,url in enumerate(urls):
    print(f"URL: {idx}")
    try:
        hrefs.extend(get_href_from_ul(url))
    except Exception as e:
        print(e)
        
hrefs = list(set(hrefs))
print("number of url: ",len(hrefs))
with open("urls.txt",'a') as f:
    for href in hrefs:
        f.write(href+"\n")

