import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Define the API endpoint
api_url = "https://api.redsols.com/job/listings/all"  # Replace with your API URL

# Fetch data from the API
response = requests.get(api_url, headers={"Authorization" : "Bearer "+ os.getenv("SECRET_KEY")})
if response.status_code != 200:
    raise Exception(f"Failed to fetch data from API: {response.text}")

data = response.json()

# Function to convert timestamp to desired date format
def format_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%b %d")

# Get the current date in the desired format
current_date = datetime.datetime.now().strftime("%b %d, %Y")

# Format the data into a visually enhanced markdown table
job_listings = ""
# job_listings = "| Job Title | 🏢 Company | 📍 Location | 📅 Date Posted | Apply |\n"
# job_listings += "|-----------|------------|-------------|-------------|:------:|\n"
for idx, job in enumerate(data):  # Limit to the first 50 jobs
    row_style = "background-color: #f9f9f9;" if idx % 2 == 0 else "background-color: #fff;"
    # Enhanced Apply button with emoji and bolder style
    apply_button = (
        f'<a href="{job["url"]}" '
        f'style="display: inline-block; background: linear-gradient(90deg, #870000 0%, #190A05 100%); '
        f'color: #fff; font-weight: bold; padding: 6px 18px; border-radius: 6px; text-decoration: none; '
        f'box-shadow: 0 2px 6px rgba(135,0,0,0.15); font-size: 1em;" target="_blank">'
        f'🚀 Apply'
        f'</a>'
    )
    job_listings += (
        f'<tr style="{row_style}"><td><b>{job["title"]}</b></td>'
        f'<td>{job["company_name"]}</td>'
        f'<td>{", ".join(job["locations"])}</td>'
        f'<td>{format_date(job["date_posted"])}</td>'
        f'<td>{apply_button}</td></tr>\n'
    )
# Wrap the table in <table> for HTML rendering in markdown
job_listings = (
    '<table>\n'
    '<thead>\n'
    '<tr><th>Job Title</th><th>🏢 Company</th><th>📍 Location</th><th>📅 Date Posted</th><th>Apply</th></tr>\n'
    '</thead>\n'
    '<tbody>\n' + job_listings + '</tbody>\n</table>'
)

# Additional information about the repository
additional_info = """
<p align=\"center\">
  <img src=\"https://img.shields.io/badge/Tech%20Jobs-Updated%20Daily-brightgreen\" alt=\"Tech Jobs\" />
  <img src=\"https://img.shields.io/badge/Community-Driven-blue\" alt=\"Community Driven\" />
  <img src=\"https://img.shields.io/badge/No%20Spam-Guaranteed-success\" alt=\"No Spam\" />
</p>

<h1 align=\"center\">🚀 Hunt by Redsols</h1>

---

## About This Repository

This repository contains job listings for tech professionals, including:

- Software Engineers
- Full Stack Engineers (Frontend & Backend)
- Frontend Developers
- Backend Developers
- Data Analysts
- Data Engineers
- Data Scientists

---

## <span style=\"color:#870000;font-weight:bold;\">About Hunt by Redsols</span>

> <span style=\"font-size:1.1em;\">For all job seekers out there, let's be honest: the job search can be brutal these days. I recently went through it myself, feeling overwhelmed by irrelevant postings. So, I decided to create a solution: <b>Hunt by Redsols</b> ([hunt.redsols.com](https://hunt.redsols.com)).</span>

Hunt by Redsols is a job board specifically designed for tech professionals like Software Engineers, Data Analysts, Full Stack Engineers (Frontend & Backend), and AI specialists. It curates clean and direct listings, saving you time and frustration in this competitive market.

<div align=\"center\">
  <img src=\"https://img.icons8.com/color/96/000000/job.png\" width=\"60\" alt=\"Job Board\"/>
</div>

This started as a personal project, but I realized others could benefit too! Let's build this community together and help it reach the people who need it most! Please share this post with your network of tech professionals, especially Software Engineers, Data Analysts, Full Stack Engineers (Frontend & Backend), and AI specialists. Comment down below with the hashtag <b>#HuntForYourDreamJob</b> to help spread the word! Feedback on the platform is always welcome.

---

## ✨ Features

- <b>Track your applications</b> with a simple click. The "Apply" button will turn green once you've submitted your application, preventing accidental re-applications. (Just remember, application data is stored locally on your browser, so be mindful when clearing cookies and browsing data.)
- <b>Clean, direct listings</b> with no spam or irrelevant jobs.
- <b>Community-driven improvements</b> and feedback welcome!

---

You can email your feedback at [hunt@redsols.com](mailto:hunt@redsols.com).

---

### Tags
#SoftwareEngineer #DataAnalyst #FullStackEngineer #FrontendDeveloper #BackendDeveloper #AI #JobSearch #Jobs #TechJobs
"""

# Update the README content
readme_content = f"""
# Tech Job Listings

*Updated on {current_date}*

{additional_info}

---

## Latest Jobs

{job_listings}
"""

# Write the updated content to README.md
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)