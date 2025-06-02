from prefect import task

@task
def transform_offers(offers):
    print("🔧 TRANSFORMANDO OFERTAS...")
    clean_offers = []

    for job in offers:
        if all([job["title"], job["location"], job["link"]]):
            clean_offers.append({
                "titulo": job["title"],
                "ubicacion": job["location"],
                "enlace": job["link"],
                "fecha": job["date"]  # Puede ser None
            })

    return clean_offers
