from datetime import datetime
from wiki.constants import paths

def update_index_page(total_link_count):
	date = datetime.utcnow().strftime('%B %d, %Y, at %H:%M UTC')
	replacement = f'  <p id="stats">Total links: <strong>{total_link_count}</strong>. Last updated on {date}.</p>\n'

	with open(paths.WIKI_DIR / 'index.html', 'r', encoding='utf8') as file:
		index_page_html = file.readlines()

	for line_number, line in enumerate(index_page_html):
		if '<p id="stats">' in line:
			index_page_html[line_number] = replacement
			break

	with open(paths.WIKI_DIR / 'index.html', 'w', encoding='utf8') as file:
		file.writelines(index_page_html)
