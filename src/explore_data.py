import pandas as pd
import pyarrow.parquet as pq

# 查看Parquet文件
df = pd.read_parquet('yellow_tripdata_2023-01.parquet', engine='pyarrow')
print(f"数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")
print(df.head())

# 查看关键字段统计
print(f"时间范围: {df['tpep_pickup_datetime'].min()} 到 {df['tpep_pickup_datetime'].max()}")
print(f"经纬度范围: PULocationID: {df['PULocationID'].min()}-{df['PULocationID'].max()}")
print(f"费用统计: 平均${df['total_amount'].mean():.2f}, 最大${df['total_amount'].max():.2f}")