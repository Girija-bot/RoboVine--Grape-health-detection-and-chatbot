import os
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

# Define sample path
sample_path = "C:/Users/girij/Distributed systems/Dataset/Grape/DiseaseSamples"

# Load model
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# Load sample features only once
sample_features = []
sample_labels = []

def load_sample_features():
    global sample_features, sample_labels
    print("🔁 Loading sample features...")

    valid_exts = [".jpg", ".jpeg", ".png"]
    files = [f for f in os.listdir(sample_path) if f.lower().endswith(tuple(valid_exts))]

    for fname in files:
        fpath = os.path.join(sample_path, fname)
        feat = extract_features(fpath)
        if feat is not None:
            sample_features.append(feat[0])
            label = os.path.splitext(fname)[0]
            sample_labels.append(label)

    sample_features_np = np.array(sample_features)
    return sample_features_np, sample_labels

def extract_features(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        return features
    except Exception as e:
        print(f"❌ Error processing {img_path}: {e}")
        return None

def predict_grape_condition(uploaded_path):
    features = extract_features(uploaded_path)
    if features is None:
        return {"status": "Unknown", "confidence": 0.0}

    if not sample_features:
        load_sample_features()

    sims = cosine_similarity(features, np.array(sample_features))[0]
    best_idx = np.argmax(sims)
    return {
        "status": sample_labels[best_idx],
        "confidence": float(sims[best_idx])
    }
#if _name_ == "_main_":
    #uploaded_path = "C:/Users/girij/Distributed systems/captured_images/image_3935.png"
    #result = predict_grape_condition(uploaded_path)
    #print(f"Prediction: {result}")
