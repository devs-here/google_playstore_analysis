import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd
from pathlib import Path

url = URL.create(
    "mysql+pymysql",
    username="root",
    password=os.environ["MYSQL_PASSWORD"],
    host="localhost",
    port=3306,
    database="google_play_analysis",
)

engine = create_engine(url)

base = Path(__file__).resolve().parents[1]
df = pd.read_csv(base / "data" / "googleplaystore_clean.csv", parse_dates=["last_updated"])

df.to_sql("apps", engine, if_exists="replace", index=False, chunksize=1000)

