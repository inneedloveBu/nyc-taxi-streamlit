🚕 NYC Taxi Analysis Dashboard
An interactive Streamlit-based dashboard for visualizing and analyzing NYC taxi data processed with Spark, providing rich insights and analytics.

✨ Features


- **[streamlit.app](https://nyc-taxi-app-ln639f2iesnkuqbr9jwh78.streamlit.app/)** - Interactive web interface

<img width="1440" height="765" alt="1" src="https://github.com/user-attachments/assets/aed33902-3c1a-4711-bca0-5357dd90809b" />

<img width="1440" height="765" alt="3" src="https://github.com/user-attachments/assets/b80fe89b-8b47-4de3-a706-1bb0a65ec1ce" />


<img width="1440" height="765" alt="2" src="https://github.com/user-attachments/assets/b0d8805e-66d5-47d8-a6e9-a1e84f6b2f8b" />




📊 Data Analysis Dimensions
Popular Route Analysis: Displays the Top 15 busiest taxi routes

Time Distribution Analysis: Hourly and weekly trip distribution patterns

Hotspot Area Analysis: Distribution of most frequent pickup and dropoff zones

Fare Analysis: Fare distribution and distance-fare relationship visualization

Passenger Statistics: Trip distribution by passenger count

Clustering Analysis: Visualization of trip pattern clusters

Map View: Interactive map displaying hotspot areas

🎨 Visualization Features
Responsive design supporting various screen sizes

Interactive charts (hover for details)

Multiple chart types: bar charts, line charts, scatter plots, bubble charts, histograms

Interactive map markers

Data export functionality (CSV format)

🚀 Quick Start
Requirements
Python 3.8+

Streamlit 1.28.0+

Pandas, NumPy, Plotly

Installation Steps
Clone the Repository

bash
git clone https://github.com/yourusername/nyc-taxi-streamlit.git
cd nyc-taxi-streamlit
Install Dependencies

bash
pip install -r requirements.txt
Prepare Data

bash
# Ensure data files are in the correct location
mkdir -p data/processed
# Place CSV data files into the data/processed/ directory
Run the Application

bash
streamlit run app.py
📁 Project Structure
text
nyc-taxi-streamlit/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── data/                    # Data directory
│   └── processed/           # Processed data files
│       ├── hot_routes.csv           # Popular route data
│       ├── hourly_traffic.csv       # Hourly traffic data
│       ├── daily_traffic.csv        # Daily traffic data
│       ├── pickup_hotspots.csv      # Pickup hotspot data
│       ├── dropoff_hotspots.csv     # Dropoff hotspot data
│       ├── passenger_stats.csv      # Passenger statistics
│       ├── cluster_stats.csv        # Clustering statistics
│       └── taxi_zones_processed.csv # Geographic location data
└── .streamlit/              # Streamlit configuration
    └── config.toml          # Application configuration
📊 Data Description
Data File Details
hot_routes.csv - Popular route statistics
Columns: PULocationID, DOLocationID, trip_count, avg_distance, avg_fare, avg_tip

hourly_traffic.csv - Hourly traffic statistics
Columns: pickup_hour, trip_count, avg_fare, avg_distance

daily_traffic.csv - Daily traffic statistics
Columns: pickup_dayofweek, trip_count, avg_fare

pickup_hotspots.csv - Pickup hotspot statistics
Columns: PULocationID, pickup_count, avg_fare, avg_distance

dropoff_hotspots.csv - Dropoff hotspot statistics
Columns: DOLocationID, dropoff_count, avg_fare

passenger_stats.csv - Passenger statistics
Columns: passenger_count, trip_count, avg_fare, avg_distance

cluster_stats.csv - Clustering statistics
Columns: prediction, trip_count, avg_trip_distance, avg_total_amount

taxi_zones_processed.csv - Geographic location data
Columns: location_id, borough, zone_name, latitude, longitude

🎯 Usage Instructions
Local Execution
bash
# 1. Install dependencies
pip install streamlit pandas plotly numpy

# 2. Run the app (using port 8080)
streamlit run app.py --server.port=8080 --server.address=0.0.0.0

# 3. Access in browser
#    http://localhost:8080 or
#    http://0.0.0.0:8080
Running in Google Cloud Shell
bash
# Set environment variables to disable WebSocket (required for Cloud Shell)
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_SERVER_ENABLE_CORS=false

# Run the application
streamlit run app.py --server.port=8080 --server.address=0.0.0.0

# Use Cloud Shell's Web Preview feature to access
🌐 Deployment Options
Option 1: Streamlit Cloud (Recommended)
Push your code to a GitHub repository

Visit https://share.streamlit.io

Sign in with your GitHub account

Click "New app", select repository and branch

Set app.py as the entry point

Click "Deploy"

Option 2: Google Cloud Run
bash
# 1. Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
EOF

# 2. Build and push image
gcloud builds submit --tag gcr.io/your-project-id/nyc-taxi-dashboard
gcloud run deploy nyc-taxi-dashboard --image gcr.io/your-project-id/nyc-taxi-dashboard --platform managed --region us-central1 --allow-unauthenticated
Option 3: Heroku
bash
# 1. Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# 2. Create runtime.txt
echo "python-3.9.13" > runtime.txt

# 3. Deploy to Heroku
heroku create nyc-taxi-dashboard
git push heroku main
Option 4: Local Network Sharing
bash
# 1. Run the app locally
streamlit run app.py --server.port=8080

# 2. Expose to the internet using ngrok
ngrok http 8080

# 3. Share the URL provided by ngrok
🔧 Configuration
Streamlit Configuration (.streamlit/config.toml)
toml
[server]
port = 8080
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "localhost"

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
Environment Variables
bash
# Optimize for Cloud Shell environment
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
📈 Data Analysis Insights
Key Findings
Peak Hours: Identification of the busiest time periods during the day

Popular Routes: Discovery of the most frequently used taxi routes

Fare Patterns: Analysis of the relationship between distance and fare

Zone Hotspots: Identification of areas with the highest pickup and dropoff frequency

Passenger Patterns: Analysis of trip characteristics by passenger count

Trip Clustering: Discovery of different types of trip patterns

Business Applications
Taxi dispatch optimization

Pricing strategy formulation

Regional service planning

Resource allocation decision support

🛠️ Tech Stack
Frontend Framework: Streamlit

Visualization Libraries: Plotly, Streamlit built-in charts

Data Processing: Pandas, NumPy

Map Display: Streamlit map components

Deployment Platforms: Streamlit Cloud / Google Cloud Run / Heroku

🤝 Contributing
Fork this repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📞 Contact
For questions or suggestions, please reach out via:

Project Issues: GitHub Issues

Email: your.email@example.com

🙏 Acknowledgments
Data Source: New York City Taxi and Limousine Commission (TLC)

Streamlit team for the excellent framework

All contributors and users


⭐ If you find this project helpful, please give it a Star!
