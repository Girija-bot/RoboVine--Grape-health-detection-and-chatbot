import os
import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# Set paths
sample_path = "C:/Users/girij/Distributed systems/Dataset/Grape/DiseaseSamples"
unlabeled_path = "C:/Users/girij/Distributed systems/Dataset/Grape"
output_csv_path = os.path.join(unlabeled_path, "predicted_results.csv")
log_path = "skipped_images.log"

# Load pre-trained model
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# Allowed image extensions
valid_exts = [".jpg", ".jpeg", ".png"]

def is_image_file(file):
    return file.lower().endswith(tuple(valid_exts))

def extract_features(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        return features
    except Exception as e:
        print(f"❌ Failed to process {img_path}: {e}")
        return None

# Load and extract features from sample images
sample_features = []
sample_labels = []

print("🔍 Extracting features from sample images...")
sample_files = [f for f in os.listdir(sample_path) if is_image_file(f)]
print("📁 Files in sample_images_path:", sample_files)

for fname in sample_files:
    fpath = os.path.join(sample_path, fname)
    feature = extract_features(fpath)
    if feature is not None:
        sample_features.append(feature[0])
        label = os.path.splitext(fname)[0]
        sample_labels.append(label)

sample_features = np.array(sample_features)

# Safety check
if len(sample_features) == 0:
    raise ValueError("⚠️ No sample features extracted. Please check sample images.")

# Predict disease for unlabeled images
print("🧪 Predicting diseases for unlabeled images...")
results = []
skipped = []

for fname in tqdm(os.listdir(unlabeled_path)):
    fpath = os.path.join(unlabeled_path, fname)

    if not is_image_file(fname):
        skipped.append(fname)
        continue

    feature = extract_features(fpath)
    if feature is None:
        skipped.append(fname)
        continue

    try:
        similarities = cosine_similarity(feature, sample_features)[0]
        predicted_index = np.argmax(similarities)
        predicted_label = sample_labels[predicted_index]
        results.append({"filename": fname, "predicted_label": predicted_label})
    except Exception as e:
        print(f"⚠️ Error comparing features for {fname}: {e}")
        skipped.append(fname)

# Save results
pd.DataFrame(results).to_csv(output_csv_path, index=False)
print(f"✅ Predictions saved to {output_csv_path}")

# Save skipped image names
if skipped:
    with open(log_path, "w") as f:
        for item in skipped:
            f.write(f"{item}\n")
    print(f"⚠️ Skipped images logged in {log_path}")
    print(f"🔍 Total skipped images: {len(skipped)}")
    print("🕵️‍♂️ Skipped images (missing from CSV):", skipped)

