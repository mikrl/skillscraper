import json

with open("./skillscraper/common_job_titles.json") as f:
    data = json.load(f)

industries  = data.get('top_industries')
for industry in industries:
    if industry.get('industry_name') == 'Technology':
        print(industry.get('common_job_titles'))