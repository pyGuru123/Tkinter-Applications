import mechanize
from bs4 import BeautifulSoup

def scrape_phone_info(phone):
	url = "https://www.findandtrace.com/trace-mobile-number-location"

	try:
		br = mechanize.Browser()
		br.set_handle_robots(False) # ignore robots
		br.open(url)
		br.select_form(name="trace")
		br["mobilenumber"] = phone
		res = br.submit()

		soup = BeautifulSoup(res.read(),'html.parser')
		tbl = soup.find_all('table',class_='shop_table')
		data = tbl[0].find('tfoot')

		result = ''

		count = 0
		for tr in data:
			count += 1
			if count in(1,4,6,8):
				continue
			th = tr.find('th')
			td = tr.find('td')
			result += f"{th.text} {td.text}\n\n"

		data = tbl[1].find('tfoot')
		count = 0
		for tr in data:
			count += 1
			if count in (2,20,22,26):	
				th = tr.find('th')
				td = tr.find('td')
				result += f"{th.text} {td.text}\n\n"

		return result
	except:
		return 'ConnectionError'