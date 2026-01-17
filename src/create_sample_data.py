import pandas as pd
import numpy as np
from datetime import datetime

# 创建示例出租车数据
np.random.seed(42)

n_records = 1000
dates = pd.date_range('2023-01-01', periods=30, freq='D')

data = {
    'tpep_pickup_datetime': np.random.choice(dates, n_records),
    'PULocationID': np.random.randint(1, 264, n_records),
    'DOLocationID': np.random.randint(1, 264, n_records),
    'trip_distance': np.random.uniform(0.5, 20, n_records),
    'total_amount': np.random.uniform(5, 100, n_records),
    'tip_amount': np.random.uniform(0, 20, n_records),
    'passenger_count': np.random.randint(1, 6, n_records)
}

df = pd.DataFrame(data)
df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'] + pd.to_timedelta(np.random.randint(0, 86400, n_records), unit='s')
df['tpep_dropoff_datetime'] = df['tpep_pickup_datetime'] + pd.to_timedelta(df['trip_distance'] * 300, unit='s')

# 保存为CSV和Parquet
data_dir = "data/raw"
df.to_csv(f"{data_dir}/sample_taxi_data.csv", index=False)
df.to_parquet(f"{data_dir}/sample_taxi_data.parquet", index=False)

print(f"已创建示例数据: {data_dir}/sample_taxi_data.csv")
print(f"数据形状: {df.shape}")
