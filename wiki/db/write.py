def make_file_line(value):
	if isinstance(value, list):
		value = ', '.join(map(str, value))

	return f'{value}\n'


def write_db_file(filename, data):
	lines = []

	for record in data:
		for _, value in record.items():
			lines.append(make_file_line(value))
		# delimiter
		lines.append('\n')

	with open(filename, 'w', encoding='utf8') as file:
		file.writelines(lines)
