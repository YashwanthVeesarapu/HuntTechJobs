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

<h1 align=\"center\">Hunt by Redsols</h1>

<p align=\"center\">Curated tech jobs with a limited GitHub preview and the full experience on <a href=\"https://hunt.redsols.com\">hunt.redsols.com</a>.</p>

<p align=\"center\">
  <a href=\"https://hunt.redsols.com\"><b>Browse the full board</b></a>
</p>

### Why use this

- Fresh tech jobs, updated daily
- GitHub shows a preview only
- Full browsing and filters live on the site

You can email feedback at [hunt@redsols.com](mailto:hunt@redsols.com).
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
