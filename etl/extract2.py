from prefect import task
import requests
from bs4 import BeautifulSoup

@task
def extract_jobs():
    print("🔍 EXTRACCIÓN DE OFERTAS DE REMOTIVE.IO")

    url = "https://remotive.io/remote-jobs/software-dev"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_cards = soup.find_all("a", class_="job-tile")
    print(f"Se encontraron {len(job_cards)} ofertas laborales.")

    jobs = []
    for card in job_cards:
        title_tag = card.find("h2", class_="job-tile-title")
        location_tag = card.find("div", class_="location")
        link_tag = card["href"]
        date_tag = card.find("time")

        job = {
            "title": title_tag.text.strip() if title_tag else None,
            "location": location_tag.text.strip() if location_tag else None,
            "link": "https://remotive.io" + link_tag if link_tag else None,
            "date": date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else None
        }

        jobs.append(job)

    return jobs
