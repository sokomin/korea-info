import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import os

dir_name = 'out/origin/'
dir_name_f = 'out/origin_front/'
Path(dir_name).mkdir(parents=True, exist_ok=True)

exist = 7300
with open('exist.txt', 'r') as f:
    line = f.read()
    if int(line) > 0:
        exist = int(line)

exist_to = exist + 10
overwrite = 0

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)

for dr in range(exist,exist_to):
    try:
        print(str(dr) + "is crowing...")
        url = 'http://redstone.logickorea.co.kr/notice/noticeboard/view.aspx?sqn=' +str(dr)
        response = requests.get(url)
        response.raise_for_status()
        html_ranking = response.text

        soup = BeautifulSoup(html_ranking, 'html.parser')
        # title = soup.title.string
        # print(title)
        table = soup.find('table')
        try:
            url2 = 'http://redstone.logickorea.co.kr/notice/updateboard/view.aspx?sqn=' +str(dr)
            response2 = requests.get(url2)
            response2.raise_for_status()
            html_ranking2 = response2.text

            soup2 = BeautifulSoup(html_ranking2, 'html.parser')
            table2 = soup2.find('table')
        except:
            print(str(dr) + "fail to get updateboard.")

        data = str(table)
        # どっちのパスか判別つかないのでif文で両方比較
        data2 = str(table2)
        if len(data) < len(data2):
            print(str(dr) + "is updateboard.")
            data = data2
            soup = soup2

        # ファイル量多くなるとGitHubから怒られるので最新100件のみ保存
        # gitのcommitlog辿れば過去のデータ手に入るしいいよね理論
        del_file = dr - 100
        last_file = dir_name_f + str(del_file) + ".html"
        print("delete:" + str(last_file))
        if os.path.exists(last_file):
            os.remove(last_file)

        data = re.sub('http://redstone.logickorea.co.kr/notice/noticeboard/view.aspx?sqn=','https://sokomin.github.io/korea-info/out/origin_front/', data)
        data = re.sub('http://redstone.logickorea.co.kr/notice/updateboard/view.aspx?sqn=','https://sokomin.github.io/korea-info/out/origin_front/', data)
        # 画像パス変更（ローカルでしか表示されない…）
        data = re.sub('<img src="','<img src="http://redstone.logickorea.co.kr', data)
        data = re.sub('<img src="','<img src="https://sokomin.github.io/korea-info/out/origin_front/img/', data)

        imgs = soup.find_all('img',src=re.compile('^https://sokomin.github.io/korea-info/out/origin_front/img/'))
        for img in imgs:
                print(img['src'])
                r = requests.get(img['src'])
                with open(str(dir_name_f + '/ADDONS2/')+str(uuid.uuid4())+str('.png'),'wb') as file:
                        file.write(r.content)

        # エラー処理
        if data.find('<script type="text/javascript">document.location.href="/notice/updateboard/view.aspx?sqn=') > 0:
            print(str(dr) + "is not exist page.")
            continue
        if data.find('<script type="text/javascript">document.location.href="/notice/noticeboard/view.aspx?sqn=') > 0:
            print(str(dr) + "is not exist page.")
            continue
        # Not foundならそこで止める

        with open(dir_name + str(dr) + ".html", "w", encoding='utf-8') as f:
            f.write(str(data))
        overwrite = dr
        with open(dir_name_f + str(dr) + ".html", "w", encoding='utf-8') as f:
            f.write(str(data))
    except:
        print(str(dr) + " is not found.")


with open('exist.txt', "w", encoding='utf-8') as f:
    f.write(str(overwrite))


