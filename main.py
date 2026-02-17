import os
import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from zenrows import ZenRowsClient
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--lang=zh-TW')
chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(
    chrome_options=chrome_options, executable_path=chromedriver)

game_name = []
html_num = []
price = []
send_to_dis_game = []
send_to_dis_now_price = []
send_to_dis_his_price = []
send_to_dis_his_date = []


url = 'https://store.steampowered.com/wishlist/profiles/76561198346512176/#sort=order'
browser.get(url)
time.sleep(3)

temp = browser.find_elements(By.CLASS_NAME, "title")

for i in range(len(temp)):
    text = temp[i].get_attribute("outerHTML")
    # print(text)
    game_name.append(text.split('class="title">')[1].split(
        '\n\t\t\t\t\t')[1].split('\n\t\t\t\t</a>')[0])
    html_num.append(text.split('app/')[1].split('/?')[0])

# print(game_name)
# print(html_num)

temp2 = browser.find_elements(By.CLASS_NAME, 'mid_container')

for i in range(len(temp2)):
    text2 = temp2[i].get_attribute("outerHTML")
    # print(text2)
    if 'original_price' in text2:
        temp = 'Y'
        price.append(temp)
    else:
        temp = 'N'
        price.append(temp)
# print(price)

temp3 = browser.find_elements(By.CLASS_NAME, 'wishlist_header')
for i in range(len(temp3)):
    text3 = temp3[i].get_attribute("outerHTML")
    name = text3.split('<h2>')[1].split('</h2>')[0].split("'s")[0]

zen_url = []
for i in range(len(price)):
    if 'Y' in price[i]:
        #print(game_name[i], ',', html_num[i], ',', price[i])
        temp_url = 'https://steamdb.info/app/' + html_num[i] + '/'
        # print(temp_url)
        zen_url.append(temp_url)
        send_to_dis_game.append(game_name[i])

if len(zen_url) > 0:
    send_to_dis_cont = f'{name}您好，目前願望清單中共有{len(zen_url)}款遊戲在特價，快來確認吧！\n'
else:
    send_to_dis_cont = f'{name}您好，目前願望清單中沒有遊戲在特價，下次再來吧！\n'
print(send_to_dis_game, zen_url,end=', ')

proxy = os.environ['ZENROWS_PROXY']
client = ZenRowsClient(proxy)
for j in range(len(zen_url)):
    time.sleep(5)
    url = zen_url[j]
    params = {"js_render": "true","wait":"1000"}
    #params = {"js_render": "true", "antibot": "true", "premium_proxy": "true"}
    response = client.get(url, params=params)
    content = response.text

    ctr = 1
    while True:
        if '"code":"RESP001"' in content:
            time.sleep(10)
            response = client.get(url, params=params)
            content = response.text
            ctr +=1
        else:
            break
    split_text = content.split('<tr>')
    #print(content,'\n')
    print(f"{ctr=}")
    status = 0
    for i in range(len(split_text)):
        if 'Taiwan Dollar\n</td>' in split_text[i]:
            data = split_text[i]
            #print(data)
            if ' at ' not in data.split('NT$ ')[1]:
                now_price = data.split('NT$ ')[1].split('</td')[
                    0] + '(SteamDB尚未更新)'
            else:
                now_price = data.split('NT$ ')[1].split(' at')[0]
            his_price = data.split('NT$ ')[2].split(' at')[0]
            print(f"{j+1}:",end="")
            print(send_to_dis_game[j],now_price, his_price)
            send_to_dis_now_price.append(now_price)
            send_to_dis_his_price.append(his_price)
            status = 1
            break
    if status == 0:
        print(content,'\n')

if len(zen_url) > 0:
    for i in range(len(send_to_dis_now_price)):
        send_to_dis_cont += f'{i+1}. ' + send_to_dis_game[i] + \
            '，目前特價 $'+send_to_dis_now_price[i] + \
            '，歷史最低 $'+send_to_dis_his_price[i]+'\n'
print(send_to_dis_cont)

# Discord part
url = os.environ['DISCORD_WEBHOOK_URL']
data = {"content": send_to_dis_cont}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.status_code)
