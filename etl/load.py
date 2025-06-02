from prefect import task
import mysql.connector

@task
def load_offers(offers, db_config):
    print("💾 CARGANDO OFERTAS EN LA BASE DE DATOS...")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ofertas_laborales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255),
            ubicacion VARCHAR(255),
            enlace TEXT,
            fecha DATE
        )
    """)

    # Insertar ofertas
    for job in offers:
        cursor.execute("""
            INSERT INTO ofertas_laborales (titulo, ubicacion, enlace, fecha)
            VALUES (%s, %s, %s, %s)
        """, (job["titulo"], job["ubicacion"], job["enlace"], job["fecha"]))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(offers)} ofertas cargadas correctamente.")
