import cProfile
import pstats
from .constants import paths
from .logging import log

OUTPUT_DATA_FILE = paths.DEBUG_DIR / 'output.dat'
OUTPUT_TIME_FILE = paths.DEBUG_DIR / 'output_time.txt'
OUTPUT_CALLS_FILE = paths.DEBUG_DIR / 'output_calls.txt'

def debug(function_to_debug):
	if not paths.DEBUG_DIR.exists():
		paths.DEBUG_DIR.mkdir()
		log.info(f'Created debug directory: {paths.DEBUG_DIR}')

	cProfile.run(function_to_debug, OUTPUT_DATA_FILE)

	with open(OUTPUT_TIME_FILE, 'w', encoding='utf8') as debug_file:
		stats = pstats.Stats(str(OUTPUT_DATA_FILE), stream=debug_file)
		stats.sort_stats('time').print_stats()

	with open(OUTPUT_CALLS_FILE, 'w', encoding='utf8') as debug_file:
		stats = pstats.Stats(str(OUTPUT_DATA_FILE), stream=debug_file)
		stats.sort_stats('calls').print_stats()

	log.info('Generated debug info files')

def remove_debug_files():
	is_files_deleted = False

	if OUTPUT_DATA_FILE.exists():
		OUTPUT_DATA_FILE.unlink()
		is_files_deleted = True

	if OUTPUT_TIME_FILE.exists():
		OUTPUT_TIME_FILE.unlink()
		is_files_deleted = True

	if OUTPUT_CALLS_FILE.exists():
		OUTPUT_CALLS_FILE.unlink()
		is_files_deleted = True

	if paths.DEBUG_DIR.exists():
		paths.DEBUG_DIR.rmdir()
		is_files_deleted = True

	if is_files_deleted:
		log.info('Deleted debug files')
