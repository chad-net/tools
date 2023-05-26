from datetime import datetime
from wiki.constants import paths
from .categories import escape_html

def update_index_page(total_link_count, news_text):
	utc_date = datetime.utcnow()
	stats_date = utc_date.strftime('%B %d, %Y, at %H:%M UTC')
	stats_replacement = f'  <p id="stats">Total links: <strong>{total_link_count}</strong>. Last updated on {stats_date}.</p>\n'
	if news_text:
		news_date = utc_date.strftime('%B %d')
		news_replacement = f'  <p id="news"><strong>News:</strong> (Also on <a href="https://twitter.com/realChadnet" target="_blank"><img class="icon" src="files/twitter.svg" alt="Twitter"></a> <a href="https://t.me/Chadnet" target="_blank"><img class="icon" src="files/telegram.svg" alt="Telegram"></a>) {news_date}: {escape_html(news_text)}</p>\n'

	with open(paths.WIKI_DIR / 'index.html', 'r', encoding='utf8') as file:
		index_page_html = file.readlines()

	for line_number, line in enumerate(index_page_html):
		if '<p id="stats">' in line:
			index_page_html[line_number] = stats_replacement
			continue
		if news_text and '<p id="news">' in line:
			index_page_html[line_number] = news_replacement
			continue

	with open(paths.WIKI_DIR / 'index.html', 'w', encoding='utf8') as file:
		file.writelines(index_page_html)
