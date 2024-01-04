from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
import time

def main():
    # Chrome WebDriverのオプションを設定
    options = webdriver.ChromeOptions()

    # オプション: ヘッドレスモード（画面表示なし）を有効にする場合
    options.add_argument('--headless')

    # ユーザーエージェントを設定
    options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # Chrome WebDriverのインスタンスを作成
    driver = webdriver.Chrome(options=options)

    # 初回のアクセスするURL
    url = 'https://r.gnavi.co.jp/7w3g8a410000/?sc_lid=r-r_display01&sc_dsp=shop_203888'

    # データを格納するリストを初期化
    data_list = []

    # ループ回数
    loop_count = 50

    for i in range(loop_count):
        # ブラウザで指定されたURLを開く
        driver.get(url)

        time.sleep(3)

        # メールアドレス (仮で空の文字列を設定)
        mail = ""

        # 店名
        store = driver.find_element(By.ID, "info-name").text
        #print(store)

        # 電話番号
        phone = driver.find_element(By.CLASS_NAME, "number").text
        #print(phone)

        # 住所
        address = driver.find_element(By.CLASS_NAME, "region").text
        #print(address)

        # 建物
        #building = driver.find_element(By.CLASS_NAME, "locality").text
        #print(building)
        locality_elements = driver.find_elements(By.CLASS_NAME, "locality")
        if locality_elements:
            building = locality_elements[0].text
            #print(building)
        else:
            print("要素が見つかりませんでした。")    

        # 正規表現パターン
        pattern = r'^(.+?[都道府県])([^\d]+)(.+)$'
        # パターンにマッチする部分を検索
        match = re.match(pattern, address)
        if match:
            prefecture = match.group(1)
            city = match.group(2)
            rest_of_address = match.group(3)

            #print('都道府県:', prefecture)
            #print('市区町村:', city)
            #print('残りの住所:', rest_of_address)
        else:
            print('住所の解析に失敗しました')

        # 現在のページのURLを取得
        current_page_url = driver.current_url

        # HTML内に"https"が含まれているかを確認
        ssl = current_page_url.startswith('https')

        # データを辞書に格納
        data = {
            '店舗名': store,
            '電話番号': phone,
            'メールアドレス': mail,
            '都道府県': prefecture,
            '市区町村': city,
            '番地': rest_of_address,
            '建物名': building,
            'URL': current_page_url,
            'SSL': ssl
        }

        # リストにデータを追加
        data_list.append(data)

        # class属性が "pr-unit4__name" の要素を取得
        ul_element = driver.find_elements(By.CLASS_NAME, "pr-unit4__name--pr")

        # 4あるうちの1つ目のaタグを取得
        a_tag = ul_element[0].find_element(By.TAG_NAME, "a")

        # aタグのhref属性を取得し、次のURLとして設定
        url = a_tag.get_attribute('href')



    # データフレームを作成
    df = pd.DataFrame(data_list)

    # データフレームを表示
    #print(df)

    # CSVファイルに保存
    df.to_csv('sample.csv', index=False)

if __name__ == "__main__":
    main()
