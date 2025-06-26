import pandas as pd

# Load predicted results
predicted_df = pd.read_csv('C:/Users/girij/Distributed systems/Dataset/Grape/predicted_results.csv')

# Mapping of correct image filenames
mapping_data = {
    'filename': ['DSC18_07553.JPG', 'DSC18_07567.JPG', 'DSC18_07899.JPG', 'IMG2005_2292.JPG', 'IMG18_6742.JPG',
                 'IMG2006_4214.JPG', 'IMG2005_2316.JPG', 'IMG2006_4246.JPG', 'IMG2006_4287.JPG', 'IMG2005_2365.JPG',
                 'IMG2006_4297.JPG', 'IMG2006_4294.JPG', 'IMG2007_0056.JPG', 'IMG2007_0043.JPG', 'IMG2006_4264.JPG',
                 'IMG2006_4291.JPG', 'IMG2007_0059.JPG', 'IMG_8820.JPG', 'IMG2007_0059.JPG', 'IMG2007_0086.JPG',
                 'IMG2007_0067.JPG', 'IMG2006_4263.JPG', 'IMG2007_0081.JPG', 'IMG2007_0089.JPG', 'IMG2007_0063.JPG',
                 'IMG2007_0102.JPG', 'IMG2007_0075.JPG', 'IMG2007_0062.JPG', 'DSC18_07597.JPG', 'IMG_19075001.JPG',
                 'IMG2007_0089.JPG', 'IMG_19075051.JPG']
}

# Load the dataset from Excel
dataset_df = pd.read_excel('C:/Users/girij/Distributed systems/Dataset/Grape/Dataset.xlsx',
                           sheet_name='Daily Transpiration_anova_graph')

# ✅ Replace incorrect 'DATA' values with correct filenames
dataset_df = dataset_df.copy()
dataset_df['filename'] = pd.Series(mapping_data['filename'])

# Merge datasets based on correct 'filename'
merged_df = pd.merge(dataset_df, predicted_df[['filename', 'predicted_label']], on='filename', how='left')

# Save result
merged_df.to_excel('C:/Users/girij/Distributed systems/Dataset/Grape/transpiration1.xlsx', index=False)

print(f"\n✅ Final merged file 'transpiration1.xlsx' saved successfully.")
