import re

def get_brand_from_name(name):
    if name:
        return name.split()[0]
    return None

def get_brand(source):
    # Lấy tên điện thoại
    name = get_name(source)
    if name:
        return get_brand_from_name(name)
    return None

def get_name(source):
    name_elem = source.find('h1', class_='detail-title')
    if name_elem:
        name = name_elem.text.strip()
        return name.replace('Điện thoại', '').strip()
    return None

def get_price(source):
    """Lấy giá từ nhiều vị trí có thể có trên trang"""
    item_div = source.find('div', class_='item cf-left')
    if item_div:
        price_b = item_div.find('b')
        if price_b:
            price_b_text = price_b.find('b')
            if price_b_text:
                return re.sub(r'[^\d]', '', price_b_text.text.strip())

    price_present = source.find('p', class_='box-price-present')
    if price_present:
        return re.sub(r'[^\d]', '', price_present.text.strip())

    price_one = source.find('div', class_='price-one')
    if price_one:
        price_present = price_one.find('p', class_='box-price-present')
        if price_present:
            return re.sub(r'[^\d]', '', price_present.text.strip())

    bs_price = source.find('div', class_='bs_price')
    if bs_price:
        price_strong = bs_price.find('strong')
        if price_strong:
            return re.sub(r'[^\d]', '', price_strong.text.strip())

    box_price = source.find('div', class_='box-price')
    if box_price:
        price_b = box_price.find('b')
        if price_b:
            return re.sub(r'[^\d]', '', price_b.text.strip())

    return None

def get_processor(source):
    item_div = source.find('div', class_='item cf-right')
    if item_div:
        param_list = item_div.find('ul', class_='parameter')
        if param_list:
            chip_item = param_list.find('span', string='Chip:')
            if chip_item:
                value_div = chip_item.find_parent('li').find('div')
                if value_div:
                    value_elem = value_div.find('p')
                    if value_elem:
                        text = value_elem.text.strip()
                        try:
                            if isinstance(text, bytes):
                                text = text.decode('utf-8')
                            else:
                                text = text.encode('latin1').decode('utf-8')
                        except (UnicodeEncodeError, UnicodeDecodeError):
                            pass
                        return text

    spec_tab = source.find('div', class_='specifications tab-content current')
    if spec_tab:
        chip_label = spec_tab.find('strong', string=lambda x: x and ('Chip xử lý' in x or 'CPU' in x))
        if chip_label:
            chip_aside = chip_label.find_parent('aside').find_next_sibling('aside')
            if chip_aside:
                chip_span = chip_aside.find('span')
                if chip_span:
                    text = chip_span.text.strip()
                    try:
                        if isinstance(text, bytes):
                            text = text.decode('utf-8')
                        else:
                            text = text.encode('latin1').decode('utf-8')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        pass
                    return text

    return None

def get_ram(source):
    """Lấy thông tin RAM từ cấu trúc HTML"""
    item_div = source.find('div', class_='item cf-right')
    if item_div:
        param_list = item_div.find('ul', class_='parameter')
        if param_list:
            ram_item = param_list.find('span', string='RAM:')
            if ram_item:
                value_div = ram_item.find_parent('li').find('div')
                if value_div:
                    value_elem = value_div.find('p')
                    if value_elem:
                        return value_elem.text.strip()

    spec_tab = source.find('div', class_='specifications tab-content current')
    if spec_tab:
        ram_label = spec_tab.find('a', string=lambda x: x and 'RAM:' in x)
        if ram_label:
            ram_aside = ram_label.find_parent('aside').find_next_sibling('aside')
            if ram_aside:
                ram_span = ram_aside.find('span')
                if ram_span:
                    return ram_span.text.strip()

    return None

def get_storage(source):

    item_div = source.find('div', class_='item cf-right')
    if item_div:
        spec_section = item_div.find('ul', class_='parameter')
        if spec_section:
            storage_item = spec_section.find('span', text=lambda t: t and ('Dung lượng' in t))
            if storage_item:
                value_div = storage_item.find_parent('li').find('div')
                if value_div:
                    p_elems = value_div.find('p')
                    if p_elems:
                        return p_elems.text.strip()
                    
    spec_tab = source.find('div', class_='specifications tab-content current')
    if spec_tab:
        storage_label = spec_tab.find('strong', text=lambda x: x and ('Dung lượng' in x))
        if storage_label:
            storage_aside = storage_label.find_parent('aside').find_next_sibling('aside')
            if storage_aside:
                storage_span = storage_aside.find('span')
                if storage_span:
                    return storage_span.text.strip()
                
    return None

def get_battery(source):
    # Tìm phần tử chứa thông tin dung lượng pin
    item_div = source.find('div', class_='item cf-right')
    if item_div:
        spec_section = item_div.find('ul', class_='parameter')
        if spec_section:
            battery_item = spec_section.find('span', text=lambda t: t and 'Pin' in t)
            if battery_item:
                value_div = battery_item.find_parent('li').find('div')
                if value_div:
                    p_elems = value_div.find_all('p')
                    for p in p_elems:
                        text = p.text.strip()
                        if 'mah' in text.lower():
                            return text
    
    spec_tab = source.find('div', class_='specifications tab-content current')
    if spec_tab:
        battery_label = spec_tab.find('strong', string=lambda x: x and 'Dung lượng pin' in x)
        if battery_label:
            battery_aside = battery_label.find_parent('aside').find_next_sibling('aside')
            if battery_aside:
                battery_span = battery_aside.find('span')
                if battery_span:
                    return battery_span.text.strip()
    
    return None

def get_charging(source):
    # Tìm phần tử chứa thông tin dung lượng pin
    item_div = source.find('div', class_='item cf-right')
    if item_div:
        spec_section = item_div.find('ul', class_='parameter')
        if spec_section:
            charging_item = spec_section.find('span', text=lambda t: t and 'Pin' in t)
            if charging_item:
                value_div = charging_item.find_parent('li').find('div')
                if value_div:
                    p_elems = value_div.find_all('p')
                    for p in p_elems:
                        text = p.text.strip()
                        if 'w' in text.lower():
                            return text
    
    # Tìm trong tab thông số kỹ thuật
    spec_tab = source.find('div', class_='specifications tab-content current')
    if spec_tab:
        charging_label = spec_tab.find('strong', string=lambda x: x and 'Hỗ trợ sạc tối đa' in x)
        if charging_label:
            charging_aside = charging_label.find_parent('aside').find_next_sibling('aside')
            if charging_aside:
                charging_span = charging_aside.find('span')
                if charging_span:
                    return charging_span.text.strip()
    
    return None 