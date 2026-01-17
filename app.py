# NYC Taxi Dashboard - 修复气泡大小和聚类颜色问题
import os
import sys
import time
from pathlib import Path

# 设置环境变量
os.environ["STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"

# 导入库
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="NYC Taxi Dashboard",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主标题
st.title("🚕 NYC Taxi 高级分析仪表板")
st.markdown("---")

# 加载数据函数
@st.cache_data(ttl=300)
def load_all_data():
    """加载所有数据文件"""
    data_dir = Path("data/processed")
    data_dict = {}
    
    if not data_dir.exists():
        st.error(f"数据目录不存在: {data_dir}")
        return {}
    
    csv_files = list(data_dir.glob("*.csv"))
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            data_dict[csv_file.stem] = df
        except Exception as e:
            st.warning(f"无法读取 {csv_file.name}: {e}")
    
    return data_dict

# 显示加载状态
with st.spinner("正在加载数据..."):
    data = load_all_data()

if not data:
    st.error("❌ 没有找到数据文件")
    st.stop()

# 显示数据概览
st.subheader("📊 数据概览")

# 创建指标卡片
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("数据文件数", len(data))

with col2:
    total_rows = sum(len(df) for df in data.values())
    st.metric("总数据行数", f"{total_rows:,}")

with col3:
    if 'hot_routes' in data:
        st.metric("热门路线数", f"{len(data['hot_routes']):,}")
    else:
        st.metric("热门路线数", "0")

with col4:
    if 'hot_routes' in data:
        total_trips = data['hot_routes']['trip_count'].sum()
        st.metric("总行程数", f"{int(total_trips):,}")
    else:
        st.metric("总行程数", "0")

# 创建标签页
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🔥 热门路线", "⏰ 时间分析", "📍 热点区域", 
    "💰 费用分析", "👥 乘客统计", "📊 聚类分析", "🗺️ 地图视图"
])

with tab1:
    st.subheader("🔥 热门路线分析")
    
    if 'hot_routes' in data and len(data['hot_routes']) > 0:
        hot_routes = data['hot_routes'].copy()
        
        # 按行程数排序，取前15条
        top_routes = hot_routes.sort_values('trip_count', ascending=False).head(15)
        
        x_labels = top_routes['PULocationID'].astype(str) + ' → ' + top_routes['DOLocationID'].astype(str)
        
        fig = go.Figure(data=[
            go.Bar(
                x=x_labels.tolist(),
                y=top_routes['trip_count'].tolist()
            )
        ])
        
        fig.update_layout(
            title='Top 15 热门路线',
            xaxis_title='路线 (上车→下车)',
            yaxis_title='行程数',
            xaxis_tickangle=45,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("热门路线数据未找到")

with tab2:
    st.subheader("⏰ 时间分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'hourly_traffic' in data and len(data['hourly_traffic']) > 0:
            hourly = data['hourly_traffic'].copy()
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=hourly['pickup_hour'].tolist(),
                    y=hourly['trip_count'].tolist(),
                    mode='lines+markers',
                    name='行程数'
                )
            ])
            
            fig.update_layout(
                title='每小时行程分布',
                xaxis_title='小时',
                yaxis_title='行程数',
                xaxis=dict(tickmode='linear', dtick=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 找到高峰时段
            if len(hourly) > 0:
                peak_hour = hourly.loc[hourly['trip_count'].idxmax()]
                st.info(f"**高峰时段**: {int(peak_hour['pickup_hour'])}:00，行程数: {int(peak_hour['trip_count']):,}")
                
        else:
            st.info("小时流量数据未找到")
    
    with col2:
        if 'daily_traffic' in data and len(data['daily_traffic']) > 0:
            daily = data['daily_traffic'].copy()
            
            # 映射星期名称
            days_map = {1: '周日', 2: '周一', 3: '周二', 4: '周三', 
                      5: '周四', 6: '周五', 7: '周六'}
            daily['day_name'] = daily['pickup_dayofweek'].map(days_map)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=daily['day_name'].tolist(),
                    y=daily['trip_count'].tolist()
                )
            ])
            
            fig.update_layout(
                title='星期行程分布',
                xaxis_title='星期',
                yaxis_title='行程数'
            )
            
            st.plotly_chart(fig, use_container_width=True)
                
        else:
            st.info("每日流量数据未找到")

with tab3:
    st.subheader("📍 热点区域分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'pickup_hotspots' in data and len(data['pickup_hotspots']) > 0:
            pickup_hotspots = data['pickup_hotspots'].copy()
            
            # 按上车次数排序，取前10条
            top_pickup = pickup_hotspots.sort_values('pickup_count', ascending=False).head(10)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=top_pickup['PULocationID'].astype(str).tolist(),
                    y=top_pickup['pickup_count'].tolist()
                )
            ])
            
            fig.update_layout(
                title='上车热点区域 TOP 10',
                xaxis_title='区域ID',
                yaxis_title='上车次数'
            )
            
            st.plotly_chart(fig, use_container_width=True)
                
        else:
            st.info("上车热点数据未找到")
    
    with col2:
        if 'dropoff_hotspots' in data and len(data['dropoff_hotspots']) > 0:
            dropoff_hotspots = data['dropoff_hotspots'].copy()
            
            # 按下车次数排序，取前10条
            top_dropoff = dropoff_hotspots.sort_values('dropoff_count', ascending=False).head(10)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=top_dropoff['DOLocationID'].astype(str).tolist(),
                    y=top_dropoff['dropoff_count'].tolist()
                )
            ])
            
            fig.update_layout(
                title='下车热点区域 TOP 10',
                xaxis_title='区域ID',
                yaxis_title='下车次数'
            )
            
            st.plotly_chart(fig, use_container_width=True)
                
        else:
            st.info("下车热点数据未找到")

with tab4:
    st.subheader("💰 费用分析")
    
    if 'hot_routes' in data and len(data['hot_routes']) > 0:
        hot_routes = data['hot_routes'].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 费用分布直方图
            fig = go.Figure(data=[
                go.Histogram(
                    x=hot_routes['avg_fare'].tolist(),
                    nbinsx=20
                )
            ])
            
            fig.update_layout(
                title='费用分布直方图',
                xaxis_title='平均费用 ($)',
                yaxis_title='频次'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # 费用统计
            avg_fare = hot_routes['avg_fare'].mean()
            max_fare = hot_routes['avg_fare'].max()
            min_fare = hot_routes['avg_fare'].min()
            
            st.metric("平均费用", f"${avg_fare:.2f}")
            st.metric("最高费用", f"${max_fare:.2f}")
            st.metric("最低费用", f"${min_fare:.2f}")
        
        # 距离-费用关系气泡图
        st.subheader("📏 距离 vs 费用关系")
        
        # 取前50条热门路线进行分析
        scatter_data = hot_routes.sort_values('trip_count', ascending=False).head(50)
        
        if len(scatter_data) > 0:
            # 计算气泡大小 - 这里改小了气泡的半径
            # 原始：bubble_size = scatter_data['trip_count'] / scatter_data['trip_count'].max() * 40
            # 改小：使用更小的乘数，比如15，并且调整sizeref使气泡更小
            
            # 调整气泡大小的计算方法
            bubble_size = scatter_data['trip_count'] / scatter_data['trip_count'].max() * 20  # 从40改小到20
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=scatter_data['avg_distance'].tolist(),
                    y=scatter_data['avg_fare'].tolist(),
                    mode='markers',
                    marker=dict(
                        size=bubble_size.tolist(),
                        sizemode='diameter',  # 直径模式
                        sizeref=2.0,  # 增大sizeref会使气泡更小，从0.1增加到2.0
                        sizemin=1,  # 最小尺寸
                        color=scatter_data['trip_count'].tolist(),
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title='行程数')
                    ),
                    text=[f"路线: {pu}→{do}<br>行程数: {count}<br>距离: {dist:.2f}<br>费用: ${fare:.2f}" 
                          for pu, do, count, dist, fare in zip(
                              scatter_data['PULocationID'], 
                              scatter_data['DOLocationID'],
                              scatter_data['trip_count'],
                              scatter_data['avg_distance'],
                              scatter_data['avg_fare']
                          )],
                    hoverinfo='text'
                )
            ])
            
            # 自动调整坐标轴范围，让点更分散
            x_min = scatter_data['avg_distance'].min()
            x_max = scatter_data['avg_distance'].max()
            y_min = scatter_data['avg_fare'].min()
            y_max = scatter_data['avg_fare'].max()
            
            # 添加15%的边距
            x_padding = (x_max - x_min) * 0.15
            y_padding = (y_max - y_min) * 0.15
            
            # 确保最小值不为负数（如果数据都是正数）
            x_range = [max(0, x_min - x_padding), x_max + x_padding]
            y_range = [max(0, y_min - y_padding), y_max + y_padding]
            
            fig.update_layout(
                title='距离 vs 费用关系 (气泡大小表示行程数)',
                xaxis_title='平均距离',
                yaxis_title='平均费用 ($)',
                height=500,
                xaxis=dict(range=x_range),
                yaxis=dict(range=y_range)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 计算相关系数
            correlation = scatter_data['avg_distance'].corr(scatter_data['avg_fare'])
            st.metric("距离-费用相关系数", f"{correlation:.3f}")
            
    else:
        st.info("热门路线数据未找到")

with tab5:
    st.subheader("👥 乘客统计")
    
    if 'passenger_stats' in data and len(data['passenger_stats']) > 0:
        passenger_stats = data['passenger_stats'].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    x=passenger_stats['passenger_count'].tolist(),
                    y=passenger_stats['trip_count'].tolist()
                )
            ])
            
            fig.update_layout(
                title='乘客数量分布',
                xaxis_title='乘客数',
                yaxis_title='行程数'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("乘客统计详情:")
            st.dataframe(passenger_stats, use_container_width=True)
    else:
        st.info("乘客统计数据未找到")

with tab6:
    st.subheader("📊 聚类分析")
    
    if 'cluster_stats' in data and len(data['cluster_stats']) > 0:
        cluster_stats = data['cluster_stats'].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    x=cluster_stats['prediction'].astype(str).tolist(),
                    y=cluster_stats['trip_count'].tolist()
                )
            ])
            
            fig.update_layout(
                title='聚类行程分布',
                xaxis_title='聚类编号',
                yaxis_title='行程数'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if len(cluster_stats) >= 2:
                # 修复聚类特征散点图颜色问题
                fig = go.Figure()
                
                # 为每个聚类创建单独的数据点
                unique_clusters = cluster_stats['prediction'].unique()
                
                # 使用不同的颜色和标记符号
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
                markers = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up']
                
                for i, cluster in enumerate(unique_clusters):
                    cluster_data = cluster_stats[cluster_stats['prediction'] == cluster]
                    
                    # 计算气泡大小 - 减小气泡尺寸
                    bubble_size = cluster_data['trip_count'] / cluster_stats['trip_count'].max() * 25
                    
                    fig.add_trace(go.Scatter(
                        x=cluster_data['avg_trip_distance'].tolist(),
                        y=cluster_data['avg_total_amount'].tolist(),
                        mode='markers',
                        name=f'聚类 {cluster}',
                        marker=dict(
                            size=bubble_size.tolist(),
                            sizemode='diameter',
                            sizeref=2.0,  # 增大sizeref使气泡更小
                            color=colors[i % len(colors)],  # 使用离散颜色
                            symbol=markers[i % len(markers)],  # 使用不同标记符号
                            line=dict(width=1, color='black')  # 添加边框
                        ),
                        text=[f"聚类: {pred}<br>行程数: {count}<br>距离: {dist:.2f}<br>费用: ${amt:.2f}" 
                              for pred, count, dist, amt in zip(
                                  cluster_data['prediction'],
                                  cluster_data['trip_count'],
                                  cluster_data['avg_trip_distance'],
                                  cluster_data['avg_total_amount']
                              )],
                        hoverinfo='text'
                    ))
                
                fig.update_layout(
                    title='聚类特征散点图',
                    xaxis_title='平均距离',
                    yaxis_title='平均总费用 ($)',
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("聚类数据点不足，无法显示散点图")
    else:
        st.info("聚类统计数据未找到")

with tab7:
    st.subheader("🗺️ 地图视图")
    
    # 检查是否有位置数据
    if 'taxi_zones_processed' in data and len(data['taxi_zones_processed']) > 0:
        zones_df = data['taxi_zones_processed'].copy()
        
        # 创建地图选项
        map_option = st.selectbox("选择地图类型:", 
                                 ["区域位置分布", "上车热点地图", "下车热点地图"])
        
        if map_option == "区域位置分布":
            # 显示所有区域的位置
            st.map(zones_df[['latitude', 'longitude']].rename(
                columns={'latitude': 'lat', 'longitude': 'lon'}
            ))
            st.caption(f"显示 {len(zones_df)} 个出租车区域")
        
        elif map_option == "上车热点地图":
            if 'pickup_hotspots' in data and len(data['pickup_hotspots']) > 0:
                pickup_hotspots = data['pickup_hotspots'].copy()
                # 合并位置信息
                pickup_map = pickup_hotspots.merge(
                    zones_df, 
                    left_on='PULocationID', 
                    right_on='location_id',
                    how='left'
                )
                
                # 过滤掉没有位置信息的行
                pickup_map = pickup_map.dropna(subset=['latitude', 'longitude'])
                
                if len(pickup_map) > 0:
                    # 创建地图数据
                    map_data = pickup_map[['latitude', 'longitude', 'pickup_count', 'PULocationID']].rename(
                        columns={'latitude': 'lat', 'longitude': 'lon'}
                    )
                    st.map(map_data)
                    st.caption(f"显示 {len(pickup_map)} 个上车热点区域")
                else:
                    st.warning("无法找到上车热点的位置信息")
            else:
                st.info("上车热点数据未找到")
        
        elif map_option == "下车热点地图":
            if 'dropoff_hotspots' in data and len(data['dropoff_hotspots']) > 0:
                dropoff_hotspots = data['dropoff_hotspots'].copy()
                # 合并位置信息
                dropoff_map = dropoff_hotspots.merge(
                    zones_df, 
                    left_on='DOLocationID', 
                    right_on='location_id',
                    how='left'
                )
                
                # 过滤掉没有位置信息的行
                dropoff_map = dropoff_map.dropna(subset=['latitude', 'longitude'])
                
                if len(dropoff_map) > 0:
                    # 创建地图数据
                    map_data = dropoff_map[['latitude', 'longitude', 'dropoff_count', 'DOLocationID']].rename(
                        columns={'latitude': 'lat', 'longitude': 'lon'}
                    )
                    st.map(map_data)
                    st.caption(f"显示 {len(dropoff_map)} 个下车热点区域")
                else:
                    st.warning("无法找到下车热点的位置信息")
            else:
                st.info("下车热点数据未找到")
    else:
        st.info("位置数据未找到，无法显示地图")

# 侧边栏
st.sidebar.title("🔧 控制面板")
st.sidebar.markdown("---")

# 应用信息
st.sidebar.subheader("ℹ️ 应用信息")
st.sidebar.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 数据文件信息
st.sidebar.subheader("📁 数据文件")
for name in sorted(data.keys()):
    st.sidebar.write(f"• {name}: {len(data[name])}行")

# 刷新按钮
st.sidebar.markdown("---")
if st.sidebar.button("🔄 刷新数据"):
    st.cache_data.clear()
    st.rerun()

# 页脚
st.markdown("---")
st.caption(f"© 2024 NYC Taxi Analysis Dashboard | 最后更新: {datetime.now().strftime('%H:%M:%S')}")