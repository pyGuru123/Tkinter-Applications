import random
import requests
import lxml
from bs4 import BeautifulSoup

user_agents = [
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.165 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.148 Safari/537.36')  # chrome
]

user = input('Enter profile user name : ')
if user:
	url = f"https://www.instagram.com/{user}/"
	header = {'User-Agent': random.choice(user_agents)}
	
	response = requests.get(url, headers=header)
	if response.ok:
		html = response.text
		soup = BeautifulSoup(html, 'lxml')
		
		title = soup.find('meta', attrs={'property':'og:title'})
		image = soup.find('meta', attrs={'property':'og:image'})
		desc = soup.find('meta', attrs={'property':'og:description'})

		name = title['content'].split('@')[0].strip('(').strip()
		info = desc['content'].split('-')[0]
		followers = info.split('Followers')[0].strip()
		following = info.split('Following')[0].split('Followers')[1].strip(',')
		posts = info.split('Following')[1].split('Posts')[0]

		print(f'Profile Name : {name}')
		print(f'Followers : {followers}')
		print(f'Following : {following}')
		print(f'Posts : {posts}')
		
		print('Downloading profile image....')
		url = image['content']
		r = requests.get(url)
		with open('profile.jpg', 'wb') as file:
			file.write(r.content)