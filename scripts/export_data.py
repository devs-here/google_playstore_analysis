import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

base = Path(__file__).resolve().parents[1]
out = base / "app_data"
out.mkdir(exist_ok=True)

url = URL.create(
    "mysql+pymysql",
    username="root",
    password=os.environ["MYSQL_PASSWORD"],
    host="localhost",
    port=3306,
    database="google_play_analysis",
)
engine = create_engine(url)

queries = {
    "categories": """
        SELECT category,
               COUNT(*) AS total_apps,
               COUNT(rating) AS rated_apps,
               ROUND(100 * COUNT(rating) / COUNT(*), 1) AS pct_rated,
               ROUND(AVG(rating), 2) AS avg_rating
        FROM apps
        GROUP BY category
        ORDER BY total_apps DESC
    """,
    "free_paid": """
        SELECT type,
               COUNT(*) AS total_apps,
               ROUND(AVG(rating), 2) AS avg_rating,
               ROUND(AVG(reviews)) AS avg_reviews,
               ROUND(AVG(installs)) AS avg_installs
        FROM apps
        WHERE type IS NOT NULL
        GROUP BY type
    """,
    "install_ranges": """
        SELECT CASE
                   WHEN installs < 1000     THEN '1. Under 1K'
                   WHEN installs < 100000   THEN '2. 1K - 100K'
                   WHEN installs < 10000000 THEN '3. 100K - 10M'
                   ELSE                          '4. 10M+'
               END AS install_range,
               COUNT(*) AS total_apps,
               COUNT(rating) AS rated_apps,
               ROUND(AVG(rating), 2) AS avg_rating,
               ROUND(AVG(reviews)) AS avg_reviews
        FROM apps
        GROUP BY install_range
        ORDER BY install_range
    """,
    "size_ranges": """
        SELECT CASE
                   WHEN size_mb < 5  THEN '1. Under 5 MB'
                   WHEN size_mb < 20 THEN '2. 5 - 20 MB'
                   WHEN size_mb < 50 THEN '3. 20 - 50 MB'
                   ELSE                   '4. 50 MB+'
               END AS size_range,
               COUNT(*) AS total_apps,
               COUNT(rating) AS rated_apps,
               ROUND(AVG(rating), 2) AS avg_rating,
               ROUND(AVG(installs)) AS avg_installs
        FROM apps
        WHERE size_mb IS NOT NULL
        GROUP BY size_range
        ORDER BY size_range
    """,
    "update_year": """
        SELECT YEAR(last_updated) AS update_year,
               COUNT(*) AS total_apps,
               COUNT(rating) AS rated_apps,
               ROUND(AVG(rating), 2) AS avg_rating
        FROM apps
        WHERE last_updated IS NOT NULL
        GROUP BY update_year
        ORDER BY update_year
    """,
    "content_rating": """
        SELECT content_rating,
               COUNT(*) AS total_apps,
               COUNT(rating) AS rated_apps,
               ROUND(AVG(rating), 2) AS avg_rating,
               ROUND(AVG(installs)) AS avg_installs
        FROM apps
        GROUP BY content_rating
        ORDER BY total_apps DESC
    """,
    "top_reviews": """
        SELECT app, category, reviews, rating
        FROM apps
        ORDER BY reviews DESC
        LIMIT 10
    """,
    "top_installs": """
        SELECT app, category, installs, reviews, rating
        FROM apps
        ORDER BY installs DESC, reviews DESC
        LIMIT 10
    """,
    "rating_heatmap": """
        SELECT category,
               CASE
                   WHEN installs < 1000     THEN '1. Under 1K'
                   WHEN installs < 100000   THEN '2. 1K - 100K'
                   WHEN installs < 10000000 THEN '3. 100K - 10M'
                   ELSE                          '4. 10M+'
               END AS install_range,
               COUNT(rating) AS rated_apps,
               ROUND(AVG(rating), 2) AS avg_rating
        FROM apps
        GROUP BY category, install_range
        HAVING COUNT(rating) >= 10
    """,
}

with engine.connect() as connection:
    for name, sql in queries.items():
        df = pd.read_sql(text(sql), connection)
        df.to_csv(out / f"{name}.csv", index=False)
        print(f"{name}.csv saved, {df.shape[0]} rows")