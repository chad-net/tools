from datetime import datetime
import re
from wiki.constants import paths

def update_index_page(total_link_count):
	date = datetime.utcnow().strftime('%B %d, %Y, at %H:%M UTC')
	replacement = f'<p>Total links: <strong>{total_link_count}</strong>. Last updated on {date}.</p>'

	with open(paths.WIKI_DIR / 'index.html', 'r+', encoding='utf8') as file:
		content = file.read()
		content_new = re.sub(r'<p>Total links: <strong>.*<\/p>', replacement, content)

		file.seek(0)
		file.write(content_new)
		file.truncate()
