from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parents[1]
apps = pd.read_csv(base / "data" / "googleplaystore.csv")
clean_path = base / "data" / "googleplaystore_clean.csv"

print("Original shape:", apps.shape)
print("Exact duplicate rows:", apps.duplicated().sum())
print("Duplicate app names:", apps["App"].duplicated().sum())
print("Invalid category rows:", (apps["Category"] == "1.9").sum())

# Keep a cleaned copy; remove exact duplicates and the malformed row
apps_clean = apps.drop_duplicates().copy()
apps_clean = apps_clean[apps_clean["Category"] != "1.9"].copy()

apps_clean = (
    apps_clean
    .sort_values("Reviews", ascending=False)
    .drop_duplicates(subset="App", keep="first")
    .copy()
)

# Convert text-formatted numbers
apps_clean["Reviews"] = pd.to_numeric(apps_clean["Reviews"])

apps_clean = (
    apps_clean
    .sort_values("Reviews", ascending=False)
    .drop_duplicates(subset="App", keep="first")
    .copy()
)

apps_clean["Installs"] = pd.to_numeric(
    apps_clean["Installs"]
    .str.replace(",", "", regex=False)
    .str.replace("+", "", regex=False)
)

apps_clean["Price"] = pd.to_numeric(
    apps_clean["Price"].str.replace("$", "", regex=False)
)

# Convert app sizes to megabytes
size_text = apps_clean["Size"].str.upper().str.strip()

size_number = pd.to_numeric(
    size_text
    .str.replace("M", "", regex=False)
    .str.replace("K", "", regex=False),
    errors="coerce"
)

apps_clean["Size_MB"] = size_number.where(
    ~size_text.str.endswith("K"),
    size_number / 1024
)

# Convert the update date
apps_clean["Last Updated"] = pd.to_datetime(
    apps_clean["Last Updated"],
    format="%B %d, %Y",
    errors="coerce"
)

# Check the cleaned data before renaming columns
print("\nCleaned shape:", apps_clean.shape)
print("Maximum rating:", apps_clean["Rating"].max())
print("Missing values:")
print(apps_clean.isna().sum().sort_values(ascending=False))
print("\nSize conversion examples:")
print(apps_clean[["Size", "Size_MB"]].head(10))
print("\nRows with size listed as 'Varies with device':",
      apps_clean["Size_MB"].isna().sum())

# Make column names convenient for SQL
apps_clean.columns = (
    apps_clean.columns
    .str.lower()
    .str.replace(" ", "_", regex=False)
)


apps_clean.to_csv(clean_path, index=False)

print("\nCleaned file saved to:", clean_path)
print("Updated date type:", apps_clean["last_updated"].dtype)