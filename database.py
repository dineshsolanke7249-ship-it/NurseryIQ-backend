import sqlite3

DATABASE_NAME = "nurseryiq.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            scientific_name TEXT,
            category TEXT NOT NULL,
            sunlight TEXT,
            watering TEXT,
            soil TEXT,
            temperature TEXT,
            description TEXT,
            care_instructions TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_sample_plants():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM plants")
    count = cursor.fetchone()[0]

    if count == 0:
        plants = [
            (
                "Aloe Vera",
                "Aloe barbadensis miller",
                "Medicinal",
                "Bright indirect sunlight",
                "Water every 2-3 weeks",
                "Well-draining sandy soil",
                "18-30°C",
                "A popular succulent known for its medicinal and soothing properties.",
                "Allow the soil to dry completely between watering."
            ),
            (
                "Snake Plant",
                "Dracaena trifasciata",
                "Indoor",
                "Low to bright indirect light",
                "Water every 2-3 weeks",
                "Well-draining potting soil",
                "15-30°C",
                "A hardy indoor plant that requires relatively little maintenance.",
                "Avoid overwatering and provide good drainage."
            ),
            (
                "Rose",
                "Rosa",
                "Flowering",
                "6-8 hours of sunlight",
                "Water 2-3 times per week",
                "Fertile well-draining soil",
                "15-28°C",
                "A popular flowering plant available in many colors and varieties.",
                "Provide sunlight, regular watering and periodic pruning."
            ),
            (
                "Tulsi",
                "Ocimum tenuiflorum",
                "Medicinal",
                "4-6 hours of sunlight",
                "Water when the topsoil becomes dry",
                "Rich well-draining soil",
                "20-35°C",
                "An aromatic medicinal herb commonly grown in homes.",
                "Give plenty of sunlight and avoid waterlogging."
            ),
            (
                "Money Plant",
                "Epipremnum aureum",
                "Indoor",
                "Bright indirect light",
                "Water once a week",
                "Well-draining potting mix",
                "18-30°C",
                "A popular indoor plant that can grow as a trailing or climbing vine.",
                "Keep the soil lightly moist but avoid excessive watering."
            )
        ]

        cursor.executemany("""
            INSERT INTO plants (
                name,
                scientific_name,
                category,
                sunlight,
                watering,
                soil,
                temperature,
                description,
                care_instructions
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, plants)

        connection.commit()

    connection.close()


def initialize_database():
    create_database()
    add_sample_plants()