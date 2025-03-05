# District Clustering using Jenks Natural Breaks

This project groups districts based on a selected performance indicator using the **Jenks Natural Breaks** classification method.

## 🚀 Features

- Reads district performance data from an Excel file.
- Extracts a **specific indicator** (e.g., Disaster Management, Waste Management, etc.).
- Applies **Jenks Natural Breaks** to categorize districts into 5 groups.
- Saves the results in an Excel file.
- Generates a bar chart showing the distribution of districts across the groups.

## 📂 File Structure

- `main.py` → The main script that performs the Jenks classification.
- `NA.xlsx` → Input Excel file (not included in the repository).
- `district_jenks_clustering.xlsx` → Output file containing classified districts.
- `README.md` → This documentation.

## 🛠️ Installation & Usage

### Install dependencies

```bash
pip install pandas numpy jenkspy matplotlib openpyxl
```