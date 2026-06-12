import datetime
import html
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.redsols.com/hunt/job/listings/all"
README_JOB_LIMIT = int(os.getenv("README_JOB_LIMIT", "25"))


def format_date(timestamp):
    return datetime.datetime.fromtimestamp(float(timestamp)).strftime("%b %d")


def escape_text(value):
    if value is None:
        return "N/A"
    return html.escape(str(value))


def format_locations(locations):
    if not locations:
        return "N/A"
    if isinstance(locations, str):
        locations = [locations]
    return escape_text(", ".join(str(location) for location in locations if location))


def job_timestamp(job):
    try:
        return float(job.get("date_posted", 0))
    except (TypeError, ValueError):
        return 0.0


secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY is required")


response = requests.get(
    API_URL,
    headers={"Authorization": f"Bearer {secret_key}"},
    timeout=30,
)
response.raise_for_status()

data = response.json()

if not isinstance(data, list):
    raise RuntimeError("Expected API to return a list of jobs")

data = sorted(data, key=job_timestamp, reverse=True)
visible_jobs = data[:README_JOB_LIMIT]

current_date = datetime.datetime.now().strftime("%b %d, %Y")
latest_posted = next((job.get("date_posted") for job in data if job.get("date_posted")), None)
latest_posted_text = format_date(latest_posted) if latest_posted else "N/A"

job_listings = ""
for idx, job in enumerate(visible_jobs):
    row_style = "background-color: #f9f9f9;" if idx % 2 == 0 else "background-color: #fff;"
    job_url = job.get("url")
    apply_button = (
        f'<a href="{html.escape(str(job_url), quote=True)}" '
        'style="color: #fff; background-color: #007bff; padding: 5px 10px; border-radius: 5px; text-decoration: none;">'
        'Apply</a>'
        if job_url
        else "N/A"
    )
    job_listings += (
        f'<tr style="{row_style}"><td><b>{escape_text(job.get("title"))}</b></td>'
        f'<td>{escape_text(job.get("company_name"))}</td>'
        f'<td>{format_locations(job.get("locations"))}</td>'
        f'<td>{format_date(job.get("date_posted")) if job.get("date_posted") else "N/A"}</td>'
        f'<td>{apply_button}</td></tr>\n'
    )

job_listings = (
    '<table>\n'
    '<thead>\n'
    '<tr><th>Job Title</th><th>🏢 Company</th><th>📍 Location</th><th>📅 Date Posted</th><th>Apply</th></tr>\n'
    '</thead>\n'
    '<tbody>\n' + job_listings + '</tbody>\n</table>'
)

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

summary = f"""
## Snapshot

- Total jobs available: **{len(data)}**
- Showing on GitHub: **{len(visible_jobs)}**
- Latest posting: **{latest_posted_text}**
- Full experience: [hunt.redsols.com](https://hunt.redsols.com)

"""

readme_content = f"""
# Tech Job Listings

*Updated on {current_date}*

{additional_info}

---

{summary}

## Latest Jobs

{job_listings}

"""

with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)
