import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
import time

def clean_text_shift_jis(text):
    """Shift-JISエンコーディングでテキストをクリーンアップする関数"""
    if text is None:
        return ""

    # テキストを文字列に変換してから shift-jis に変換
    converted_text = str(text).encode('shift-jis', 'replace').decode('shift-jis', 'replace')

    # 特定の文字を修正
    converted_text = converted_text.replace('?', 'ー')  # ? を ー に置換

    return converted_text

def judge_string(soup, class_name):
    """指定されたクラス名で要素を探し、Shift-JISエンコーディングでクリーンアップしたテキストを返す関数"""
    item = soup.find('span', class_=class_name)
    return clean_text_shift_jis(item.string) if item else ""

def get_canonical_url(soup):
    """Canonical URLを取得し、Shift-JISエンコーディングでクリーンアップしたテキストを返す関数"""
    canonical_tag = soup.find('link', {'rel': 'canonical'})
    return clean_text_shift_jis(canonical_tag.attrs['href']) if canonical_tag else ""

def get_dynamic_href(url):
    """動的に生成されるリンクを取得する関数"""
    # Headless ブラウザの起動
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    # ページを開いて JavaScript を実行
    driver.get(url)
    time.sleep(3)  # JavaScript の実行を待つ (必要に応じて調整)

    # BeautifulSoup でページを解析
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # a タグを検索
    a_tag = soup.find('a', class_='url go-off')

    # a タグが存在するかチェックしてから href 属性を取得
    if a_tag:
        dynamic_href = a_tag.get('href')
    else:
        dynamic_href = ""

    return dynamic_href

def scrape_data(url, headers):
    """指定されたURLから店舗データをスクレイピングする関数"""
    data = {}

    try:
        # ページの取得
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 店舗名の取得
        raw_store_name = soup.find(id="info-name").string
        store = clean_text_shift_jis(raw_store_name)

        # その他の情報の取得
        phone = judge_string(soup, "number")
        prefecture = judge_string(soup, "region")
        building = judge_string(soup, "locality")
        mail = ""

        # 住所の正規表現パターン
        pattern = r'^(.+?[都道府県])([^\d]+)(.+)$'
        match = re.match(pattern, prefecture)
        if match:
            prefecture = clean_text_shift_jis(match.group(1))
            city = clean_text_shift_jis(match.group(2))
            rest_of_address = clean_text_shift_jis(match.group(3))
        else:
            prefecture = city = rest_of_address = ""
            
        # 公式サイトの取得(パターン1)
        official_url1 = soup.find('a', class_='sv-of double')
        # official_url1 が存在する場合はその href を取得、存在しない場合は空文字列
        official_url1_href = official_url1['href'] if official_url1 else ""

        # decide_url に代入する
        if official_url1_href:
            decide_url = official_url1_href
        # 公式サイトの取得(パターン2 動的に取得)
        else:
            decide_url = get_dynamic_href(url)

        ssl = decide_url.startswith('https')

        # データを辞書に格納
        data = {
            '店舗名': store,
            '電話番号': phone,
            'メールアドレス': mail,
            '都道府県': prefecture,
            '市区町村': city,
            '番地': rest_of_address,
            '建物名': building,
            'URL': decide_url,
            'SSL': ssl
        }

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    return data

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
   
    # 条件url
    target_url = "https://r.gnavi.co.jp/area/aream2157/rs/?date=20240106"

    url_list = []
    data_list = []
    count = 0
    max_data_count = 50  # 取得する最大データ数

    page_num = 1  # 初期ページ数

    while count < max_data_count:

        # p=が含まれているかどうかの判定
        if 'p=' in target_url:
            search_url = target_url.replace('p=1', f'p={page_num}')
            
        else:
            # ? が含まれているかどうかの判定
            if '?' in target_url:
                 # URLを構築
                search_url = f'{target_url}&p={page_num}'
            else:
                # URLを構築
                search_url = f'{target_url}?p={page_num}'
                
        print(search_url)

        try:
            # ページの取得
            time.sleep(3)
            response = requests.get(search_url, headers=headers)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')

            link_elements = soup.find_all('a', class_='style_titleLink__oiHVJ')
            url_list = [link['href'] for link in link_elements] if link_elements else []

            if url_list:
                for url in url_list:
                    count += 1
                    if count <= max_data_count:
                        data_list.append(scrape_data(url, headers))
                    else:
                        break

            else:
                print("URLが見つかりませんでした。")
                break

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            break

        page_num += 1  # 次のページへ遷移

    df = pd.DataFrame(data_list)
    df.to_csv('1-1.csv', index=False, encoding='shift-jis')  # shift-jis エンコーディングに変更

if __name__ == "__main__":
    main()
