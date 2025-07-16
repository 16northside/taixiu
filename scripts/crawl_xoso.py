import requests
from bs4 import BeautifulSoup
import sys

def crawl_xoso_full_table():
    url = "https://www.minhngoc.net.vn/free/index.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    all_numbers = []
    for td in soup.find_all("td"):
        text = td.get_text(strip=True)
        if text.isdigit():
            all_numbers.append(text)
    return all_numbers

def filter_last_n_digits(numbers, n=2):
    """Lọc ra n số cuối của mỗi số trong danh sách."""
    filtered = []
    for number in numbers:
        if len(number) >= n:
            filtered.append(number[-n:])
        else:
            filtered.append(number.zfill(n))
    return filtered

def safe_print(s):
    try:
        sys.stdout.buffer.write((s + '\n').encode('utf-8'))
    except Exception:
        print(s)

if __name__ == "__main__":
    all_numbers = crawl_xoso_full_table()
    safe_print("2 số cuối: {}".format(filter_last_n_digits(all_numbers, 2)))
    # Lọc chỉ những số có từ 3 chữ số trở lên
    numbers_3_digits = [num for num in all_numbers if len(num) >= 3]
    if numbers_3_digits:
        safe_print("3 số cuối: {}".format(filter_last_n_digits(numbers_3_digits, 3))) 