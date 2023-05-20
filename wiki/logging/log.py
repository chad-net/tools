import sys
import time
import traceback

def bold_text(text):
	return f'\033[1m{text}\033[0m'


def gold_text(text):
	return f'\033[1;33m{text}\033[0m'


def info(text):
	# orange ansi escape code
	print(f'\033[38;2;255;165;0mINFO: {text}\033[0m')


#def debug(text):
#	print(f'{bold_text("DEBUG:")} {text}')


def error_and_exit(text):
	print(f'\033[1;31mERROR: {str(text)}\033[0m')
	traceback.print_exc()
	sys.exit(1)

def module_execution_time(module_time, text):
	current_time = time.perf_counter()
	elapsed_time = current_time - module_time
	print(f'[{elapsed_time:.2f}] {text}')
	return current_time
