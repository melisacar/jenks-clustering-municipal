import pandas as pd
import numpy as np
import jenkspy
import matplotlib.pyplot as plt

# Read the data
raw_df = pd.read_excel("ilce_performans.xlsx", sheet_name='2023', na_values=["", "N/A"], header=0)

# Properly handle NaN values
raw_df.replace(["N/A", "NA", "nan"], np.nan, inplace=True)

# Get the indicator name (Column 3, Row 13)
gosterge_adi = raw_df.iloc[13, 3]
print(f"Selected Indicator: {gosterge_adi}")

# Select the columns related to districts (from column 5 to the third last column)
ilce_sutunlari = raw_df.columns[5:-3]

# Retrieve the values of the selected indicator (Row 13, district-related columns)
gosterge_degerleri = raw_df.iloc[13, 5:-3]

# Convert values to numeric
gosterge_degerleri = pd.to_numeric(gosterge_degerleri, errors='coerce')

# Remove NaN values
gosterge_degerleri = gosterge_degerleri.dropna()

# Apply Jenks algorithm to group districts based on the selected indicator
num_classes = 5  # Define 5 classes

if len(gosterge_degerleri) > num_classes:
    breaks = jenkspy.jenks_breaks(gosterge_degerleri.values, num_classes)

    # Assign groups
    jenks_labels = np.digitize(gosterge_degerleri.values, bins=breaks, right=True)

    # Store results in a DataFrame
    grouped_df = pd.DataFrame({
        "District": gosterge_degerleri.index,
        gosterge_adi: gosterge_degerleri.values,
        "Jenks Group": jenks_labels
    })

    print(grouped_df)

    # Save results to an Excel file
    grouped_df.to_excel("district_jenks_clustering.xlsx", index=False)

    # Visualization
    plt.figure(figsize=(10, 6))
    grouped_df["Jenks Group"].value_counts().sort_index().plot(kind="bar", color="skyblue")
    plt.title(f"{gosterge_adi} - Distribution of Districts by Jenks Groups")
    plt.xlabel("Jenks Group")
    plt.ylabel("Number of Districts")
    plt.xticks(rotation=0)
    plt.show()
else:
    print("Not enough unique values for Jenks classification.")