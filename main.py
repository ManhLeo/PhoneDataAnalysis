import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os
import argparse

from getlink import get_phone_links, save_phone_links, load_phone_links
import get_info

def scrape_phone_details(phone_links):
    """Lấy thông tin chi tiết từ danh sách links"""
    phones_data = []
    total_phones = len(phone_links)
    
    print("\n=== Bắt đầu thu thập thông tin chi tiết ===")
    for index, phone_info in enumerate(phone_links, 1):
        try:
            link = phone_info['link']
            initial_name = phone_info['name']
            # Lấy brand từ tên trong JSON
            brand = initial_name.split()[0] if initial_name else None
            
            print(f"\nĐang xử lý điện thoại {index}/{total_phones}: {initial_name}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Lấy thông tin chi tiết sử dụng các hàm từ get_info.py
            phone_data = {
                'name': initial_name,
                'brand': brand,
                'price': get_info.get_price(soup),
                'processor': get_info.get_processor(soup),
                'ram': get_info.get_ram(soup),
                'storage': get_info.get_storage(soup),
                'battery': get_info.get_battery(soup),
                'charging': get_info.get_charging(soup)
            }
            
            phones_data.append(phone_data)
            print_phone_details(phone_data)
            
            time.sleep(1)  # Be nice to the server
            
        except Exception as e:
            print(f"\nLỗi khi crawl {link}: {str(e)}")
            continue
    
    return phones_data

def print_phone_details(phone_data):
    """In thông tin chi tiết của điện thoại"""
    print("\n=== Thông tin điện thoại ===")
    print(f"Hãng: {phone_data.get('brand', 'N/A')}")
    print(f"Tên sản phẩm: {phone_data.get('name', 'N/A')}")
    
    # Format giá tiền
    price = phone_data.get('price')
    if price:
        try:
            price_int = int(price)
            price_formatted = "{:,}".format(price_int)
            print(f"Giá bán: {price_formatted} VNĐ")
        except (ValueError, TypeError):
            print(f"Giá bán: {price} VNĐ")
    else:
        print("Giá bán: N/A")
        
    print(f"Chip: {phone_data.get('processor', 'N/A')}")
    print(f"RAM: {phone_data.get('ram', 'N/A')}")
    print(f"Dung lượng lưu trữ: {phone_data.get('storage', 'N/A')}")
    print(f"Pin: {phone_data.get('battery', 'N/A')}")
    print(f"Sạc: {phone_data.get('charging', 'N/A')}")
    print("=" * 50)

def save_phone_data(phones_data, data_dir='data'):
    """Lưu dữ liệu điện thoại vào file CSV"""
    # Create DataFrame
    df = pd.DataFrame(phones_data)
    
    # Create data directory if not exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Add STT column
    df.insert(0, 'STT', range(1, len(df) + 1))
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(data_dir, f"phone_data_{timestamp}.csv")
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\nĐã lưu dữ liệu vào file {filename}")
    print(f"Tổng số điện thoại đã crawl: {len(phones_data)}")
    return filename

def crawl_links():
    """Hàm crawl và lưu danh sách links"""
    phone_links = get_phone_links()
    if phone_links:
        save_phone_links(phone_links)

def crawl_details(links_file=None):
    """Hàm crawl thông tin chi tiết từ file links"""
    phone_links = load_phone_links(links_file)
    if phone_links:
        phones_data = scrape_phone_details(phone_links)
        if phones_data:
            save_phone_data(phones_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawl dữ liệu điện thoại từ TheGioiDiDong')
    parser.add_argument('--mode', choices=['links', 'details', 'all'], 
                      default='all', help='Chọn chế độ crawl: links, details, hoặc all')
    parser.add_argument('--links-file', help='File JSON chứa danh sách links (cho chế độ details)')
    
    args = parser.parse_args()
    
    if args.mode == 'links':
        crawl_links()
    elif args.mode == 'details':
        crawl_details(args.links_file)
    else:  # all
        crawl_links()
        crawl_details() 