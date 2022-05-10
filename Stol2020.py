import requests
from bs4 import BeautifulSoup
import csv
import re
import schedule
import time
from datetime import datetime	


def getLinks():
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"}
	page = requests.get("https://stol.it/", headers=headers)
	soup = BeautifulSoup(page.content, "html.parser")
	
	global links
	links = []
	
	for link in soup.findAll('a', href=re.compile('^/artikel/')):
		links.append(link.get("href"))
	
	string ="https://stol.it"
	links = [string + x for x in links]
	links = list(dict.fromkeys(links))

def createArticle(url_input):
	global url
	global title
	global subtitle
	global rubrik
	global date
	global category
	global text
	global author
	global timestamp

	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"}
	page = requests.get(url_input, headers=headers)
	url = url_input
	soup = BeautifulSoup(page.content, "html.parser")
	[s.extract() for s in soup('script')]

	try:
		title = soup.find("h1",attrs={"class": "single-title"}).get_text().replace("  ", "").replace("\n", "")
	except:
		title = "No title"

	try:	
		subtitle = soup.find("p",attrs={"class": "uk-text"}).get_text().replace("  ", "").replace("\n", "")
	except:
		subtitle = "No subtitle"#

	rubrik = url.split("/")[4:5]

	try:	
		date = soup.find("div",attrs={"class": "date"}).get_text().replace("  ", "").replace("\n", "")
	except:
		date = "No date"	

	try:
		category = soup.find("div",attrs={"class": "category"}).get_text().replace("  ", "").replace("\n", "")
	except:
		category = "No category"

	try:	
		text = soup.find("div",attrs={"class": "uk-text uk-flex uk-flex-column"}).get_text().replace("  ", "").replace("\n", "")
	except:
		text = "No text"	
	
	try:
		author = soup.find("p",attrs={"class": "author"}).get_text().replace("  ", "").replace("\n", "")
	except:
		author = "No author"

	timestamp = datetime.now()	
	current_time = timestamp.strftime("%H:%M:%S")

	try:	
		with open ("Artikel.csv", "a", newline="", encoding="utf-8") as f:
			artikel_csv = csv.writer(f, delimiter=";" , quoting=csv.QUOTE_ALL)
			artikel_csv.writerow((title, subtitle, "".join(rubrik).capitalize(), category, date, text, "".join(author), url, timestamp))
	except:
		pass

	print(timestamp, url)


def createArticles():
	for url in links:
		createArticle(url_input=url)


schedule.every(29).minutes.do(getLinks)
schedule.every(29).minutes.do(createArticles)

while 1:
	try:
		schedule.run_pending()
		time.sleep(1)
	except:
		pass

"""
getLinks()
createArticles()
"""