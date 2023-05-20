def get_link_icon_filename(url):
	if url.startswith('https://www.youtube.com'):
		icon_filename = 'yt.svg'

	elif url.startswith('http'):
		icon_filename = 'globe.svg'

	elif url.startswith('files'):
		if url.endswith(('jpg', 'jpeg', 'png', 'gif')):
			icon_filename = 'painting.png'

		elif url.endswith(('mp4', 'webm')):
			icon_filename = 'video.png'

		elif url.endswith('mp3'):
			icon_filename = 'speaker.png'

		else:
			icon_filename = 'doc.png'

	else:
		icon_filename = 'chad-square.png'

	return icon_filename

def update_url_and_check_if_opens_in_new_tab(url):
	opens_in_new_tab = url.startswith('!')
	url = url.lstrip('!') if opens_in_new_tab else url
	return url, opens_in_new_tab
