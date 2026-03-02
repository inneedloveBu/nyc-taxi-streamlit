# 🚕 纽约出租车数据分析 🚕 NYC Taxi Fare Prediction Web App

[![bilibili](https://img.shields.io/badge/🎥-Video%20on%20Bilibili-red)](https://www.bilibili.com/video/BV1NArXB4EU5/?share_source=copy_web&vd_source=56cdc7ef44ed1ee2c9b9515febf8e9ce&t=1)

[![streamlit](https://img.shields.io/badge/🤗-streamlit-blue)](https://nyc-taxi-app-ln639f2iesnkuqbr9jwh78.streamlit.app/)
[![GitHub](https://img.shields.io/badge/📂-GitHub-black)](https://github.com/inneedloveBu/nyc-taxi-streamlit)

一个基于Streamlit的交互式纽约出租车数据分析板，可视化Spark处理结果，提供丰富的分析和洞察。

An interactive New York City taxi data analysis dashboard built with Streamlit, visualizing Spark-processed results and providing rich analysis and insights.


## ✨ 功能特点 ✨ Features

- **[streamlit.app](https://nyc-taxi-app-ln639f2iesnkuqbr9jwh78.streamlit.app/)** - Interactive web interface

<img width="1440" height="765" alt="1" src="https://github.com/user-attachments/assets/8d7087d1-481e-49bd-9e76-facc13744633" />

<img width="1440" height="765" alt="3" src="https://github.com/user-attachments/assets/0117324b-8538-4ac7-83c2-4de8995deb80" />

<img width="1440" height="765" alt="2" src="https://github.com/user-attachments/assets/5e185320-85eb-4511-834f-6ac0265f4fa5" />

An end-to-end machine learning deployment project that predicts New York City taxi fares and provides an interactive web interface built with Streamlit.

This project demonstrates:

- **Feature engineering for geospatial regression**

- **Model training and evaluation**

- **Production-style inference pipeline**

- **Interactive web deployment**

- **Data visualization integration**

## Project Overview

This project predicts taxi fares using trip-related features such as pickup/dropoff coordinates, passenger count, and temporal information.

The system includes:

- **Data preprocessing pipeline**

- **Feature engineering**

- **Regression model training**

- **Model serialization**

- **Real-time web inference via Streamlit**

The focus is on transforming a machine learning model into a usable data product.

## Dataset

The dataset is derived from the NYC Taxi & Limousine Commission trip records.

### Input Features

- **Pickup longitude**

- **Pickup latitude**

- **Dropoff longitude**

- **Dropoff latitude**

- **Passenger count**

- **Pickup datetime**

### Engineered Features

- **Trip distance (Haversine formula)**

- **Hour of day**

- **Day of week**

- **Is weekend indicator**

- **Distance-based interaction features**

## Feature Engineering
### Geospatial Feature

Trip distance is calculated using the Haversine formula:

- **Accounts for Earth curvature**

- **Improves regression stability**

- **Reduces noise from raw coordinates**

### Temporal Features

- **Hour extraction**

- **Day-of-week encoding**

- **Weekend binary indicator**

These improve modeling of demand and pricing patterns.

## Model Architecture

This project supports classical regression models:

- **Linear Regression**

- **Random Forest Regressor**

- **Gradient Boosting Regressor**

Final selected model:

- **Random Forest Regressor**

Model characteristics:

- **Non-linear relationship modeling**

- **Robust to feature scaling**

- **Handles interaction effects automatically**

## Training & Evaluation
### Data Split

- **Training set: 80%**

- **Test set: 20%**

### Evaluation Metrics

- **Mean Absolute Error (MAE)**

- **Root Mean Squared Error (RMSE)**

- **R² Score**

These metrics evaluate prediction accuracy and generalization performance.

## Deployment Architecture

The system follows a simplified ML deployment pipeline:

**1.Data preprocessing**

**2.Feature transformation**

**3.Model inference**

**4.Prediction display**

**5.Visualization rendering**

The trained model is serialized using:

- **joblib**

The web interface is built with:

- **Streamlit**

## Interactive Web Application

The Streamlit app allows users to:

- Enter pickup and dropoff coordinates

- Select passenger count

- Choose date and time

- Instantly receive predicted fare

Additional features:

- **Map visualization**

- **Distance display**

- **Real-time prediction update**

## Technical Stack

- **Python 3.8+**

- **scikit-learn**

- **NumPy**

- **Pandas**

- **Matplotlib**

- **Streamlit**

- **joblib**

## Project Structure
nyc-taxi-streamlit/
├── app.py
├── model.pkl
├── data/
├── notebooks/
├── requirements.txt
└── README.md
## How to Run
**1. Clone the Repository**
git clone https://github.com/inneedloveBu/nyc-taxi-streamlit.git
cd nyc-taxi-streamlit
**2. Install Dependencies**
pip install -r requirements.txt
**3. Launch the Web App**
streamlit run app.py

The application will open in your browser.

## Key Contributions

- **Built full ML training-to-deployment pipeline**

- **Implemented geospatial distance feature engineering**

- **Integrated trained model into interactive web interface**

- **Designed real-time inference workflow**

- **Demonstrated practical ML productization**

## Future Improvements

- **Hyperparameter tuning via GridSearchCV**

- **Add XGBoost model comparison**

- **Docker containerization**

- **Cloud deployment (AWS / GCP)**

- **Live API endpoint integration**

## What This Project Demonstrates

- **Machine learning model development**

- **Geospatial feature engineering**

- **Production-style inference**

- **ML deployment skills**

- **Interactive data product design**











