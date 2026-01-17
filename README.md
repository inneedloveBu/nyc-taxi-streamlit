# 🚕 NYC Taxi Analysis Dashboard

一个基于Streamlit的交互式纽约出租车数据分析仪表板，可视化Spark处理结果，提供丰富的分析和洞察。

## ✨ 功能特点

- **[streamlit.app](https://nyc-taxi-app-ln639f2iesnkuqbr9jwh78.streamlit.app/)** - Interactive web interface

<img width="1440" height="765" alt="1" src="https://github.com/user-attachments/assets/8d7087d1-481e-49bd-9e76-facc13744633" />

<img width="1440" height="765" alt="3" src="https://github.com/user-attachments/assets/0117324b-8538-4ac7-83c2-4de8995deb80" />

<img width="1440" height="765" alt="2" src="https://github.com/user-attachments/assets/5e185320-85eb-4511-834f-6ac0265f4fa5" />



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



