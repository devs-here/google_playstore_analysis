# 📱 Google Play Store Analysis Dashboard

An interactive data analysis dashboard built with Python, MySQL and Streamlit, analysing 9,659 unique Google Play Store apps.

🚀 [Live Demo](https://playstore-analysis-gaurav.streamlit.app/)

## ✨ Features

* 🧹 **Data Cleaning** — pandas pipeline that fixes malformed rows, duplicate apps and text-formatted numbers
* 🗄️ **SQL Analysis** — 9 queries in MySQL (GROUP BY, HAVING, CASE, multi-column grouping)
* 🎯 **Interactive Filter** — slider to set the minimum number of rated apps per category
* 📊 **KPI Cards** — total apps, categories shown and share of apps with a rating
* 🗂️ **5 Organised Tabs** — Categories, Free vs Paid, Installs & Size, Trends, Top apps

## 📈 What's Inside

### 🏷️ Categories
* Average rating by category
* Rating vs number of apps (competition scatter plot)

### 💸 Free vs Paid
* Average rating, reviews and installs by app type
* Rating heatmap by category and install range

### 📦 Installs & Size
* Rating and reviews by install range
* Rating and installs by app size

### 📅 Trends
* Average rating by last update year
* Rating and installs by content rating

### 🏆 Top Apps
* Top 10 apps by reviews
* Top 10 apps by installs

## 🔎 Key Findings

* Ratings are tightly clustered across categories, from about 3.97 (Dating) to 4.36 (Education, Art & Design)
* Paid apps are rated slightly higher than free apps (4.26 vs 4.17), but free apps get far more installs and reviews
* Apps in the 1K–100K install range have the lowest average ratings
* Apps updated in 2018 are rated higher (4.23) than older ones (about 4.03–4.09)

## 🧹 Data Cleaning

* Removed one malformed row and exact duplicate rows
* Kept one row per app, the version with the most reviews
* Converted `Installs`, `Price` and `Reviews` to numbers, `Size` to MB, and `Last Updated` to a date
* Left missing values as NULL instead of filling them (for example, size listed as "Varies with device")

## 🛠️ Built With

* Python
* Pandas
* MySQL, SQLAlchemy and PyMySQL
* Plotly
* Streamlit

## 📂 Project Structure

```
├── app.py               # Streamlit dashboard
├── app_data/            # Query results the dashboard reads (CSV)
├── scripts/
│   ├── load_and_clean.py   # Clean the raw CSV with pandas
│   ├── load_mysql.py       # Load the cleaned data into MySQL
│   └── export_data.py      # Run the SQL queries and save results to app_data/
├── sql/
│   └── queries.sql      # All analysis queries
└── requirements.txt
```

## 📂 Dataset

[Google Play Store Apps](https://www.kaggle.com/datasets/lava18/google-play-store-apps) from Kaggle. The raw file is not included in the repo.

## 🚀 Run Locally

**Just the dashboard** (the query results are already in `app_data/`):

```
git clone https://github.com/devs-here/google_playstore_analysis.git
cd google_playstore_analysis
pip install -r requirements.txt
streamlit run app.py
```

**Full pipeline** (needs MySQL running locally):

1. Download `googleplaystore.csv` from Kaggle into a `data/` folder
2. Create a database called `google_play_analysis` in MySQL
3. Set your MySQL password as an environment variable:

```
$env:MYSQL_PASSWORD = "your_password"
```

4. Run the scripts in order:

```
python scripts/load_and_clean.py
python scripts/load_mysql.py
python scripts/export_data.py
```
