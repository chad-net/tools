from wiki.constants import paths
from wiki.db.sort import normalize_text
from . import link_utils

def wrap_text_for_javascript(text):
	return '"' + text.replace('\\"', '"').replace('"', '\\"') + '",\n'


def prepare_text_for_search(text):
	# todo: < and > should be escaped
	text = text.replace('&', 'and') # todo: improve
	return normalize_text(text, ['/', ' '])


def get_head_template():
	with open(paths.TEMPLATES_DIR / 'HEAD_SEARCH.html', 'r', encoding='utf8') as head:
		return '\n'.join(head.read().splitlines())


def get_new_tab_line(opens_in_new_tab):
	if opens_in_new_tab:
		return '"1",\n'

	return '"",\n'

def make_link_html(link):
	html = []

	description_delimiter = ' ' if link['description'] != '' else ' '

	html.append(wrap_text_for_javascript(prepare_text_for_search(link['title'] + description_delimiter + link['description'])))
	html.append(wrap_text_for_javascript(link['title']))
	html.append(wrap_text_for_javascript(link['description']))

	url, opens_in_new_tab = link_utils.update_url_and_check_if_opens_in_new_tab(link['url'])

	html.append(wrap_text_for_javascript(url))
	html.append(wrap_text_for_javascript(link_utils.get_link_icon_filename(url)))

	html.append(get_new_tab_line(opens_in_new_tab))

	return html


def write_search_file(filepath, html):
	with open(filepath, 'w', encoding='utf8') as file:
		file.writelines(html)

# todo: add which directories a link is under?
def make_search_page(links):
	html = []

	html.extend(get_head_template())

	for link in links:
		html.extend(make_link_html(link))

	# close js array
	html.append('];\n</script>\n</body>\n</html>')

	write_search_file(paths.WIKI_DIR / 'search.html', html)
