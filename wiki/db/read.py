def parse_field(field, line):
	if field['list']:
		return [x.strip() for x in line.strip().split(',')]

	return line.strip()


def process_lines(field_count, fields, file):
	records = []
	record = {}

	for line_number, line in enumerate(file, start=1):
		delimiter_line = 0
		if line_number % field_count == delimiter_line:
			records.append(record)
			record = {}
		else:
			# get current field type. line_number-1 because list index starts at 0
			field = fields[(line_number - 1) % field_count]
			record[field['name']] = parse_field(field, line)

	# if last line wasn't blank, add record like this
	if record:
		records.append(record)

	return records


def read_db_file(filename, fields):
	# add 1, taking into account the last delimiter/blank line
	field_count = len(fields) + 1

	with open(filename, 'r', encoding='utf8') as file:
		records = process_lines(field_count, fields, file)

	return records
