from bs4 import BeautifulSoup
import requests
from feedgen.feed import FeedGenerator

# Webページから情報を取得
url = 'https://sokomin.github.io/korea-info/out/origin_front/7903.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# RSSフィードの設定
fg = FeedGenerator()
fg.title('공지사항')
fg.link(href='URL_TO_YOUR_WEBSITE') # ウェブサイトのURLを設定
fg.description('공지사항のRSSフィード')

# 記事のタイトル、登録日、本文の一部を追加
rows = soup.find_all('tr')
for row in rows:
    # タイトルと登録日を取得
    title_cell = row.find('th', class_='title')
    title = title_cell.text.strip() if title_cell else None
    date_cell = row.find('td', class_='date_txt')
    date = date_cell.text.strip() if date_cell else None
    
    # 本文の一部を取得（最初のp要素のテキストを使用）
    p_element = soup.find('p')
    article_excerpt = p_element.text.strip()[:200] if p_element else None

    if title and date and article_excerpt:
        fe = fg.add_entry()
        fe.title(title)
        fe.pubdate(date) # 登録日を公開日として設定
        fe.description(article_excerpt) # 本文の一部を説明として設定

# RSSフィードをファイルに保存
fg.rss_file('rss.xml')