import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prefect import flow
from etl.extract import extract_jobs
from etl.transform import transform_offers
from etl.load import load_offers

@flow
def linkedin_etl_flow():
    db_config = {
        'host': 'localhost',
        'user': 'jnr',
        'password': 'jnr123',
        'database': 'ofertas_db',
         'port': 3307
    }

    offers = extract_jobs()
    clean_offers = transform_offers(offers)

     # Mostrar cantidad de registros extraídos
    print(f"🔎 Se extrajeron {len(clean_offers)} ofertas.")

    # Mostrar un resumen (primeras 3 ofertas)
    for i, offer in enumerate(clean_offers[:3], start=1):
        print(f"\n📌 Oferta {i}:")
        for key, value in offer.items():
            print(f"   {key}: {value}")

    load_offers(clean_offers, db_config)

if __name__ == "__main__":
    linkedin_etl_flow()
