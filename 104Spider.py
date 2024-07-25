import requests
import bs4
import openpyxl

# Open Excel Sheet
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet["A1"] = "職缺名稱"
worksheet["B1"] = "公司名稱"
worksheet["C1"] = "工作縣市"
worksheet["D1"] = "區域"
worksheet["E1"] = "計薪方式"
worksheet["F1"] = "薪資下限"
worksheet["G1"] = "薪資上限"
worksheet["H1"] = "職缺連結"

page = 1
job_article_list = []

# Get 104 Web Contet
def GetWebContent(page) :
    response = requests.get("https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=.NET%20C%23&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page=" + str(page) + "&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1")
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # Get Job Information
    global job_article_list
    job_article_list = soup.find_all("article", class_ = "b-block--top-bord job-list-item b-clearfix js-job-item")
    GetJobInfo()

def GetJobInfo():
    while job_article_list != []:
        global page
        global workbook
        global worksheet
        print("第"+ str(page)+"頁")
        for job_article in job_article_list :
            # Job Title
            job_title = job_article["data-job-name"]

            # Company Name
            company_name = job_article["data-cust-name"]
            print(company_name)

            # Location
            location = job_article.find("ul", class_ = "b-list-inline b-clearfix job-list-intro b-content").find("li").text
            city = location[:3]
            discret = location[3:]

            # Link
            link = "https:" + job_article.find("a", class_ = "js-job-link")["href"]

            # Salary 
            org_salary_desc = ""
            salary_arrange = ""
            salary_type = ""
            min_salary = ""
            max_salary = ""
            salary_div = job_article.find("div", class_ = "job-list-tag b-content")
            # 辨識給薪方式
            if len(salary_div.find_all("span")) != 0 and salary_div.find_all("span")[0].text == "待遇面議":
                org_salary_desc = salary_div.find_all("span")[0].text
                salary_type = "面議"
                min_salary = 0
                max_salary = 0
            else :
                org_salary_desc = salary_div.find_all("a")[0].text
                salary_type = org_salary_desc[:2]
                # 擷取薪資上下限
                for char in org_salary_desc:
                    if char.isnumeric() or char == "~":
                        salary_arrange += char
                if salary_arrange.find("~") > 0:
                    min_salary = int(salary_arrange[:salary_arrange.find("~")])
                    max_salary = int(salary_arrange[salary_arrange.find("~") + 1:])

            worksheet.append([job_title, company_name, city, discret, salary_type, min_salary, max_salary, link])
            workbook.save("./Excel/104JobInfomation.xlsx")
        
        page += 1
        GetWebContent(page)

GetWebContent(page)