import re
from natsort import natsorted
from unidecode import unidecode
from wiki.constants import options

def normalize_text(text, safe_characters):
	text = unidecode(text).lower()
	normalized_text = []

	for char in text:
		if char.isalnum() or char in safe_characters:
			normalized_text.append(char)

	# remove extra spaces
	return ' '.join(''.join(normalized_text).split())


# split the string into a list of numbers and non-numbers, which python's
# sorted function uses to perform a "natural sort"
def natural_key(text):
	parts = re.split(r'(\d+)', text)

	result = []

	for part in parts:
		if part.isdigit():
			result.append(int(part))
		else:
			result.append(part)

	return result


# sort the list in something akin to how gnu's sort does it
# natsorted may become a performance bottleneck
def sort_db(database, field_to_sort_by):
	if options.USE_OWN_SORTING_METHOD:
		# LOCAL HAND-MADE NATURAL SORT
		return sorted(database, key=lambda x: natural_key(normalize_text(x[field_to_sort_by], [' '])))

	# EXTERNAL DEPENDENCY OPTION
	return natsorted(database, key=lambda x: normalize_text(x[field_to_sort_by], [' ']))
