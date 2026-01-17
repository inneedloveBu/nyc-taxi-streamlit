#!/bin/bash    run_cloudshell.sh
# Cloud Shell专用启动脚本

echo "========================================"
echo "NYC Taxi Streamlit应用 - Cloud Shell版本"
echo "========================================"

# 设置环境变量
export STREAMLIT_SERVER_PORT=8080
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_HEADLESS=true

# 停止可能已在运行的Streamlit进程
echo "检查并停止已有进程..."
pkill -f "streamlit.*8080" 2>/dev/null || true

# 显示端口信息
echo ""
echo "启动Streamlit服务器..."
echo "使用端口: 8080"
echo ""
echo "等待应用启动后，请点击Cloud Shell右上角的"
echo "📊 'Web预览'按钮，然后选择'在端口8080上预览'"
echo "========================================"

# 运行Streamlit
streamlit run app.py \
  --server.port=8080 \
  --server.address=0.0.0.0 \
  --browser.serverAddress="localhost" \
  --theme.base="light" \
  --logger.level="info"