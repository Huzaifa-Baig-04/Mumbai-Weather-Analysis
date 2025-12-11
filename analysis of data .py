# ---------------------------------------------------------
# 🌦️ Mumbai Weather & Flood Analysis – by Huzaifa Baig
# Under guidance of: Mr. Dhanraj Jadhav
# Project: Analyzing Weather Patterns for Climate Change Research
# ---------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# === Step 1: Load Dataset ===
df = pd.read_csv("cleaned_Merged_Flood_Weather.csv")

print("✅ Dataset Loaded Successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist(), "\n")

# === Step 2: Clean column names ===
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# === Step 3: Fix 'year' column safely ===
year_cols = [c for c in df.columns if "year" in c]

if len(year_cols) == 0:
    raise ValueError("No 'year' column found.")
else:
    # Convert each to string, then numeric
    year_data = None
    for col in year_cols:
        series = df[col]
        # If it's a DataFrame (multi-column), flatten it
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]
        # Convert to numeric safely
        numeric_series = pd.to_numeric(series, errors="coerce")
        if year_data is None or numeric_series.notna().sum() > year_data.notna().sum():
            year_data = numeric_series

    df["year"] = year_data.astype(float)

# Drop any duplicate year columns except the main one
df = df.loc[:, ~df.columns.duplicated()]

# === Step 4: Convert numeric columns ===
for col in df.columns:
    df[col] = df[col].astype(str).str.replace(",", "").str.strip()
    try:
        df[col] = df[col].astype(float)
    except:
        pass

# === Step 5: Overview ===
print("📊 Dataset Overview:\n")
print(df.describe().T)
print("\nMissing Values:\n", df.isnull().sum(), "\n")

# === Step 6: Correlation Matrix ===
corr = df.corr(numeric_only=True)
print("📈 CORRELATION MATRIX:\n", corr, "\n")

plt.figure(figsize=(8,6))
plt.imshow(corr, cmap="coolwarm", interpolation="nearest")
plt.title("Correlation Heatmap")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.colorbar(label="Correlation Strength")
plt.tight_layout()
plt.show()

# === Step 7: Rainfall & Temperature Trend ===
if "rainfall_mm" in df.columns:
    plt.figure(figsize=(10,5))
    plt.plot(df["year"], df["rainfall_mm"], color="blue", label="Rainfall (mm)")
    if "avg_temp_c" in df.columns:
        plt.plot(df["year"], df["avg_temp_c"], color="red", label="Avg Temp (°C)")
    plt.title("Rainfall & Temperature Trend – Mumbai")
    plt.xlabel("Year"); plt.ylabel("Values")
    plt.legend(); plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Step 8: Flood Frequency Trend (if present) ===
if "flood_frequency" in df.columns:
    plt.figure(figsize=(10,5))
    plt.bar(df["year"], df["flood_frequency"], color="purple")
    plt.title("Flood Frequency in Mumbai Over Years")
    plt.xlabel("Year"); plt.ylabel("No. of Floods")
    plt.grid(axis="y"); plt.tight_layout()
    plt.show()

# === Step 9: Decadal Averages ===
df["decade"] = (df["year"] // 10) * 10
decadal_avg = df.groupby("decade").mean(numeric_only=True).reset_index()

plt.figure(figsize=(10,5))
if "rainfall_mm" in decadal_avg.columns:
    plt.plot(decadal_avg["decade"], decadal_avg["rainfall_mm"], marker="o", label="Rainfall (mm)")
if "avg_temp_c" in decadal_avg.columns:
    plt.plot(decadal_avg["decade"], decadal_avg["avg_temp_c"], marker="s", label="Avg Temp (°C)")
if "flood_frequency" in decadal_avg.columns:
    plt.plot(decadal_avg["decade"], decadal_avg["flood_frequency"], marker="^", label="Flood Events")
plt.title("Decadal Averages – Rainfall, Temperature & Floods")
plt.xlabel("Decade"); plt.ylabel("Average Values")
plt.legend(); plt.grid(True); plt.tight_layout()
plt.show()

print("\n📆 Decadal Summary:\n", decadal_avg, "\n")

# === Step 10: Extremes ===
if "rainfall_mm" in df.columns:
    max_rain = df.loc[df["rainfall_mm"].idxmax()]
    min_rain = df.loc[df["rainfall_mm"].idxmin()]
    print(f"🌧 Highest Rainfall Year: {int(max_rain['year'])} – {max_rain['rainfall_mm']} mm")
    print(f"🌧 Lowest Rainfall Year: {int(min_rain['year'])} – {min_rain['rainfall_mm']} mm")

if "avg_temp_c" in df.columns:
    max_temp = df.loc[df["avg_temp_c"].idxmax()]
    min_temp = df.loc[df["avg_temp_c"].idxmin()]
    print(f"🌡 Highest Avg Temp Year: {int(max_temp['year'])} – {max_temp['avg_temp_c']} °C")
    print(f"🌡 Lowest Avg Temp Year: {int(min_temp['year'])} – {min_temp['avg_temp_c']} °C")

# === Step 11: Correlation Rainfall vs Floods ===
if "rainfall_mm" in df.columns and "flood_frequency" in df.columns:
    print("\n🌊 Climate Impact on Floods:\n")
    slope, intercept, r_value, p_value, std_err = linregress(df["rainfall_mm"], df["flood_frequency"])
    print(f"Correlation (Rainfall vs Flood Frequency): {r_value:.3f}")
    print(f"R-squared: {r_value**2:.3f}")

    plt.figure(figsize=(8,6))
    plt.scatter(df["rainfall_mm"], df["flood_frequency"], color="dodgerblue")
    plt.plot(df["rainfall_mm"], intercept + slope*df["rainfall_mm"], color="red", linewidth=2)
    plt.title("Rainfall vs Flood Frequency (Climate Impact)")
    plt.xlabel("Rainfall (mm)"); plt.ylabel("Flood Frequency")
    plt.grid(True); plt.tight_layout(); plt.show()

# === Step 12: Trend Summary ===
if "rainfall_mm" in df.columns and "avg_temp_c" in df.columns:
    rain_trend = "increasing" if df["rainfall_mm"].iloc[-1] > df["rainfall_mm"].iloc[0] else "decreasing"
    temp_trend = "increasing" if df["avg_temp_c"].iloc[-1] > df["avg_temp_c"].iloc[0] else "decreasing"
    print(f"\n📈 Overall Trends Summary:")
    print(f"→ Rainfall trend: {rain_trend}")
    print(f"→ Temperature trend: {temp_trend}")

print("\n✅ Comprehensive Analysis Completed Successfully!")

