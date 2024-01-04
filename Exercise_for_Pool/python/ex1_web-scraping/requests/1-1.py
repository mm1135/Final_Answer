# 必要なモジュールをインポート
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

# ぐるなびのurl
urls = [
        "https://r.gnavi.co.jp/c088t36g0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203965",
        "https://r.gnavi.co.jp/aeebgy0w0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202426",
        "https://r.gnavi.co.jp/fdn145ys0000/?sc_type=area&sc_area=jp&sc_dsp=rs_204129",
        "https://r.gnavi.co.jp/pph4y6np0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203303",
        "https://r.gnavi.co.jp/asbe5e280000/?sc_type=area&sc_area=jp&sc_dsp=rs_206016",
        "https://r.gnavi.co.jp/3f6ev8pe0000/?sc_type=area&sc_area=jp&sc_dsp=rs_204170",
        "https://r.gnavi.co.jp/7u7cvkur0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202784",
        "https://r.gnavi.co.jp/hrcjvea30000/?sc_type=area&sc_area=jp&sc_dsp=rs_203487",
        "https://r.gnavi.co.jp/nycwthv00000/?sc_type=area&sc_area=jp&sc_dsp=rs_201383",
        "https://r.gnavi.co.jp/8xz3f7hg0000/?sc_type=area&sc_area=jp&sc_dsp=rs_201291",
        "https://r.gnavi.co.jp/ptytkyga0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203406",
        "https://r.gnavi.co.jp/7w3g8a410000/?sc_lid=home_check_shop",
        "https://r.gnavi.co.jp/snv8gzwj0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202487",
        "https://r.gnavi.co.jp/a096200/?sc_type=area&sc_area=jp&sc_dsp=rs_198849",
        "https://r.gnavi.co.jp/b232405/?sc_type=area&sc_area=jp&sc_dsp=rs_199231",
        "https://r.gnavi.co.jp/rmecc00v0000/?sc_type=area&sc_area=jp&sc_dsp=rs_199710",
        "https://r.gnavi.co.jp/ku6gdpmx0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203241",
        "https://r.gnavi.co.jp/fccmb6s70000/?sc_type=area&sc_area=jp&sc_dsp=rs_200421",
        "https://r.gnavi.co.jp/acbn169b0000/?sc_type=area&sc_area=jp&sc_dsp=rs_200400",
        "https://r.gnavi.co.jp/pp4z1k7b0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202606",
        "https://r.gnavi.co.jp/g926002/?sc_type=area&sc_area=jp&sc_dsp=rs_201121",
        "https://r.gnavi.co.jp/kdbd8tvy0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203305",
        "https://r.gnavi.co.jp/5fbgzxhh0000/?sc_type=area&sc_area=jp&sc_dsp=rs_206079",
        "https://r.gnavi.co.jp/prhp6j1f0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202653",
        "https://r.gnavi.co.jp/nf6us7dj0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202967",
        "https://r.gnavi.co.jp/358ddcrm0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203801",
        "https://r.gnavi.co.jp/6c9k8wmx0000/?sc_type=area&sc_area=jp&sc_dsp=rs_205627",
        "https://r.gnavi.co.jp/kum15p9s0000/?sc_type=area&sc_area=jp&sc_dsp=rs_207649",
        "https://r.gnavi.co.jp/4bs240nr0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203351",
        "https://r.gnavi.co.jp/f000302/?sc_type=area&sc_area=jp&sc_dsp=rs_199861",
        "https://r.gnavi.co.jp/933uk4hz0000/?sc_type=area&sc_area=jp&sc_dsp=rs_200301",
        "https://r.gnavi.co.jp/hj8xdfcc0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203677",
        "https://r.gnavi.co.jp/pk7z9wdu0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202079",
        "https://r.gnavi.co.jp/rgt38r9u0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203862",
        "https://r.gnavi.co.jp/5z07du4c0000/?sc_type=area&sc_area=jp&sc_dsp=rs_201687",
        "https://r.gnavi.co.jp/r9xe6z9s0000/?sc_type=area&sc_area=jp&sc_dsp=rs_206595",
        "https://r.gnavi.co.jp/bjpjrbkm0000/?sc_type=area&sc_area=jp&sc_dsp=rs_201634",
        "https://r.gnavi.co.jp/p477501/?sc_type=area&sc_area=jp&sc_dsp=rs_206867",
        "https://r.gnavi.co.jp/rj5zxh1g0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202540",
        "https://r.gnavi.co.jp/7rebhk3c0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203357",
        "https://r.gnavi.co.jp/a2u7mn4m0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202122",
        "https://r.gnavi.co.jp/2smwygjw0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202890",
        "https://r.gnavi.co.jp/5vybz9ay0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203713",
        "https://r.gnavi.co.jp/pnusfg230000/?sc_type=area&sc_area=jp&sc_dsp=rs_202321",
        "https://r.gnavi.co.jp/d7esc2zr0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203714",
        "https://r.gnavi.co.jp/ejbvchhr0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202050",
        "https://r.gnavi.co.jp/j70k8g9u0000/?sc_type=area&sc_area=jp&sc_dsp=rs_203146",
        "https://r.gnavi.co.jp/rmrxrmdn0000/?sc_type=area&sc_area=jp&sc_dsp=rs_202786",
        "https://r.gnavi.co.jp/rdx0aftf0000/?sc_type=area&sc_area=jp&sc_dsp=rs_201878",
        "https://r.gnavi.co.jp/2savbzzc0000/?sc_type=area&sc_area=jp&sc_dsp=rs_200303"
]
# ユーザーエージェントを設定
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def judge_string(soup, class_name):
    item = soup.find('span', class_=class_name)
    return item.string if item else ""

def get_canonical_url(soup):
    canonical_tag = soup.find('link', {'rel': 'canonical'})
    return canonical_tag.attrs['href'] if canonical_tag else ""

# データを格納するリストを初期化
data_list = []

def main():
    for url in urls:
        # アイドリングタイム（3秒）を追加
        time.sleep(3)

        # url情報を取得
        response = requests.get(url, headers=headers)
        # 文字化け防止
        response.encoding = response.apparent_encoding

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(response.text, 'html.parser')

        # 店名
        store = soup.find(id="info-name")
        # 店名のテキストを格納
        store = store.string
        #print(store)

        # 電話番号
        phone = judge_string(soup, "number")

        # 住所
        address = judge_string(soup, "region")

        # 建物
        building = judge_string(soup, "locality")

        # メールアドレス (仮で空の文字列を設定)
        mail = ""

        # 正規表現パターン
        pattern = r'^(.+?[都道府県])([^\d]+)(.+)$'

        # パターンにマッチする部分を検索
        match = re.match(pattern, address)
        if match:
            prefecture = match.group(1)
            city = match.group(2)
            rest_of_address = match.group(3)
        else:
            prefecture = city = rest_of_address = ""

        # linkタグからcanonical URLを取得する
        canonical_url = get_canonical_url(soup)

        # HTML内に"https"が含まれているかを確認
        ssl = canonical_url.startswith('https')

        # データを辞書に格納
        data = {
            '店舗名': store,
            '電話番号': phone,
            'メールアドレス': mail,
            '都道府県': prefecture,
            '市区町村': city,
            '番地': rest_of_address,
            '建物名': building,
            'URL': canonical_url,
            'SSL': ssl
        }

        # リストにデータを追加
        data_list.append(data)

    # データフレームを作成
    df = pd.DataFrame(data_list)

    # CSVファイルに保存
    df.to_csv('sample.csv', index=False)

if __name__ == "__main__":
    main()
