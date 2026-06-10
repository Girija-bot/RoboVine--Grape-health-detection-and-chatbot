# 🍇 RoboVine — AI-Powered Grape Health Detection & Vineyard Monitoring

An end-to-end precision agriculture system combining **computer vision**, **robotics simulation**, **time-series forecasting**, and a **natural language chatbot** to monitor and manage grapevine health.

---

## 🌱 Project Overview

Modern viticulture faces mounting challenges: early disease detection, efficient field monitoring, and data-driven crop management. RoboVine addresses all three by integrating:

- A **CNN-based disease classifier** that identifies grape health conditions from leaf images
- A **simulated autonomous robot** that navigates a virtual vineyard and logs camera feeds
- **Time-series forecasting** of key plant physiological metrics (transpiration, biomass gain, stomatal conductance)
- A **conversational chatbot** for farmer-friendly interaction with the system

---

## 🧠 System Architecture

### 1. Disease Detection — CNN (PyTorch)
**Files:** `train.py`, `model.py`, `camera_detection.py`

- CNN trained on grape leaf image datasets to classify health conditions (healthy vs. disease variants)
- Full ML pipeline: data loading → preprocessing → augmentation (flips, rotations, colour jitter) → training → evaluation
- Real-time inference via webcam feed (`camera_detection.py`) — images captured from the robot are piped into the classifier
- `check_color.py` provides additional colour-space analysis for early stress detection

### 2. Robot Simulation
**Files:** `robot_movement.py`, `robot_image_logger.py`, `field_setup.py`

- Simulates a **three-wheeled autonomous robot** navigating a virtual vineyard grid
- `field_setup.py` defines the vineyard layout (plant rows, spacing, coordinates)
- Robot logs images at each plant node (`robot_image_logger.py`), feeding them into the disease detection pipeline
- Movement and detection are decoupled — the robot navigates independently while the ML model processes captures asynchronously
- Simulation logs saved to `simulation_log.csv` for post-analysis

### 3. Plant Health Forecasting
**Files:** `forecast.py`, `new_prophet.py`, `plant_analysis.py`, `plantarray.py`

- Time-series forecasting of plant physiological signals using **Facebook Prophet**
- Metrics forecasted:
  - **Transpiration rate** (hourly and daily aggregates)
  - **Normalized transpiration** (plant water stress indicator)
  - **Stomatal conductance** (AM and PM windows: 6–7am, 12–1pm)
  - **Biomass gain** (growth rate proxy)
- Data extracted and merged from phenological parameter sheets (`data_extraction.py`, `merge1.py`)
- Forecast outputs exported as CSV + PNG plots for agronomic reporting

### 4. Chatbot Interface
**File:** `chatbot.py`

- Natural language interface allowing farmers to query vineyard status
- Integrated with the detection and forecast modules to answer questions like:
  - *"Which plants showed disease today?"*
  - *"What is the predicted transpiration for tomorrow?"*

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Disease Classification | PyTorch (CNN) |
| Image Processing | OpenCV, PIL |
| Data Analysis | Pandas, NumPy |
| Time-Series Forecasting | Facebook Prophet |
| Chatbot | Python (custom NLP interface) |
| Robotics Simulation | Python (custom grid navigator) |
| Data Storage | CSV, XLSX |
| Language | Python |

---

## 📁 Project Structure

```
├── train.py                    # CNN training pipeline
├── model.py                    # Model architecture definition
├── camera_capture.py           # Webcam image capture
├── camera_detection.py         # Real-time inference on camera feed
├── robot_movement.py           # Robot navigation simulation
├── robot_image_logger.py       # Logs images at each plant node
├── field_setup.py              # Vineyard grid layout configuration
├── plant_analysis.py           # Per-plant health analysis
├── plantarray.py               # Plant data structures
├── forecast.py                 # Prophet forecasting pipeline
├── new_prophet.py              # Updated forecasting module
├── data_extraction.py          # Raw data extraction from phenological sheets
├── merge1.py / m3.py           # Data merging and preprocessing
├── chatbot.py                  # Natural language chatbot interface
├── app.py                      # Application entry point
├── Phenological parameters.xlsx  # Source phenological data
├── merged_full_data.xlsx       # Processed merged dataset
└── simulation_log.csv          # Robot simulation output log
```

---

## 📊 Sample Forecast Outputs

The system generates forecast plots for key physiological indicators:

- `Forecast_Normalized_Transpiration.png` — plant water stress over time
- `Forecast_Stomatal_Conductance_6-7am.png` — early morning conductance
- `Forecast_Stomatal_Conductance_12-1pm.png` — midday stress window
- `Mean_Biomass_Gain_forecast.png` — growth rate projection

---

## ⚙️ Setup & Run

```bash
# Clone the repo
git clone https://github.com/Girija-bot/RoboVine--Grape-health-detection-and-chatbot.git
cd RoboVine--Grape-health-detection-and-chatbot

# Install dependencies
pip install torch torchvision opencv-python pandas numpy prophet langchain flask

# Train the model (or load existing weights)
python train.py

# Run full system
python main.py

# Run chatbot only
python chatbot.py

# Run forecasting
python forecast.py
```

---

## 🔑 Key Technical Highlights

**End-to-end ownership:** Built every layer of the system — data collection, ML model, robotics, forecasting, and user interface — independently.

**Multi-modal AI:** Combines image classification (CNN), time-series prediction (Prophet), and natural language interaction (chatbot) in one integrated system.

**Real-world domain:** Targets precision viticulture — a high-value agricultural sector where early disease detection directly impacts crop yield and economic outcome.

**Asynchronous robot + vision:** Robot navigation and ML inference are decoupled, allowing the simulation to run at full speed while the CNN processes images in parallel.

---

## 👤 Author

**Girija Jyothi Golla** — Junior ML Engineer  
[LinkedIn](https://linkedin.com/in/girija-j-815a131b7) · [GitHub](https://github.com/Girija-bot)
