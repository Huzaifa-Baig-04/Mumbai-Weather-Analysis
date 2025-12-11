import pandas as pd

# Step 1: Load your CSV
file_path = "f:/HUZAIFA/field project py/Merged_Flood_Weather.csv"
df = pd.read_csv(file_path)

# Step 2: Clean 'rainfall_mm' column
df['rainfall_mm'] = df['rainfall_mm'].astype(str).str.replace(',', '', regex=False)
df['rainfall_mm'] = pd.to_numeric(df['rainfall_mm'], errors='coerce').fillna(0)

# Step 3: Clean temperature columns and fill missing values with column mean
for col in ['avg_temp_c', 'max_temp_c', 'min_temp_c']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].mean())

# Step 4: Calculate average rainfall (ignoring 0)
average_rainfall = df.loc[df['rainfall_mm'] > 0, 'rainfall_mm'].mean()
print("Average Rainfall (mm):", average_rainfall)

# Step 5: Calculate average temperatures
avg_temp = df['avg_temp_c'].mean()
max_temp = df['max_temp_c'].mean()
min_temp = df['min_temp_c'].mean()
print("Average Temperature (°C):", avg_temp)
print("Average Max Temperature (°C):", max_temp)
print("Average Min Temperature (°C):", min_temp)

# Step 6: Flood counts per year
flood_counts = df.groupby('year')['Flood Type'].count()
print("\nFlood Counts per Year:")
print(flood_counts)

# Step 7: Total rainfall per year
rainfall_per_year = df.groupby('year')['rainfall_mm'].sum()
print("\nTotal Rainfall per Year (mm):")
print(rainfall_per_year)

# Step 8: Save cleaned CSV
output_file = "f:/HUZAIFA/field project py/cleaned_Merged_Flood_Weather.csv"
df.to_csv(output_file, index=False)
print(f"\nCleaned CSV saved as: {output_file}")








