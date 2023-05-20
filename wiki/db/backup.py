from datetime import datetime
from shutil import copyfile
from wiki.constants import paths
from wiki.logging import log

def backup_db(directory_path, filename):

	if not paths.BACKUPS_DIR.exists():
		paths.BACKUPS_DIR.mkdir()
		log.info(f'Created backups directory: {paths.BACKUPS_DIR}')

	date = datetime.now().strftime('%d-%m-%Y')

	filename_parts = filename.split('.')
	backup_filename = f'{filename_parts[0]}{date}.{filename_parts[1]}'

	copyfile(directory_path / filename, paths.BACKUPS_DIR / backup_filename)
	#copyfile(paths.WIKI_DIR / 'db.chad', paths.BACKUPS_DIR / f'db{date}.chad')
	#copyfile(paths.WIKI_DIR / 'cat.chad', paths.BACKUPS_DIR / f'cat{date}.chad')
