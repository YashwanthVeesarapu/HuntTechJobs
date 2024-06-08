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

# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Format the data into a markdown table
job_listings = "| Job Title | Company | Location | Date Posted | Apply Link |\n"
job_listings += "|-----------|---------|----------|-------------|------------|\n"
for job in data:
    job_listings += (
        f"| **{job['title']}** | {job['company_name']} | {', '.join(job['locations'])} | "
        f"{datetime.datetime.fromtimestamp(job['date_posted']).strftime('%Y-%m-%d')} | "
        f"[Apply]( {job['url']} ) |\n"
    )

# Update the README content
readme_content = f"""
# Tech Job Listings

*Updated on {current_date}*

## Latest Jobs

{job_listings}
"""

# Write the updated content to README.md
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)