from prefect import task
import requests
from bs4 import BeautifulSoup

@task
def extract_offers(url="https://www.linkedin.com/jobs/search/?keywords=data%20scientist"):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

#########################################################################################
    print("\n🧩 Fragmento del HTML recibido:")
    print(soup.prettify()[:1000])  # Solo muestra los primeros 1000 caracteres

############################################################################################

    offers = []
    job_cards = soup.find_all("li", class_="jobs-search-results__list-item")

    for card in job_cards:
        try:
            title = card.find("h3").text.strip()
            company = card.find("h4").text.strip()
            location = card.find("span", class_="job-search-card__location").text.strip()
            date_posted = card.find("time")["datetime"]
            link = card.find("a", href=True)["href"]
            offers.append({
                "titulo": title,
                "descripcion": company,
                "ubicacion": location,
                "fecha": date_posted,
                "enlace": link
            })
        except Exception:
            continue

    return offers
