import pandas as pd

# Load the predicted results
predicted_df = pd.read_csv('C:/Users/girij/Distributed systems/Dataset/Grape/predicted_results.csv')

# Mapping of filename to unit and thesis
mapping_data = {
    'filename': ['DSC18_07553.JPG', 'DSC18_07567.JPG', 'DSC18_07899.JPG', 'IMG2005_2292.JPG', 'IMG18_6742.JPG',
                 'IMG2006_4214.JPG', 'IMG2005_2316.JPG', 'IMG2006_4246.JPG', 'IMG2006_4287.JPG', 'IMG2005_2365.JPG',
                 'IMG2006_4297.JPG', 'IMG2006_4294.JPG', 'IMG2007_0056.JPG', 'IMG2007_0043.JPG', 'IMG2006_4264.JPG',
                 'IMG2006_4291.JPG', 'IMG2007_0059.JPG', 'IMG_8820.JPG', 'IMG2007_0059.JPG', 'IMG2007_0086.JPG',
                 'IMG2007_0067.JPG', 'IMG2006_4263.JPG', 'IMG2007_0081.JPG', 'IMG2007_0089.JPG', 'IMG2007_0063.JPG',
                 'IMG2007_0102.JPG', 'IMG2007_0075.JPG', 'IMG2007_0062.JPG', 'DSC18_07597.JPG', 'IMG_19075001.JPG',
                 'IMG2007_0089.JPG', 'IMG_19075051.JPG'],
    'unit': ['B18', 'B41', 'B46', 'C17', 'C19', 'C22', 'C44', 'B19', 'B21', 'B24', 'B44', 'B48', 'C20', 'C24', 'C45',
             'C47', 'B20', 'B22', 'B42', 'B47', 'C21', 'C41', 'C43', 'C48', 'B17', 'B23', 'B43', 'B45', 'C18', 'C23',
             'C42', 'C46'],
    'thesis': [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4]
}

# ✅ Convert mapping dictionary to DataFrame
mapping_df = pd.DataFrame(mapping_data)

# ✅ Merge predicted results with the mapping DataFrame
predicted_df = pd.merge(predicted_df, mapping_df, on='filename', how='left')

# ✅ Load the dataset
dataset_df = pd.read_excel('C:/Users/girij/Distributed systems/Dataset/Grape/Dataset.xlsx')

# ✅ Ensure 'treatment' exists and matches types
predicted_df['treatment'] = predicted_df['thesis'].astype(float)
dataset_df['THESIS'] = dataset_df['THESIS'].astype(float)

# ✅ Merge predictions with the main dataset
merged_df = pd.merge(
    predicted_df,
    dataset_df,
    left_on=['unit', 'treatment'],
    right_on=['Unit', 'THESIS'],
    how='left'
)

# ✅ Drop unnecessary columns
merged_df.drop(columns=['treatment', 'Unit', 'THESIS'], inplace=True)

# ✅ Save final merged results
merged_df.to_csv('C:/Users/girij/Distributed systems/Dataset/Grape/merged_results.csv', index=False)
merged_df.to_excel('C:/Users/girij/Distributed systems/Dataset/Grape/merged_results.xlsx', index=False)

print("\n✅ Final merged data (cleaned) saved to CSV and Excel.")
