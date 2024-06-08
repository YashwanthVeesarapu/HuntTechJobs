import requests
import datetime
import os

# Define the API endpoint
api_url = "https://api.redsols.us/job/listings/all"  # Replace with your API URL

# Fetch data from the API
response = requests.get(api_url, headers={"Authorization" : "Bearer "+os.environ['SECRET_KEY']})
if response.status_code != 200:
    raise Exception(f"Failed to fetch data from API: {response.text}")

data = response.json()

# Function to convert timestamp to desired date format
def format_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%b %d")

# Get the current date in the desired format
current_date = datetime.datetime.now().strftime("%b %d, %Y")

# Format the data into a markdown table
job_listings = "| Job Title | Company | Location | Date Posted | Apply |\n"
job_listings += "|-----------|---------|----------|-------------|------------|\n"
for job in data[:50]:  # Limit to the first 50 jobs
    job_listings += (
        f"| **{job['title']}** | {job['company_name']} | {', '.join(job['locations'])} | "
        f"{format_date(job['date_posted'])} | "
        f"<a href=\"{job['url']}\" style=\"background-color: #870000; color: #ffffff; padding: 4px 8px; text-decoration: none; border-radius: 4px;\" target=\"_blank\">Apply</a> |\n"
    )

# Additional information about the repository
additional_info = """
## About This Repository

This repository contains job listings for tech professionals, including:

- Software Engineers
- Full Stack Engineers (Frontend & Backend)
- Frontend Developers
- Backend Developers
- Data Analysts
- Data Engineers
- Data Scientists

### About Hunt by Redsols

For all job seekers out there, let's be honest: the job search can be brutal these days. I recently went through it myself, feeling overwhelmed by irrelevant postings. So, I decided to create a solution: Hunt by Redsols ([hunt.redsols.us](https://hunt.redsols.us)).

Hunt by Redsols is a job board specifically designed for tech professionals like Software Engineers, Data Analysts, Full Stack Engineers (Frontend & Backend), and AI specialists. It curates clean and direct listings, saving you time and frustration in this competitive market.

This started as a personal project, but I realized others could benefit too! Let's build this community together and help it reach the people who need it most! Please share this post with your network of tech professionals, especially Software Engineers, Data Analysts, Full Stack Engineers (Frontend & Backend), and AI specialists. Comment down below with the hashtag #HuntForYourDreamJob to help spread the word! Feedback on the platform is always welcome.

Hunt by Redsols is getting even better! Now you can:
- Upvote relevant jobs to help the community surface the best opportunities.
- Track your applications with a simple click. The "Apply" button will turn green once you've submitted your application, preventing accidental re-applications. (Just remember, application data is stored locally on your browser, so be mindful when clearing cookies and browsing data.)

Like and comment on your post with #HuntForYourDreamJob to increase visibility.
Share the post with your network of tech professionals to help reach those in need.

You can email your feedback at [hunt@redsols.us](mailto:hunt@redsols.us).

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