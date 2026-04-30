import os
import sqlite3
from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "immunisation.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@bp.route("/")
def index():
    conn = get_db_connection()

    year_data = conn.execute("""
        SELECT 
            MIN(year) AS min_year,
            MAX(year) AS max_year,
            COUNT(DISTINCT year) AS total_years
        FROM InfectionData
    """).fetchone()

    total_countries = conn.execute("""
        SELECT COUNT(DISTINCT country) AS total
        FROM InfectionData
    """).fetchone()["total"]

    total_infection_types = conn.execute("""
        SELECT COUNT(DISTINCT inf_type) AS total
        FROM InfectionData
    """).fetchone()["total"]

    conn.close()

    min_year = year_data["min_year"]
    max_year = year_data["max_year"]
    total_years = year_data["total_years"]

    snapshot_cards = [
        {
            "title": f"{total_years}+ Years",
            "description": f"Historical immunization records from {min_year} to {max_year}.",
            "image": "img/snap1.png",
            "alt": "Calendar snapshot data"
        },
        {
            "title": f"{total_countries}+ Countries",
            "description": "Worldwide vaccination and infection coverage data.",
            "image": "img/snap2.png",
            "alt": "Global snapshot data"
        },
        {
            "title": f"{total_infection_types} Infection Types",
            "description": "Disease and vaccine-related indicators tracked in the database.",
            "image": "img/snap3.png",
            "alt": "Disease snapshot data"
        },
        {
            "title": "Global Insights",
            "description": "Identify immunization gaps, trends, and progress across regions.",
            "image": "img/snap4.png",
            "alt": "Vaccine snapshot data"
        }
    ]

    return render_template("index.html", snapshot_cards=snapshot_cards)


@bp.route("/page1")
def page1():
    return render_template("page1.html")


@bp.route("/page2")
def page2():
    return render_template("page2.html")


@bp.route("/page3")
def page3():
    return render_template("page3.html")

@bp.route("/page4")
def page4():
    return render_template("page4.html")

@bp.route("/page5")
def page5():
    return render_template("page5.html")

@bp.route("/check-db")
def check_db():
    conn = get_db_connection()

    tables = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """).fetchall()

    output = f"<h2>Database path:</h2><p>{DATABASE_PATH}</p>"
    output += "<h2>Tables in immunisation.db</h2>"

    for table in tables:
        table_name = table["name"]
        output += f"<h3>{table_name}</h3>"

        columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()

        for column in columns:
            output += f"{column['name']} - {column['type']}<br>"

    conn.close()

    return output