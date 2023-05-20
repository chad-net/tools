from wiki.constants import paths
from . import link_utils

ESCAPE_DICT = {
	'&': '&amp;',
	'"': '&quot;',
	'<': '&lt;',
	'>': '&gt;',
	'’': "'",
	'‘': "'",
	'…': '...',
	'”': '&quot;',
	'“': '&quot;'
}

def escape_html(text):
	return ''.join(ESCAPE_DICT.get(char, char) for char in text)


def join_cats_and_links(cats, links):
	cat_urls = {cat['url']: cat for cat in cats}

	for cat in cats:
		# create lists for certain elements
		cat.update({'children': [], 'links': [], 'starred_links': []})

	for cat in cats:
		# loop over parent category url and append the current category as one of
		# its children
		for parent_url in cat['parents']:
			if parent_url in cat_urls:
				cat_urls[parent_url]['children'].append({'title': cat['title'], 'url': cat['url']})

	for link in links:
		# loop over every category link is under
		for cat_url in link['cats']:
			is_starred_link = cat_url.startswith('~')
			cat_url = cat_url.lstrip('~')
			# loop over all category and find the current one
			if cat_url in cat_urls:
				# append to appropriate link list
				cat_urls[cat_url]['starred_links' if is_starred_link else 'links'].append(link)
	return cats


def make_link_html_string(link, icon_filename):
	url, opens_in_new_tab = link_utils.update_url_and_check_if_opens_in_new_tab(link['url'])

	if icon_filename is None:
		icon_filename = link_utils.get_link_icon_filename(url)

	html_string = f'    <li><img src="{icon_filename}" draggable="false"><a href="{url}"'

	if opens_in_new_tab:
		html_string += ' target="_blank"'

	html_string += f'>{escape_html(link["title"])}</a>'

	if link['description']:
		html_string += f' {escape_html(link["description"])}'

	html_string += '</li>\n'

	return html_string


def make_cat_stats_string(cat_count, link_count):
	cat_stats_icon = '<img src="folder.png" draggable="false" class="stats">'
	link_stats_icon = '<img src="link.png" draggable="false" class="stats">'

	cat_stats_string = ''
	if cat_count:
		cat_stats_string += f' {cat_count} {cat_stats_icon}'

	if link_count:
		cat_stats_string += f' {link_count} {link_stats_icon}'

	if cat_stats_string:
		return f' ({cat_stats_string.strip()})'

	return None


def make_child_cat_html(cats, cat):
	for find_cat in cats:
		if cat['url'] == find_cat['url']:
			cat_count = len(find_cat['children'])
			link_count = len(find_cat['links']) + len(find_cat['starred_links'])
	html = f'    <li><img src="folder.png" draggable="false"><a href="{cat["url"]}.html">{escape_html(cat["title"])}</a>'

	# check what stats to add next to category, depending on its contents
	cat_stats_string = make_cat_stats_string(cat_count, link_count)
	if cat_stats_string:
		html += cat_stats_string

	html += '</li>\n'

	return html


def get_head_template():
	with open(paths.TEMPLATES_DIR / 'HEAD_CAT.html', 'r', encoding='utf8') as head:
		return head.read().splitlines()


def make_cat_head(head_html, title, link_count):
	html = []

	for line in head_html:
		html.append(
			line.replace('CHADNET_SYSTEM_ALPHA_TITLE',title)
			.replace('CHADNET_SYSTEM_ALPHA_LINKS', link_count)
			+ '\n')

	html.append('  <ul class="category">\n')

	return html


def write_category_file(filepath, html):
	with open(filepath, 'w', encoding='utf8') as file:
		file.writelines(html)


# Categories are always organized in this manner:
# * 1 Starred links
# * 2 Categories
# * 3 Links
# create all category files and add child categories and links
def make_cat_pages(cats_db, links_db):
	cats = join_cats_and_links(cats_db, links_db)

	head_html = get_head_template()

	for cat in cats:
		html = []

		category_link_count = str(len(cat['links']) + len(cat['starred_links']))

		html.extend(make_cat_head(head_html, escape_html(cat['title']), category_link_count))

		for starred_link in cat['starred_links']:
			html.append(make_link_html_string(starred_link, 'star.png'))

		for child_cat in cat['children']:
			html.append(make_child_cat_html(cats, child_cat))

		for link in cat['links']:
			html.append(make_link_html_string(link, None))

		html.append('  </ul>\n</body>\n</html>')

		#print(html)
		write_category_file(paths.WIKI_DIR / f'{cat["url"]}.html', html)
