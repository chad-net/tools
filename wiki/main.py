import time
import sys
from .constants import version, paths, options
from .logging import log
from .db.backup import backup_db
from .db.read import read_db_file
from .db.write import write_db_file
from .db.sort import sort_db
from .site.update_index import update_index_page
from .site.categories import make_cat_pages
from .site.search import make_search_page
from .site.change_file_permissions import change_file_permissions
from .performance_debug import debug, remove_debug_files


def run_wiki_system():
	# move this elsewhere
	news_text = None
	if 'news' in sys.argv:
		try:
			news_text = input('News: ')
		except KeyboardInterrupt:
			print('\n\033[38;2;255;165;0mINFO: Cancelled\033[0m')
			return

	start_time = time.perf_counter()

	module_timer = start_time

	backup_db(paths.WIKI_DIR, 'db.chad')
	backup_db(paths.WIKI_DIR, 'cat.chad')
	module_timer = log.module_execution_time(module_timer, 'Backed up database files')

	link_fields = [
		{'name': 'title', 'list': False},
		{'name': 'url', 'list': False},
		{'name': 'cats','list': True},
		{'name': 'description', 'list': False},
	]

	cat_fields = [
		{'name': 'title', 'list': False},
		{'name': 'url', 'list': False},
		{'name': 'parents', 'list': True},
	]

	links_db = read_db_file(paths.WIKI_DIR / 'db.chad', link_fields)
	links_db = sort_db(links_db, 'title')
	formatted_total_link_count = f'{len(links_db):,}'
	module_timer = log.module_execution_time(module_timer, 'Sorted db.chad')

	cats_db = read_db_file(paths.WIKI_DIR / 'cat.chad', cat_fields)
	cats_db = sort_db(cats_db, 'title')
	formatted_total_cat_count = f'{len(cats_db):,}'
	module_timer = log.module_execution_time(module_timer, 'Sorted cat.chad')

	write_db_file(paths.WIKI_DIR / 'db.chad', links_db)
	write_db_file(paths.WIKI_DIR / 'cat.chad', cats_db)
	module_timer = log.module_execution_time(module_timer, 'Updated database files')

	update_index_page(formatted_total_link_count, news_text)
	module_timer = log.module_execution_time(module_timer, 'Updated index.html')

	make_cat_pages(cats_db, links_db)
	module_timer = log.module_execution_time(module_timer, 'Created categories')

	make_search_page(links_db)
	module_timer = log.module_execution_time(module_timer, 'Set up search')

	change_file_permissions()
	module_timer = log.module_execution_time(module_timer, 'Changed file permissions')

	print(log.bold_text('-- Stats --'))
	print(f'Links: {log.bold_text(formatted_total_link_count)}')
	print(f'Categories: {log.bold_text(formatted_total_cat_count)}')

	end_time = time.perf_counter()
	execution_time = f'{(end_time - start_time):.2f}s'
	print(f'Completed: {log.bold_text(execution_time)}')


###############################################################################
try:
	print(log.gold_text(f'CHADNET SYSTEM ALPHA: WIKI SYSTEM v{version.VERSION}'))
	remove_debug_files()

	if not options.IS_DEBUG_MODE:
		run_wiki_system()
	else:
		debug('run_wiki_system()')

except Exception as e:
	log.error_and_exit(str(e))
