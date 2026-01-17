import pandas as pd
import numpy as np
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def analyze_data():
    """简化版的数据分析"""
    print("开始分析出租车数据...")
    
    # 加载示例数据
    data_path = project_root / "data/raw/sample_taxi_data.csv"
    df = pd.read_csv(data_path)
    
    print(f"数据加载完成: {len(df)} 行")
    
    # 基本分析
    # 1. 热门路线
    df['route'] = df['PULocationID'].astype(str) + '->' + df['DOLocationID'].astype(str)
    hot_routes = df.groupby(['PULocationID', 'DOLocationID', 'route']).agg({
        'total_amount': ['count', 'mean', 'sum']
    }).reset_index()
    
    hot_routes.columns = ['PULocationID', 'DOLocationID', 'route', 'trip_count', 'avg_fare', 'total_fare']
    hot_routes = hot_routes.sort_values('trip_count', ascending=False)
    
    # 2. 热门上车点
    pickup_hotspots = df.groupby('PULocationID').agg({
        'total_amount': 'count',
        'trip_distance': 'mean'
    }).reset_index()
    pickup_hotspots.columns = ['PULocationID', 'pickup_count', 'avg_distance']
    pickup_hotspots = pickup_hotspots.sort_values('pickup_count', ascending=False)
    
    # 3. 按小时分析
    df['hour'] = pd.to_datetime(df['tpep_pickup_datetime']).dt.hour
    hourly_traffic = df.groupby('hour').agg({
        'total_amount': 'count',
        'trip_distance': 'mean'
    }).reset_index()
    hourly_traffic.columns = ['hour', 'trip_count', 'avg_distance']
    
    # 保存结果
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    hot_routes.to_csv(output_dir / "hot_routes.csv", index=False)
    pickup_hotspots.to_csv(output_dir / "pickup_hotspots.csv", index=False)
    hourly_traffic.to_csv(output_dir / "hourly_traffic.csv", index=False)
    
    print(f"分析结果已保存到: {output_dir}")
    print(f"热门路线Top 5:")
    print(hot_routes.head())
    
    return hot_routes, pickup_hotspots, hourly_traffic

if __name__ == "__main__":
    analyze_data()
