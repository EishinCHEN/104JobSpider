import requests
import bs4
import openpyxl

# Get 104 Web Contet
page = 1
response = requests.get("https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=.NET%20C%23&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page=" + str(page) + "&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1")
soup = bs4.BeautifulSoup(response.text, "html.parser")