from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd

# 波ダッシュを空白に変換する関数
def clean_text(text):
    return re.sub(r'\uff5e', ' ', text)

def clean_and_encode(text):
    # 不要な文字を削除または適切に変換
    cleaned_text = text.replace('\uff0d', '-')  # ハイフンに変換
    return cleaned_text.encode('shift-jis', 'replace').decode('shift-jis', 'replace')

def main():
    options = webdriver.ChromeOptions()
    # オプション: ヘッドレスモード（画面表示なし）を有効にする場合
    options.add_argument('--headless')
    options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(options=options)
    
    count = 0
    # データを格納するリストを初期化
    data_list = []
    
    # 条件url
    url = 'https://r.gnavi.co.jp/area/jp/ramen/rs/'

    driver.get(url)
    
    # ページが完全に読み込まれるまで待機
    time.sleep(3)
    
    # リストの範囲内でループ 今回は50回
    for i in range(50):
        # 要素数の取得
        h2_elements = driver.find_elements(By.CLASS_NAME, 'style_restaurantNameWrap__wvXSR')
        # ページの全ての要素を取得したら次ページへ遷移する
        if count == len(h2_elements):
            # 親要素を取得してその中からリンクを見つける
            parent_element = driver.find_element(By.CLASS_NAME, "style_pageNation__AZy1A")
            try:
                # 最後から2番目のリンク要素を取得
                next_page_link = parent_element.find_element(By.CSS_SELECTOR, "li:nth-last-child(2) a")
                # リンクをクリック
                driver.execute_script("arguments[0].click();", next_page_link)
                # countをリセット
                count -= len(h2_elements)
            except NoSuchElementException:
                print("最後から2番目の要素が見つかりませんでした。")            
        
        # JavaScript を使用して h2 要素をクリック
        # 現在のページで存在する 'style_restaurantNameWrap__wvXSR' クラスを持つ要素のリストを取得 
        h2_elements = driver.find_elements(By.CLASS_NAME, 'style_restaurantNameWrap__wvXSR')
        driver.execute_script("arguments[0].click();", h2_elements[count])

        # 新しいページが読み込まれるのを待つための短い遅延を追加
        time.sleep(3)
        
        # メールアドレス (仮で空の文字列を設定)
        mail = ""

        # 店名
        store = clean_text(driver.find_element(By.ID, "info-name").text)

        # 電話番号
        phone = clean_text(driver.find_element(By.CLASS_NAME, "number").text)

        # 住所
        address = clean_text(driver.find_element(By.CLASS_NAME, "region").text)

        # 建物
        locality_elements = driver.find_elements(By.CLASS_NAME, "locality")
        if locality_elements:
            building = clean_text(locality_elements[0].text)
        else:
            print("要素が見つかりませんでした。")   
            building = ""

        # 正規表現パターン
        pattern = r'^(.+?[都道府県])([^\d]+)(.+)$'
        # パターンにマッチする部分を検索
        match = re.match(pattern, address)
        if match:
            prefecture = match.group(1)
            city = match.group(2)
            rest_of_address = match.group(3)

        else:
            print('住所の解析に失敗しました')
        
        # 公式ページ(パターン1)
        official_url1 = driver.find_elements(By.CLASS_NAME, "sv-of.double")

        # 各<a>要素のhref属性の値を取得
        for url1 in official_url1:
            try:
                href_value = url1.get_attribute('href')
            except NoSuchElementException:
                print("要素が見つかりませんでした。")
                
        # 公式ページ(パターン2)
        official_url2 = driver.find_elements(By.CLASS_NAME, "url go-off")

        # 各<a>要素のhref属性の値を取得
        for url1 in official_url2:
            try:
                href_value = url1.get_attribute('href')
            except NoSuchElementException:
                print("要素が見つかりませんでした。")
                
        # 現在のページのURLを格納
        current_page_url = href_value
                
        # HTML内に"https"が含まれているかを確認
        ssl = current_page_url.startswith('https')

        # データを辞書に格納
        data = {
            '店舗名': clean_and_encode(store),
            '電話番号': clean_and_encode(phone),
            'メールアドレス': clean_and_encode(mail),
            '都道府県': clean_and_encode(prefecture),
            '市区町村': clean_and_encode(city),
            '番地': clean_and_encode(rest_of_address),
            '建物名': clean_and_encode(building),
            'URL': clean_and_encode(current_page_url),
            'SSL': ssl
        }

        # リストにデータを追加
        data_list.append(data)
        
        # "店舗一覧へ戻る"ボタンをクリック
        a_tag = driver.find_element(By.ID, 'gn_info-breadcrumbs-htpback-go')
        driver.execute_script("arguments[0].click();", a_tag)
        
        # 新しいページが読み込まれるのを待つための短い遅延を追加
        time.sleep(3)
        
        # count数の繰り上げ
        count += 1  

    # データフレームを作成
    df = pd.DataFrame(data_list)

    # CSVファイルに保存
    df.to_csv('1-2.csv', index=False, encoding='shift-jis')

if __name__ == "__main__":
    main()
