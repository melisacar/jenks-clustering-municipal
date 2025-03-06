import pandas as pd
import numpy as np
import jenkspy

# Read the data
raw_df = pd.read_excel("jenks_ornek.xlsx", sheet_name='Sayfa1', na_values=["", "N/A"], header=0)

# Properly handle NaN values
raw_df.replace(["N/A", "NA", "nan"], np.nan, inplace=True)

# Select the columns related to districts (from column 5 to the third last column)
ilce_sutunlari = raw_df.columns[6:]

# Define the number of classes
num_classes = 5  

# Create an empty DataFrame to store results
jenks_results = pd.DataFrame(columns=["Column_0", "Column_1", "Column_2", "Indicator"] + list(ilce_sutunlari))

# Iterate over each row (each indicator)
for index, row in raw_df.iterrows():
    # Extract first 3 columns (0, 1, 2) and indicator name (column 3)
    col_0, col_1, col_2 = row[0], row[1], row[2]
    gosterge_adi = row[3]  # Indicator name from column 3
    gosterge_degerleri = row[6:]  # Indicator values for districts

    # Convert values to numeric and drop NaNs
    gosterge_degerleri = pd.to_numeric(gosterge_degerleri, errors='coerce').dropna()

    # Check if the number of unique values is at least 5
    if len(set(gosterge_degerleri)) < num_classes:
        print(f"Skipping '{gosterge_adi}' because it has less than {num_classes} unique values.")
        continue  # Skip this indicator

    # Apply Jenks natural breaks
    breaks = jenkspy.jenks_breaks(gosterge_degerleri.values, num_classes)
    jenks_labels = np.digitize(gosterge_degerleri.values, bins=breaks, right=False)  # 🔥 `right=False`

    # ✅ Start from 1 and max 5 group
    jenks_labels = np.clip(jenks_labels, 1, num_classes)  

    # Create a dictionary for this indicator
    row_data = {"Column_0": col_0, "Column_1": col_1, "Column_2": col_2, "Indicator": gosterge_adi}
    
    for ilce, label in zip(gosterge_degerleri.index, jenks_labels):
        row_data[ilce] = label  # Assign Jenks group to corresponding district

    # 🔥 **Fix: Fill missing districts with "No Data"**
    for ilce in ilce_sutunlari:
        if ilce not in row_data:
            row_data[ilce] = "No Data"

    # Append to the results DataFrame
    jenks_results = pd.concat([jenks_results, pd.DataFrame([row_data])], ignore_index=True)

# Save results to an Excel file
jenks_results.to_excel("jenks_ornek_output.xlsx", index=False)

# Summary print
print("Jenks classification completed and saved to 'jenks_ornek_output.xlsx'.")
