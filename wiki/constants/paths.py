from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
WIKI_DIR = PROJECT_DIR.parent.parent
FILES_DIR = WIKI_DIR / 'files'
TOOLS_DIR = WIKI_DIR / 'tools'
TEMPLATES_DIR = TOOLS_DIR / 'templates'
BACKUPS_DIR = TOOLS_DIR / 'backups'
DEBUG_DIR = PROJECT_DIR / 'debug'
