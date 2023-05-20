from wiki.constants import paths

def change_file_permissions():
	# loop over every file in wiki/
	for item in paths.WIKI_DIR.rglob('*'):
		# skip tools/ dir
		if 'tools' in item.parts:
			continue

		if item.is_file():
			item.chmod(0o644)

	paths.FILES_DIR.chmod(0o755)
