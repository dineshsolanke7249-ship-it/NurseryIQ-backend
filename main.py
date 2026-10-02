from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection, initialize_database

app = FastAPI(title="NurseryIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

initialize_database()


@app.get("/")
def home():
    return {"message": "NurseryIQ Backend is working"}


@app.get("/api/plants")
def get_plants():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM plants")
    plants = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return {
        "plants": plants,
        "total": len(plants)
    }


@app.get("/api/plants/search")
def search_plants(q: str):
    connection = get_connection()
    cursor = connection.cursor()

    search_term = "%" + q + "%"

    cursor.execute(
        """
        SELECT * FROM plants
        WHERE name LIKE ?
        OR scientific_name LIKE ?
        OR category LIKE ?
        """,
        (search_term, search_term, search_term)
    )

    plants = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return {
        "query": q,
        "plants": plants,
        "total": len(plants)
    }


@app.get("/api/plants/{plant_id}")
def get_plant(plant_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM plants WHERE id = ?",
        (plant_id,)
    )

    plant = cursor.fetchone()

    connection.close()

    if plant is None:
        raise HTTPException(
            status_code=404,
            detail="Plant not found"
        )

    return dict(plant)


@app.get("/api/categories")
def get_categories():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT DISTINCT category FROM plants ORDER BY category"
    )

    categories = [row["category"] for row in cursor.fetchall()]

    connection.close()

    return {
        "categories": categories,
        "total": len(categories)
    }