from plant_analysis import predict_grape_condition

#Define disease color mapping

disease_colors = {
    "ulcer": ([1, 0, 0, 1],"Red"),
    "gray_mold": ([0.5, 0.5, 0.5, 1],"Gray"),
    "black_mold": ([0, 0, 0, 1],"Black"),
    "powdery_mildew": ([1, 1, 1, 1],"White"),
    "sour_rot": ([1, 1, 0, 1],"Yellow"),
    "mosaic_virus": ([0, 1, 0, 1],"Green"),
    "downy_mildew": ([0, 0, 1, 1],"Blue"),
}

# Path to your test image
image_path = "C:/Users/girij/Distributed systems/captured_images/image_787.png"

# Run prediction
result = predict_grape_condition(image_path)
status = result['status'].lower()

# Get color information
if status in disease_colors:
    rgba, color_name = disease_colors[status]
    print(f"Prediction for {image_path} -> Disease : {status.upper()}, Confidence: {result['confidence']:.2f}")
    print(f"Disease Color: {color_name} | RGBA: {rgba}")
else:
    print(f"Prediction for {image_path} -> Disease: {status.upper()} (Unknown), Confidence: {result['confidence']:.2f}")
    print("Disease Color:  Unknown")

# Output result
print(f"Prediction for {image_path} -> {result}")
