# 🚕 纽约出租车数据分析 🚕 NYC Taxi Analysis Dashboard


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


### 📊 Data Analysis Dimensions
- **Popular Route Analysis**: Showcases the top 15 busiest taxi routes
- **Temporal Distribution Analysis**: Trip distribution patterns by hour and day of week
- **Hotspot Analysis**: Most frequent pickup and dropoff zones
- **Fare Analysis**: Fare distribution, distance-fare relationship visualization
- **Passenger Statistics**: Trip distribution by passenger count
- **Cluster Analysis**: Trip pattern clustering results
- **Map View**: Interactive map displaying hotspot zones

### 🎨 Visualization Features
- Responsive design, adaptable to various screen sizes
- Interactive charts (hover for details)
- Multiple chart types: bar, line, scatter, bubble, histogram
- Interactive map markers
- Data export functionality (CSV format)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit 1.28.0+
- Pandas, NumPy, Plotly

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nyc-taxi-streamlit.git
cd nyc-taxi-streamlit
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Prepare the data**

```bash
# Ensure data files are in the correct location
mkdir -p data/processed
# Place CSV data files into the data/processed/ directory
```

4. **Run the application**

```bash
streamlit run app.py
```

## 📁 Project Structure
```
nyc-taxi-streamlit/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── data/                    # Data directory
│   └── processed/           # Processed data files
│       ├── hot_routes.csv           # Popular routes data
│       ├── hourly_traffic.csv       # Hourly traffic data
│       ├── daily_traffic.csv        # Daily traffic data
│       ├── pickup_hotspots.csv      # Pickup hotspot data
│       ├── dropoff_hotspots.csv     # Dropoff hotspot data
│       ├── passenger_stats.csv      # Passenger statistics
│       ├── cluster_stats.csv        # Cluster statistics
│       └── taxi_zones_processed.csv # Geographic location data
└── .streamlit/              # Streamlit configuration
    └── config.toml          # App configuration
```

## 📊 Data Description
### Data Files
- **hot_routes.csv** - Popular route statistics  
  Columns: PULocationID, DOLocationID, trip_count, avg_distance, avg_fare, avg_tip
- **hourly_traffic.csv** - Hourly traffic statistics  
  Columns: pickup_hour, trip_count, avg_fare, avg_distance
- **daily_traffic.csv** - Daily traffic statistics  
  Columns: pickup_dayofweek, trip_count, avg_fare
- **pickup_hotspots.csv** - Pickup hotspot statistics  
  Columns: PULocationID, pickup_count, avg_fare, avg_distance
- **dropoff_hotspots.csv** - Dropoff hotspot statistics  
  Columns: DOLocationID, dropoff_count, avg_fare
- **passenger_stats.csv** - Passenger statistics  
  Columns: passenger_count, trip_count, avg_fare, avg_distance
- **cluster_stats.csv** - Cluster statistics  
  Columns: prediction, trip_count, avg_trip_distance, avg_total_amount
- **taxi_zones_processed.csv** - Geographic location data  
  Columns: location_id, borough, zone_name, latitude, longitude

## 🎯 Usage Instructions
### Local Execution
```bash
# 1. Install dependencies
pip install streamlit pandas plotly numpy

# 2. Run the application (using port 8080)
streamlit run app.py --server.port=8080 --server.address=0.0.0.0

# 3. Open in your browser
#    http://localhost:8080  or
#    http://0.0.0.0:8080
```

### Running on Google Cloud Shell
```bash
# Set environment variables to disable WebSocket (required for Cloud Shell)
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_SERVER_ENABLE_CORS=false

# Run the application
streamlit run app.py --server.port=8080 --server.address=0.0.0.0

# Use Cloud Shell's web preview feature to access
```

## 🌐 Deployment Options
### Option 1: Streamlit Cloud (Recommended)
1. Push your code to a GitHub repository
2. Visit https://share.streamlit.io
3. Log in with your GitHub account
4. Click "New app", select the repository and branch
5. Set `app.py` as the entry point
6. Click "Deploy"

### Option 2: Google Cloud Run
```bash
# 1. Create a Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
EOF

# 2. Build and push the image
gcloud builds submit --tag gcr.io/your-project-id/nyc-taxi-dashboard
gcloud run deploy nyc-taxi-dashboard --image gcr.io/your-project-id/nyc-taxi-dashboard --platform managed --region us-central1 --allow-unauthenticated
```

### Option 3: Heroku
```bash
# 1. Create a Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# 2. Create a runtime.txt
echo "python-3.9.13" > runtime.txt

# 3. Deploy to Heroku
heroku create nyc-taxi-dashboard
git push heroku main
```

### Option 4: Local Network Sharing
```bash
# 1. Run the application locally
streamlit run app.py --server.port=8080

# 2. Expose to the public using ngrok
ngrok http 8080

# 3. Share the URL provided by ngrok
```

## 🔧 Configuration
### Streamlit Configuration (.streamlit/config.toml)
```toml
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
```

### Environment Variables
```bash
# Optimize for Cloud Shell
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 📈 Data Analysis Insights
### Key Findings
- **Peak Hours**: Identify the busiest times of day
- **Popular Routes**: Discover the most frequently used taxi routes
- **Fare Patterns**: Analyze the relationship between distance and fare
- **Area Hotspots**: Identify zones with the highest pickup and dropoff frequencies
- **Passenger Patterns**: Analyze trip characteristics by passenger count
- **Trip Clusters**: Discover different types of trip patterns

### Business Applications
- Taxi dispatch optimization
- Pricing strategy formulation
- Zone service planning
- Resource allocation decision support

## 🛠️ Technology Stack
- **Frontend Framework**: Streamlit
- **Visualization Libraries**: Plotly, Streamlit built-in charts
- **Data Processing**: Pandas, NumPy
- **Map Display**: Streamlit map component
- **Deployment Platforms**: Streamlit Cloud / Google Cloud Run / Heroku

## 🤝 Contributing Guide
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact
For questions or suggestions, please reach out via:

- Project Issues: [GitHub Issues](https://github.com/inneedloveBu/nyc-taxi-streamlit/issues)
- Email: your.email@example.com

## 🙏 Acknowledgements
- Data source: New York City Taxi and Limousine Commission (TLC)
- The Streamlit team for their excellent framework
- All contributors and users

⭐ If this project helps you, please give it a Star!

### 📊 数据分析维度
- **热门路线分析**：展示Top 15最繁忙的出租车路线
- **时间分布分析**：每小时和每周的行程分布模式
- **热点区域分析**：上下车最频繁的区域分布
- **费用分析**：费用分布、距离-费用关系可视化
- **乘客统计**：不同乘客数量的行程分布
- **聚类分析**：行程模式聚类结果展示
- **地图视图**：交互式地图显示热点区域

### 🎨 可视化特性
- 响应式设计，支持各种屏幕尺寸
- 交互式图表（悬停查看详情）
- 多种图表类型：柱状图、折线图、散点图、气泡图、直方图
- 交互式地图标记
- 数据导出功能（CSV格式）

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Streamlit 1.28.0+
- Pandas, NumPy, Plotly

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/nyc-taxi-streamlit.git
cd nyc-taxi-streamlit
安装依赖

bash
pip install -r requirements.txt
准备数据

bash
# 确保数据文件位于正确位置
mkdir -p data/processed
# 将CSV数据文件放入 data/processed/ 目录
运行应用

bash
streamlit run app.py
📁 项目结构
nyc-taxi-streamlit/
├── app.py                    # 主应用程序
├── requirements.txt          # Python依赖包
├── README.md                # 项目说明文档
├── data/                    # 数据目录
│   └── processed/           # 处理后的数据文件<img width="1440" height="765" alt="1" src="https://github.com/user-attachments/assets/9ab7bcf7-1a50-4475-9b4d-6b08d546cf5c" />
<img width="1440" height="765" alt="2" src="https://github.com/user-attachments/assets/e8cc822b-a1cb-4270-9da8-649ba7210e91" />
<img width="1440" height="765" alt="3" src="https://github.com/user-attachments/assets/cafb4b8e-8118-485b-a934-c568ae0a3c15" />

│       ├── hot_routes.csv           # 热门路线数据
│       ├── hourly_traffic.csv       # 小时流量数据
│       ├── daily_traffic.csv        # 每日流量数据
│       ├── pickup_hotspots.csv      # 上车热点数据
│       ├── dropoff_hotspots.csv     # 下车热点数据
│       ├── passenger_stats.csv      # 乘客统计数据
│       ├── cluster_stats.csv        # 聚类统计数据
│       └── taxi_zones_processed.csv # 地理位置数据
└── .streamlit/              # Streamlit配置文件
    └── config.toml          # 应用配置
📊 数据说明
数据文件说明
hot_routes.csv - 热门路线统计

列：PULocationID, DOLocationID, trip_count, avg_distance, avg_fare, avg_tip

hourly_traffic.csv - 小时流量统计

列：pickup_hour, trip_count, avg_fare, avg_distance

daily_traffic.csv - 每日流量统计

列：pickup_dayofweek, trip_count, avg_fare

pickup_hotspots.csv - 上车热点统计

列：PULocationID, pickup_count, avg_fare, avg_distance

dropoff_hotspots.csv - 下车热点统计

列：DOLocationID, dropoff_count, avg_fare

passenger_stats.csv - 乘客统计

列：passenger_count, trip_count, avg_fare, avg_distance

cluster_stats.csv - 聚类统计

列：prediction, trip_count, avg_trip_distance, avg_total_amount

taxi_zones_processed.csv - 地理位置数据

列：location_id, borough, zone_name, latitude, longitude

🎯 使用说明
本地运行
bash
# 1. 安装依赖
pip install streamlit pandas plotly numpy

# 2. 运行应用（使用8080端口）
streamlit run app.py --server.port=8080 --server.address=0.0.0.0

# 3. 在浏览器中访问
#    http://localhost:8080 或
#    http://0.0.0.0:8080
在Google Cloud Shell中运行
bash
# 设置环境变量禁用WebSocket（Cloud Shell需要）
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_SERVER_ENABLE_CORS=false

# 运行应用
streamlit run app.py --server.port=8080 --server.address=0.0.0.0

# 使用Cloud Shell的Web预览功能访问
🌐 部署选项
选项一：Streamlit Cloud（推荐）
将代码推送到GitHub仓库

访问 https://share.streamlit.io

使用GitHub账号登录

点击"New app"，选择仓库和分支

设置app.py为入口文件

点击"Deploy"

选项二：Google Cloud Run
bash
# 1. 创建Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
EOF

# 2. 构建和推送镜像
gcloud builds submit --tag gcr.io/your-project-id/nyc-taxi-dashboard
gcloud run deploy nyc-taxi-dashboard --image gcr.io/your-project-id/nyc-taxi-dashboard --platform managed --region us-central1 --allow-unauthenticated
选项三：Heroku
bash
# 1. 创建Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# 2. 创建runtime.txt
echo "python-3.9.13" > runtime.txt

# 3. 部署到Heroku
heroku create nyc-taxi-dashboard
git push heroku main
选项四：本地网络共享
bash
# 1. 在本地运行应用
streamlit run app.py --server.port=8080

# 2. 使用ngrok暴露到公网
ngrok http 8080

# 3. 分享ngrok提供的URL
🔧 配置说明
Streamlit配置 (.streamlit/config.toml)
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
环境变量
bash
# 优化Cloud Shell环境
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
📈 数据分析洞察
主要发现
高峰时段：识别一天中最繁忙的时间段

热门路线：发现最常使用的出租车路线

费用模式：分析距离和费用的关系

区域热点：识别上下车最频繁的区域

乘客模式：分析不同乘客数量的行程特征

行程聚类：发现不同类型的行程模式

业务应用
出租车调度优化

价格策略制定

区域服务规划

资源分配决策支持

🛠️ 技术栈
前端框架: Streamlit

可视化库: Plotly, Streamlit内置图表

数据处理: Pandas, NumPy

地图展示: Streamlit地图组件

部署平台: Streamlit Cloud / Google Cloud Run / Heroku

🤝 贡献指南
Fork本仓库

创建功能分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

打开Pull Request

📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情

📞 联系方式
如有问题或建议，请通过以下方式联系：

项目Issues: GitHub Issues

邮箱: your.email@example.com

🙏 致谢
数据来源：纽约市出租车和豪华轿车委员会（TLC）

Streamlit团队提供的优秀框架

所有贡献者和用户

⭐ 如果这个项目对你有帮助，请给它一个Star！










