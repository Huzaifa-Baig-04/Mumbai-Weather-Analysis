# ---------------------------------------------------------
# 🌦️ Mumbai Weather Data Merger by Huzaifa Baig
# Project: Analyzing Weather Patterns for Climate Change Research
# ---------------------------------------------------------

import pandas as pd

# === Step 1: Load CSV Files ===
df1 = pd.read_csv("seasonalFrequency_c_Winter-1891-2019.csv")
df2 = pd.read_csv("mumbai-monthly-rains.csv")
df3 = pd.read_csv("Mumbai_1990_2022_Santacruz.csv")

# === Step 2: Standardize Column Names ===
for df in [df1, df2, df3]:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# === Step 3: Fix and Extract Year Columns ===
# File 1
df1.rename(columns={"year": "year"}, inplace=True)

# File 2
df2.rename(columns={"year": "year"}, inplace=True)

# File 3 (extract year from 'time')
df3["year"] = pd.to_datetime(df3["time"], errors="coerce").dt.year

# === Step 4: Select Only Key Columns ===
# File 1 – Cyclone Frequency
df1 = df1[["year", "january:_total", "february:_total"]].rename(
    columns={"january:_total": "jan_cyclone_total", "february:_total": "feb_cyclone_total"}
)

# File 2 – Rainfall
df2 = df2[["year", "total"]].rename(columns={"total": "rainfall_mm"})

# File 3 – Temperature
df3 = df3[["year", "tavg", "tmax", "tmin", "prcp"]].rename(
    columns={
        "tavg": "avg_temp_c",
        "tmax": "max_temp_c",
        "tmin": "min_temp_c",
        "prcp": "rainfall_prcp_mm"
    }
)

# === Step 5: Merge All by Year ===
merged = df1.merge(df2, on="year", how="outer").merge(df3, on="year", how="outer")

# === Step 6: Sort and Clean ===
merged = merged.sort_values(by="year").drop_duplicates(subset="year")
merged.columns = [c.lower() for c in merged.columns]

# === Step 7: Save Final CSV ===
merged.to_csv("Mumbai_Weather_Combined.csv", index=False)

print("✅ Merging Complete! File saved as 'Mumbai_Weather_Combined.csv'")
print("Columns in final dataset:", list(merged.columns))
print("\nSample preview:\n", merged.head())
