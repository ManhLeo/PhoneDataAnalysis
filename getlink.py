import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def get_phone_links():
    """Lấy danh sách links điện thoại từ cả điện thoại mới và cũ"""
    # Cấu hình các tùy chọn của Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Không hiển thị giao diện trình duyệt
    chrome_options.add_argument('--no-sandbox')  # Bỏ sandboxing
    chrome_options.add_argument('--disable-dev-shm-usage')  # Tắt sử dụng shared memory

    # Tự động tải và sử dụng ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    phone_links = []

    try:
        # Lấy links điện thoại mới
        url = "https://www.thegioididong.com/dtdd#c=42&o=13&pi=6"
        driver.get(url)
        
        # Chờ cho trang web load xong
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".listproduct .item"))
        )
        
        # Xử lý HTML cho điện thoại mới
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        phones = soup.select(".listproduct .item")
        
        for phone in phones:
            link_tag = phone.select_one("a")
            if link_tag:
                link = f"https://www.thegioididong.com{link_tag['href']}"
                name = link_tag.get('data-name', '').strip()
                
                if link and name:
                    clean_name = name.replace('Điện thoại', '').strip()
                    phone_links.append({
                        'link': link, 
                        'name': clean_name,
                        'type': 'new'
                    })

        # Lấy links điện thoại cũ
        url2 = "https://www.thegioididong.com/may-doi-tra/dtdd?prop=39238,39237&pi=13"
        driver.get(url2)
        
        # Chờ cho trang web load xong và các phần tử hiển thị đầy đủ
        wait = WebDriverWait(driver, 60)  # Tăng thời gian chờ lên 60 giây
        
        # Đợi cho ul.listproduct xuất hiện
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.listproduct"))
        )
        
        # Đợi cho các div.prdItem xuất hiện
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.listproduct div.prdItem"))
        )
        
        # Đợi cho các link trong div.prdItem xuất hiện
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.listproduct div.prdItem a[href]"))
        )
        
        # Cuộn trang để load thêm nội dung (nếu có)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Tăng thời gian đợi sau khi cuộn lên 5 giây
        
        # Cuộn lại lên đầu trang
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)  # Đợi thêm 5 giây sau khi cuộn lên đầu
        
        # Xử lý HTML cho điện thoại cũ
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        used_phones = soup.select("ul.listproduct div.prdItem")
        
        for phone in used_phones:
            link_tag = phone.select_one("a")
            if link_tag:
                link = f"https://www.thegioididong.com{link_tag['href']}"
                
                if link and name:
                    phone_links.append({
                        'link': link, 
                        'type': 'used'
                    })
    finally:
        # Đóng trình duyệt sau khi hoàn tất
        driver.quit()
    
    return phone_links

def save_phone_links(phone_links, data_dir='data'):
    """Lưu danh sách links vào file JSON"""
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(data_dir, f"phone_links_{timestamp}.json")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(phone_links, f, ensure_ascii=False, indent=2)
    
    print(f"\nĐã lưu danh sách links vào file {filename}")
    return filename

def load_phone_links(filename=None, data_dir='data'):
    """Đọc danh sách links từ file JSON"""
    import os
    import json

    if filename is None:
        # Nếu không có filename, lấy file mới nhất
        if not os.path.exists(data_dir):
            print(f"Không tìm thấy thư mục {data_dir} chứa danh sách links!")
            return None
            
        files = [f for f in os.listdir(data_dir) if f.startswith('phone_links_')]
        if not files:
            print("Không tìm thấy file chứa danh sách links!")
            return None
            
        filename = os.path.join(data_dir, sorted(files)[-1])  # Lấy file mới nhất
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            phone_links = json.load(f)
        print(f"\nĐã tải danh sách links từ file {filename}")
        return phone_links
    except Exception as e:
        print(f"Lỗi khi đọc file {filename}: {str(e)}")
        return None


if __name__ == "__main__":
    phone_links = get_phone_links()
    if phone_links:
        save_phone_links(phone_links)
