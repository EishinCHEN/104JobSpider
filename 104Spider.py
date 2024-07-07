import requests
import bs4
import openpyxl

# Get 104 Web Contet
page = 1
response = requests.get("https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=.NET%20C%23&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page=" + str(page) + "&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1")
soup = bs4.BeautifulSoup(response.text, "html.parser")

# Get Job Information
job_article_list = soup.find_all("article", class_ = "b-block--top-bord job-list-item b-clearfix js-job-item")

for job_article in job_article_list :
    # Job Title
    job_title = job_article["data-job-name"]
    print(job_title)

    # Company Name
    company_name = job_article["data-cust-name"]
    print(company_name)

    # Location
    location = job_article.find("ul", class_ = "b-list-inline b-clearfix job-list-intro b-content").find("li").text
    print(location)

    # Link
    link = job_article.find("a", class_ = "js-job-link")["href"]
    print("https:" + link)

    # Salary 
    salary = ""
    salary_div = job_article.find("div", class_ = "job-list-tag b-content")
    if len(salary_div.find_all("span")) != 0 and salary_div.find_all("span")[0].text == "待遇面議":
        print(salary_div.find_all("span")[0].text)
    else :
        print(salary_div.find_all("a")[0].text)

    print("--------------------")