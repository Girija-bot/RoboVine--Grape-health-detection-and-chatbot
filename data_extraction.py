import pandas as pd

file_path = r"C:\Users\girij\Distributed systems\Phenological parameters.xlsx"

sheet_names = [
    'Normalized daily transpiration',
    'Normalized Gs canopy 6-7h',
    'Normalized Gs canopy 12-13h',
    'weight'
]

sheets = {name: pd.read_excel(file_path, sheet_name=name) for name in sheet_names}

# Flexible blank row detection: row is blank if >= 70% of cells are empty
def is_row_blank(row, threshold=0.7):
    blank_cells = sum(pd.isna(x) or (isinstance(x, str) and x.strip() == '') for x in row)
    return blank_cells / len(row) >= threshold

def split_clusters(sheet, sheet_name):
    blank_rows = [idx for idx, row in sheet.iterrows() if is_row_blank(row)]
    print(f"Blank rows found at indices: {blank_rows} in sheet '{sheet_name}'")

    if len(blank_rows) < 2:
        preview_file = f"{sheet_name.replace(' ', '_')}_preview.csv"
        sheet.to_csv(preview_file, index=False)
        print(f"⚠️  Not enough blank rows found in '{sheet_name}'. Preview saved as {preview_file}")
        raise ValueError(f"Cluster split points not found correctly in sheet '{sheet_name}'.")

    cluster1 = sheet.iloc[:blank_rows[0]].dropna(how='all')
    cluster2 = sheet.iloc[blank_rows[0] + 1:blank_rows[1]].dropna(how='all')
    cluster3 = sheet.iloc[blank_rows[1] + 1:].dropna(how='all')

    return cluster1, cluster2, cluster3

clusters = {}
for sheet_name in sheet_names:  # include weight now
    sheet = sheets[sheet_name]
    print(f"\nProcessing sheet: {sheet_name}")
    try:
        c1, c2, c3 = split_clusters(sheet, sheet_name)
        clusters[sheet_name] = {
            'Normalized': c1,
            'Daily_Plant_Weight': c2,
            'Raw_Transpiration': c3
        }
    except ValueError as e:
        print(e)
        # Optional: for weight sheet or others, if splitting fails, save whole sheet as CSV
        safe_sheet_name = sheet_name.replace(' ', '_').replace(':', '').replace('/', '-')
        sheet.to_csv(f"{safe_sheet_name}.csv", index=False)
        print(f"Saved entire '{sheet_name}' sheet as CSV without splitting.")

# Save clusters as CSVs
for sheet_name, data in clusters.items():
    for cluster_name, df in data.items():
        safe_sheet_name = sheet_name.replace(' ', '_').replace(':', '').replace('/', '-')
        df.to_csv(f"{safe_sheet_name}_{cluster_name}.csv", index=False)

print("✅ Data extraction and splitting completed. CSV files saved successfully.")
