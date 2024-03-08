import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from urllib.parse import urljoin, urlparse, urlencode, parse_qs  # 必要なモジュールをインポート
import os
from selenium.common.exceptions import TimeoutException
import traceback
import sys
from selenium.common.exceptions import StaleElementReferenceException
import psutil
from datetime import datetime

def check_memory_usage():
    # プロセスIDを取得
    pid = psutil.Process(driver.service.process.pid)

    # メモリ使用量を表示
    print(f"Memory usage before quitting: {pid.memory_info().rss / 1024 / 1024:.2f} MB")
    log_to_file(f"Memory usage before quitting: {pid.memory_info().rss / 1024 / 1024:.2f} MB")

def close_driver(driver):
    check_memory_usage()

    try:
        # driverとdriver.service.processがNoneでないか確認
        if driver and driver.service.process:
            driver.close()  # 現在のウィンドウを閉じる
            driver.quit()  # WebDriverセッションを終了する

            # driver.service.process.pidがNoneでないか確認
            if driver.service.process.pid:
                process = psutil.Process(driver.service.process.pid)
                process.terminate()  # プロセスを強制終了
    except Exception as e:
        print(f"Error closing driver: {e}")
        log_to_file(f"Error closing driver: {e}")
    finally:
        check_memory_usage()



def log_to_file(*log_texts):
    log_file_path = 'scrape_log.txt'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 現在の時刻を取得し、文字列に変換
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{current_time} {' '.join(map(str, log_texts))}\n")  # 時刻をログメッセージの先頭に追加

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

headers = {
    "User-Agent": user_agent,
}

def scrape_wlw_data():

    url = "https://www.wlw.de"


    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    # URLを格納するリスト
    url_list = []

    data_list = []

    # ul要素を取得
    ul_elements = soup.find_all('ul', {'data-v-dbaea932': ''})

    if ul_elements:
        # ul要素内の全てのli要素を取得
        li_elements = ul_elements[1].find_all('li', {'data-v-dbaea932': ''})  # 修正: 変数名をul_elementsに変更

        for li in li_elements:
            # li要素内のaタグを取得
            a_tag = li.find('a')
            text = a_tag.text.strip()

            if text == "Akku- und Batterietechnik":
                cate = "Elektronik und Elektrotechnik"
                print(cate)
            elif text == "Ankauf und Restposten":
                cate = "Industriebedarf und Objekteinrichtung"
                print(cate)
            elif text == "Antriebstechnik":
                cate = "Antriebstechnik"

            elif text == "Arbeitsschutz":
                cate = "Arbeitsschutz, Sicherheit und Rettung"

            elif text == "Armaturentechnik":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Bau":
                cate = "Bau"

            elif text == "Baumaschinen und Baugeräte":
                cate = "Bau"

            elif text == "Baustellenbedarf":
                cate = "Bau"

            elif text == "Baustoffe und Baubedarf":
                cate = "Bau"

            elif text == "Bauteile":
                cate = "Bau"

            elif text == "Bedarf für Landwirtschaft, Forstwirtschaft, Fischerei, Gartenbau":
                cate = "Landwirtschaft, Forstwirtschaft, Fischerei und Gartenbau"

            elif text == "Bedarf für Textilproduktion und Lederverarbeitung":
                cate = "Bekleidung und Textil"

            elif text == "Befestigungstechnik, Verbindungstechnik und Beschläge":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Behälter, Logistik- und Lagerbedarf":
                cate = "Logistik, Fördertechnik und Lagerung"

            elif text == "Bekleidung und Accessoires":
                cate = "Bekleidung und Textil"

            elif text == "Beleuchtung":
                cate = "Elektronik und Elektrotechnik"

            elif text == "Beratung":
                cate = "Dienstleistungen"

            elif text == "Bürobedarf":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Design":
                cate = "Dienstleistungen"

            elif text == "Dichtungstechnik":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Dienstleistungen aus Landwirtschaft, Forstwirtschaft, Fischerei, Gartenbau":
                cate = "Landwirtschaft, Forstwirtschaft, Fischerei und Gartenbau"

            elif text == "Druck und Papier":
                cate = "Druck und Papier"

            elif text == "Druck- und Papiermaschinen":
                cate = "Maschinen und Maschinenteile"

            elif text == "Elektrodienstleistungen":
                cate = "Elektronik und Elektrotechnik"

            elif text == "Elektrotechnik":
                cate = "Elektronik und Elektrotechnik"

            elif text == "Energietechnik":
                cate = "Klima-, Lüftungs-, Wärme- und Energietechnik"

            elif text == "Entsorgung und Recycling":
                cate = "Dienstleistungen"

            elif text == "Erzeugnisse aus Landwirtschaft, Forstwirtschaft, Fischerei, Gartenbau":
                cate = "Landwirtschaft, Forstwirtschaft, Fischerei und Gartenbau"

            elif text == "Event- und Veranstaltungsdienstleistungen":
                cate = "Dienstleistungen"

            elif text == "Fahrzeuge":
                cate = "Verkehrstechnik und Transportmittel"

            elif text == "Fahrzeugteile und Fahrzeugzubehör":
                cate = "Verkehrstechnik und Transportmittel"

            elif text == "Filter- und Siebtechnik":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Finanzen und Versicherung":
                cate = "Dienstleistungen"

            elif text == "Fluidtechnik":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Fördertechnik":
                cate = "Logistik, Fördertechnik und Lagerung"

            elif text == "Foto-, Film- und Tondienstleistungen":
                cate = "Dienstleistungen"

            elif text == "Freizeit, Kultur und Tourismus":
                cate = "Sport, Kultur und Freizeit"

            elif text == "Fügen":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Gastronomie":
                cate = "Haushalt und Gastronomie"

            elif text == "Gastronomiebedarf":
                cate = "Haushalt und Gastronomie"

            elif text == "Gastronomie- und Küchengeräte":
                cate = "Haushalt und Gastronomie"

            elif text == "Gieß- und Spritzgießmaschinen":
                cate = "Maschinen und Maschinenteile"

            elif text == "Glas- und Keramikerzeugnisse":
                cate = "Werkstoffe und Halbzeuge"

            elif text == "Guss, Spritzguss und additive Fertigung":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Hardware für Informations- und Kommunikationstechnik":
                cate = "Informationstechnik und Multimedia"

            elif text == "Haushaltsartikel":
                cate = "Haushalt und Gastronomie"

            elif text == "Heimtextilien":
                cate = "Bekleidung und Textil"

            elif text == "Holz und Holzerzeugnisse":
                cate = "Werkstoffe und Halbzeuge"

            elif text == "Hygiene- und Kosmetikartikel":
                cate = "Medizin, Hygiene und Kosmetik"

            elif text == "Immobiliendienstleistungen":
                cate = "Dienstleistungen"

            elif text == "Industriebedarf":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Informationstechnik-Dienstleistungen":
                cate = "Informationstechnik und Multimedia"

            elif text == "Kabeltechnik":
                cate = "Elektronik und Elektrotechnik"

            elif text == "Kälte-, Klima-, Lüftungs- und Wärmetechnik":
                cate = "Klima-, Lüftungs-, Wärme- und Energietechnik"

            elif text == "Kennzeichnungstechnik":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Kunststoff und Kunststofferzeugnisse":
                cate = "Werkstoffe und Halbzeuge"

            elif text == "Labortechnik und -bedarf":
                cate = "Mess- und Labortechnik"

            elif text == "Lasertechnik":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Lebensmittel":
                cate = "Lebensmittel"

            elif text == "Lebensmitteltechnik":
                cate = "Maschinen und Maschinenteile"

            elif text == "Leder, textile Fasern, Garne und Stoffe":
                cate = "Bekleidung und Textil"

            elif text == "Logistik, Transporte und Lagerung":
                cate = "Logistik, Fördertechnik und Lagerung"

            elif text == "Löt-, Schweiß- und Klebetechnik":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Management und Verwaltung":
                cate = "Dienstleistungen"

            elif text == "Marketing, Werbung und Vertrieb":
                cate = "Marketing, Vertrieb und Werbetechnik"

            elif text == "Maschinenbau, Anlagenbau und Apparatebau":
                cate = "Maschinen und Maschinenteile"

            elif text == "Maschinen für Landwirtschaft, Forstwirtschaft, Fischerei, Gartenbau":
                cate = "Landwirtschaft, Forstwirtschaft, Fischerei und Gartenbau"

            elif text == "Maschinenteile":
                cate = "Maschinen und Maschinenteile"

            elif text == "Medizin und Gesundheit":
                cate = "Medizin, Hygiene und Kosmetik"

            elif text == "Mess-, Prüf- und Analysedienstleistungen":
                cate = "Mess- und Labortechnik"

            elif text == "Mess- und Prüftechnik":
                cate = "Mess- und Labortechnik"

            elif text == "Metall und Metallerzeugnisse":
                cate = "Werkstoffe und Halbzeuge"

            elif text == "Möbel und Objekteinrichtung":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Montage":
                cate = "Dienstleistungen"

            elif text == "Multimedia":
                cate = "Informationstechnik und Multimedia"

            elif text == "Oberflächenbehandlung":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Oberflächenbehandlungsmaschinen":
                cate = "Maschinen und Maschinenteile"

            elif text == "Optik":
                cate = "Mess- und Labortechnik"
            
            elif text == "Personaldienstleistungen":
                cate = "Dienstleistungen"

            elif text == "Pflege- und Kosmetikdienstleistungen":
                cate = "Dienstleistungen"

            elif text == "Planung, Konstruktion und Entwicklung":
                cate = "Dienstleistungen"

            elif text == "Pumpentechnik":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Reinigung":
                cate = "Dienstleistungen"

            elif text == "Reinigungsgeräte und -maschinen":
                cate = "Maschinen und Maschinenteile"

            elif text == "Reinigungs- und Pflegemittel":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Reinigungsutensilien":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Reparatur, Instandhaltung und Modernisierung":
                cate = "Dienstleistungen"

            elif text == "Robotik, Prozess- und Automatisierungstechnik":
                cate = "Steuer-, Regel- und Automatisierungstechnik"

            elif text == "Rohr- und Schlauchtechnik":
                cate = "Industriebedarf und Objekteinrichtung"

            elif text == "Rohstoffe und Chemie":
                cate = "Mess- und Labortechnik"

            elif text == "Sanitärtechnik":
                cate = "Bau"

            elif text == "Schulung und Weiterbildung":
                cate = "Dienstleistungen"

            elif text == "Sicherheitsdienstleistungen":
                cate = "Arbeitsschutz, Sicherheit und Rettung"

            elif text == "Sicherheits- und Rettungstechnik":
                cate = "Arbeitsschutz, Sicherheit und Rettung"

            elif text == "Software":
                cate = "Informationstechnik und Multimedia"

            elif text == "Sport":
                cate = "Sport, Kultur und Freizeit"

            elif text == "Steuer- und Regeltechnik":
                cate = "Steuer-, Regel- und Automatisierungstechnik"

            elif text == "Textilmaschinen":
                cate = "Maschinen und Maschinenteile"

            elif text == "Textilproduktion":
                cate = "Bekleidung und Textil"

            elif text == "Übersetzungs- und Lektoratsdienstleistungen":
                cate = "Dienstleistungen"

            elif text == "Umwelttechnik":
                cate = "Maschinen und Maschinenteile"

            elif text == "Verfahrenstechnik":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Verkehrstechnik":
                cate = "Verkehrstechnik und Transportmittel"

            elif text == "Verpackungsdienstleistungen":
                cate = "Verpackung"

            elif text == "Verpackungsmaschinen":
                cate = "Maschinen und Maschinenteile"

            elif text == "Verpackungsmaterial":
                cate = "Verpackung"

            elif text == "Wärmebehandlung":
                cate = "Fertigungstechnik und Verfahrenstechnik"

            elif text == "Werbemittel und Werbetechnik":
                cate = "Marketing, Vertrieb und Werbetechnik"

            elif text == "Werkzeuge und Fertigungsbedarf":
                cate = "Werkzeuge und Fertigungsbedarf"

            elif text == "Werkzeugmaschinen und -geräte":
                cate = "Maschinen und Maschinenteile"

            elif text == "Zerspanung und Umformung":
                cate = "Fertigungstechnik und Verfahrenstechnik"


            # aタグが存在する場合、そのhref属性を取得
            if a_tag:
                href = a_tag.get('href')
                # URLに "https://www.wlw.de/" を追加してリストに格納
                full_url = url + href
                url_list.append([cate, text, full_url])
            else:
                print("li要素内にaタグが見つかりませんでした。")
                log_to_file("li要素内にaタグが見つかりませんでした。")

    # 取得した情報を表示
    # print("Big Categories:", big_category)
    print("URL List:")
    log_to_file("URL List:")

    csv_filename = 'list17.csv'

    for o in range(53,70):

        item = url_list[o]
        
        count_sum = 0
        
        page = 1
    # for k in range(1):
    #     item = url_list[k]
        print(item)
        log_to_file(item)

        detail_url = item[2]
        print("detail_url：" + detail_url)
        log_to_file("detail_url：" + detail_url)

        try:

            # URLからページのHTMLを取得
            response = requests.get(detail_url, headers=headers)
            response.encoding = response.apparent_encoding

            # BeautifulSoupを使ってHTMLを解析
            soup = BeautifulSoup(response.text, 'html.parser')

            # 1秒待つ
            # time.sleep(1)

            a_tag = soup.select_one('h2[data-v-1c5ec946] a[href]')
            if a_tag:
                href_value = a_tag.get('href')
                href = url + href_value
                print(f'href属性の値: {href}')
                log_to_file(f'href属性の値: {href}')
            else:
                print('<a>タグが見つかりませんでした。')
                log_to_file('<a>タグが見つかりませんでした。')

            a_text = a_tag.text
            print("a_text", a_text )
            log_to_file("a_text", a_text )
            
            
            max_retries = 20
            retry_count = 0
            
            
            while retry_count < max_retries:

                try:
                    # URLにアクセス
                    driver.get(href)


                    # 最初の<li>タグから<a>タグを取得
                    li_tags = WebDriverWait(driver, 90).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-v-e9a02bb7]')))

                    break


                except TimeoutException:
                    # TimeoutExceptionが発生した場合、つまりボタンが見つからない場合やタイムアウトした場合
                    print("TimeoutException発生")
                    log_to_file("TimeoutException発生")
                    retry_count += 1
                except StaleElementReferenceException:
                    # 要素がStaleになった場合、再取得を試みる
                    print("Stale Element Reference Exception 発生") 
                    log_to_file("Stale Element Reference Exception 発生")      
                    retry_count += 1          
                except Exception as e:
                    # 他の例外が発生した場合
                    print("エラーが発生しました:", str(e))
                    log_to_file(f"エラーが発生しました: {type(e).__name__}, {str(e)}")
                    traceback.print_exc()  # トレースバックを出力するためのこの行を追加
                    retry_count += 1
                finally:
                    print("finalllyを通過")
                    log_to_file("finalllyを通過")
                    # 何かしらのクリーンアップや終了処理が必要な場合

            if li_tags:
                # Ensure that there is at least one <li> tag
                li_tag = li_tags[1]

                # Find the <a> tag within the selected <li> tag
                a_tag = li_tag.find_element(By.TAG_NAME, 'a')

                if a_tag:
                    href_value = a_tag.get_attribute('href')
                    categoty_url = urljoin(url, href_value)
                    print(f'href属性の値: {categoty_url}')
                    log_to_file(f'href属性の値: {categoty_url}')
                else:
                    print('liタグ内に<a>タグが見つかりませんでした。')
                    log_to_file('liタグ内に<a>タグが見つかりませんでした。')

        
            max_retries = 20
            retry_count = 0
            
            
            while retry_count < max_retries:

                try:
                    # URLにアクセス
                    driver.get(categoty_url)

                    # ページが完全に読み込まれるまで待機
                    wait = WebDriverWait(driver, 90)  # 最大で10秒待機
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

                    break

                except TimeoutException:
                    # TimeoutExceptionが発生した場合、つまりボタンが見つからない場合やタイムアウトした場合
                    print("TimeoutException発生")
                    log_to_file("TimeoutException発生")
                    retry_count += 1
                except StaleElementReferenceException:
                    # 要素がStaleになった場合、再取得を試みる
                    print("Stale Element Reference Exception 発生")  
                    log_to_file("Stale Element Reference Exception 発生")
                    retry_count += 1 
                except Exception as e:
                    # 他の例外が発生した場合
                    print("エラーが発生しました:", str(e))
                    log_to_file(f"エラーが発生しました: {type(e).__name__}, {str(e)}")
                    traceback.print_exc()  # トレースバックを出力するためのこの行を追加
                    retry_count += 1
                finally:
                    print("finalllyを通過")
                    log_to_file("finalllyを通過")
                    # 何かしらのクリーンアップや終了処理が必要な場合

            # HTMLを取得
            page_html = driver.page_source

            # BeautifulSoupを使ってHTMLを解析
            soup = BeautifulSoup(page_html, 'html.parser')

            # 'a'タグを取得
            page_num = soup.find_all('a', {'data-test': 'pagination-number'})

            # page_n分ループする
            page_n = int(page_num[len(page_num)-1].text)


            print("page_n：",page_n)

            while  page <= page_n:

                if page == 1:
                    pass
                    print("page_n：",page_n)
                    log_to_file("page_n：",page_n)

                    box_items = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'div.bg-white.shadow-200.rounded.p-1')
                        )
                    )

                    page += 1
                else:
                    # categoty_urlを基に次のページのURLを作成
                    parsed_url = urlparse(categoty_url)
                    query_params = parse_qs(parsed_url.query)
                    next_page_url = urljoin(categoty_url, f'produkte/page/{page}?{urlencode(query_params, doseq=True)}')


                    print("next_page_url：", next_page_url)
                    log_to_file("next_page_url：", next_page_url)
                    
                    
                    max_retries = 20
                    retry_count = 0
                    
                    
                    while retry_count < max_retries:

                        try:
                                                # URLにアクセス
                            driver.get(next_page_url)

                            # ページが完全に読み込まれるまで待機
                            wait = WebDriverWait(driver, 90)  # 最大で10秒待機
                            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

                            # HTMLを取得
                            page_html = driver.page_source

                            # BeautifulSoupを使ってHTMLを解析
                            soup = BeautifulSoup(page_html, 'html.parser')

                            # ここで必要な処理を行う
                            box_items = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, 'div.bg-white.shadow-200.rounded.p-1')
                                )
                            )

                            if len(box_items) == 30:
                                page += 1
                                break
                            elif page_n == page:
                                page += 1
                                break
                            else:
                                continue 

                        except TimeoutException:
                            # TimeoutExceptionが発生した場合、つまりボタンが見つからない場合やタイムアウトした場合
                            print("TimeoutException発生")
                            log_to_file("TimeoutException発生")
                            retry_count += 1
                        except StaleElementReferenceException:
                            # 要素がStaleになった場合、再取得を試みる
                            print("Stale Element Reference Exception 発生")
                            log_to_file("Stale Element Reference Exception 発生")
                            retry_count += 1 
                        except Exception as e:
                            # 他の例外が発生した場合
                            print("エラーが発生しました:", str(e))
                            log_to_file(f"エラーが発生しました: {type(e).__name__}, {str(e)}")
                            traceback.print_exc()  # トレースバックを出力するためのこの行を追加
                            retry_count += 1
                        finally:
                            print("finalllyを通過")
                            log_to_file("finalllyを通過")
                            # 何かしらのクリーンアップや終了処理が必要な場合

                print("page数：", page)
                log_to_file("page数：", page)

                
                # box_itemsは見つかった要素のリストまたは空のリストです
                print("box_item数：", len(box_items))
                log_to_file("box_item数：", len(box_items))

                count_sum += len(box_items)
                print("合計item：", count_sum)
                log_to_file("合計item：", count_sum)

                # box_itemsは見つかった要素のリストまたは空のリストです
                # for item in box_items:

                # box_itemsは見つかった要素のリストまたは空のリストです
                for j in range(len(box_items)):
                    # 各要素の処理
                    # "a"タグを取得
                    a_tags = box_items[j].find_elements(By.TAG_NAME, 'a')
                    if a_tags:
                        # "a"タグが見つかった場合は最後の要素を取得
                        a_tag = a_tags[-1]
                        
                        # "href"属性の中身を取得
                        fin_url_detail = a_tag.get_attribute('href')
                        print("fin_url_detail:", fin_url_detail)
                        log_to_file("fin_url_detail",fin_url_detail)
                        # 以下の処理に続く...
                    else:
                        print("aタグが見つかりませんでした。")

                    # fin_url_detail = url + href_content

                    # 取得したhrefの中身を出力
                    # print("fin_url_detail",fin_url_detail)
                    log_to_file("fin_url_detail",fin_url_detail)

                    # URLからページのHTMLを取得
                    response = requests.get(fin_url_detail, headers=headers)
                    response.encoding = response.apparent_encoding

                    # BeautifulSoupを使ってHTMLを解析
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # 1秒待つ
                    # time.sleep(3)

                    # <h3>タグの中のテキストを取得
                    company_name_tag = soup.find('h3', class_='no-margin')

                    # テキストが存在する場合と存在しない場合で条件分岐
                    if company_name_tag:
                        company_name = company_name_tag.text
                        print("企業名：", company_name)
                        log_to_file("企業名：", company_name)
                    else:
                        company_name = ""
                        print("企業名が見つかりませんでした。")
                        log_to_file("企業名が見つかりませんでした。")

                    # <div>タグの中のテキストを取得
                    address_tag = soup.find('div', class_='font-copy-400 text-navy-70')

                    # テキストが存在する場合と存在しない場合で条件分岐
                    if address_tag:
                        address = address_tag.text.strip()
                        # 取得したテキストを出力
                        print(address)
                        log_to_file(address)
                    else:
                        address = ""
                        print("住所が見つかりませんでした。")
                        log_to_file("住所が見つかりませんでした。")


                    # <a>タグの中のhref属性の値を取得
                    website_link_tag = soup.find('a', class_='inline-flex items-center gap-1 font-display-400 overflow-hidden')

                    # テキストが存在する場合と存在しない場合で条件分岐
                    if website_link_tag:
                        website_link = website_link_tag.get('href')
                        # 取得したhrefの値を出力
                        print("website_link：", website_link)
                        log_to_file("website_link：", website_link)
                    else:
                        website_link = ""
                        print("Websiteリンクが見つかりませんでした。")
                        log_to_file("Websiteリンクが見つかりませんでした。")

                    # <span>タグの中のテキストを取得
                    span_text_tag = soup.find('span', class_='font-display-400')

                    # テキストが存在する場合と存在しない場合で条件分岐
                    if span_text_tag:
                        span_text = span_text_tag.text
                        # 取得したテキストを出力
                        print("span_text：", span_text)
                        log_to_file("span_text：", span_text)
                    else:
                        span_text = ""
                        print("span_textが見つかりませんでした。")
                        log_to_file("span_textが見つかりませんでした。")

                    # <div>タグの中のテキストを取得
                    contact_name_tag = soup.find('div', {'class': 'font-display-300', 'data-test': 'contact-name'})

                    # テキストが存在する場合と存在しない場合で条件分岐
                    if contact_name_tag:
                        contact_name = contact_name_tag.text
                        print("contact_name：", contact_name)
                        log_to_file("contact_name：", contact_name)
                    else:
                        contact_name = ""
                        print("値が存在しません。")
                        log_to_file("値が存在しません。")
                        
                    max_retries = 20
                    retry_count = 0
                    
                    
                    while retry_count < max_retries:

                        try:
                            
                            # Chrome WebDriverのインスタンスを作成
                            driver1 = webdriver.Chrome(options=options)

                            # ブラウザで指定されたURLを開く
                            driver1.get(fin_url_detail)

                            # Cookieの同意ボタンが表示されるまで待つ
                            wait = WebDriverWait(driver1, 10)
                            button_element = wait.until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogFooterButtonSaveSettings")))

                            # JavaScriptを使用してCookieの同意ボタンをクリック
                            driver1.execute_script("arguments[0].click();", button_element)
                            time.sleep(3)

                            # 電話番号のボタンが表示されるまで待つ
                            phone_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "phone-button")))

                            # JavaScriptを使用して電話番号のボタンをクリック
                            driver1.execute_script("arguments[0].click();", phone_button)

                            # 電話番号の <a> タグの中の href 属性を取得
                            phone_number_a_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'copy-button')))
                            phone_number_href = phone_number_a_tag.get_attribute('href')
                            # "tel:" を削除して電話番号だけを取得
                            phone_number_cleaned = phone_number_href.replace("tel:", "")

                            # 取得した href を出力
                            print("電話番号の href 属性:", phone_number_cleaned)                            
                            log_to_file("電話番号の href 属性:", phone_number_cleaned)           
                            break


                        except TimeoutException:
                            # TimeoutExceptionが発生した場合、つまりボタンが見つからない場合やタイムアウトした場合
                            print("Cookieの同意ボタンまたは電話番号のボタンが見つかりませんでした。")
                            log_to_file("Cookieの同意ボタンまたは電話番号のボタンが見つかりませんでした。")
                            phone_number_cleaned = ""
                            retry_count += 1
                        except StaleElementReferenceException:
                            # 要素がStaleになった場合、再取得を試みる
                            print("Stale Element Reference Exception 発生")  
                            log_to_file("Stale Element Reference Exception 発生")  
                            phone_number_cleaned = ""
                            retry_count += 1
                        except Exception as e:
                            # 他の例外が発生した場合
                            print("エラーが発生しました:", str(e))
                            log_to_file(f"エラーが発生しました: {type(e).__name__}, {str(e)}")
                            traceback.print_exc()  # トレースバックを出力するためのこの行を追加
                            phone_number_cleaned = ""
                            retry_count += 1
                        finally:
                            print("1つ目のデータ取得終了")
                            log_to_file("1つ目のデータ取得終了")
                            # 何かしらのクリーンアップや終了処理が必要な場合
                            # ドライバーを終了
                            close_driver(driver1)

                                    # データを辞書に格納
                    data = {
                        '製品大カテゴリ': item[0],
                        '製品中カテゴリ': item[1],
                        '製品小カテゴリ':a_text,
                        '製品カテゴリページURL（=製品中カテゴリページ）': categoty_url,
                        '製品名': span_text,
                        '製品ページURL': fin_url_detail,
                        '企業名': company_name,
                        '企業サイトURL': website_link,
                        '企業担当者（無いこともある）': contact_name,
                        '企業電話番号': phone_number_cleaned,
                        '企業住所': address
                    }
                    # 既存のCSVファイルが存在する場合
                    if os.path.isfile(csv_filename):
                        # 既存のデータを読み込み
                        df_existing = pd.read_csv(csv_filename)
                        # 新しいデータをデータフレームに追加
                        df_new = pd.DataFrame([data])
                        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                        # データをCSVファイルに書き込み
                        df_combined.to_csv(csv_filename, index=False, encoding='utf-8')
                    else:
                        # 既存のCSVファイルが存在しない場合、新しいデータを直接書き込み
                        df = pd.DataFrame([data])
                        df.to_csv(csv_filename, index=False, encoding='utf-8')
                            

        except Exception as e:
            # 他のすべての例外を処理
            print("エラーが発生しました:", str(e))
            log_to_file("エラーが発生しました:", str(e))
    
if __name__ == "__main__":
        # ループの外で WebDriver のインスタンスを作成
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(options=options)

    try:
        scrape_wlw_data()
    finally:
        # スクレイピングプロセスが完了した後に WebDriver のインスタンスを閉じる
        close_driver(driver)
