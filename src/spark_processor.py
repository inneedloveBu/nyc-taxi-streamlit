from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import sys

def create_spark_session(app_name="NYCTaxiProcessor"):
    """创建Spark会话 - 类似你NLP项目中的setup"""
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    return spark

def load_data(spark, file_path, file_type="parquet"):
    """加载数据"""
    if file_type == "parquet":
        df = spark.read.parquet(file_path)
    else:
        df = spark.read.csv(file_path, header=True, inferSchema=True)
    
    print(f"数据加载完成: {df.count()} 行")
    df.printSchema()
    return df

def clean_data(df):
    """数据清洗"""
    from pyspark.sql.functions import col
    
    # 1. 去除无效经纬度（借鉴你NLP项目的clean_data思路）
    df_clean = df.filter(
        (col("PULocationID").isNotNull()) &
        (col("DOLocationID").isNotNull()) &
        (col("tpep_pickup_datetime").isNotNull()) &
        (col("total_amount") > 0) &
        (col("total_amount") < 1000)  # 去除异常高费用
    )
    
    # 2. 添加时间特征
    df_clean = df_clean.withColumn("hour", hour(col("tpep_pickup_datetime"))) \
                      .withColumn("day_of_week", dayofweek(col("tpep_pickup_datetime"))) \
                      .withColumn("month", month(col("tpep_pickup_datetime")))
    
    return df_clean

def analyze_hot_routes(df):
    """分析热门路线 - 核心业务逻辑"""
    # 计算最热门的上车->下车路线组合
    hot_routes = df.groupBy("PULocationID", "DOLocationID") \
                   .agg(
                       count("*").alias("trip_count"),
                       avg("trip_distance").alias("avg_distance"),
                       avg("total_amount").alias("avg_fare"),
                       avg("tip_amount").alias("avg_tip")
                   ) \
                   .orderBy(desc("trip_count")) \
                   .limit(100)  # 取前100条最热门路线
    
    # 计算每个区域的热度
    pickup_hotspots = df.groupBy("PULocationID") \
                       .agg(count("*").alias("pickup_count")) \
                       .orderBy(desc("pickup_count"))
    
    dropoff_hotspots = df.groupBy("DOLocationID") \
                        .agg(count("*").alias("dropoff_count")) \
                        .orderBy(desc("dropoff_count"))
    
    # 按时间分析
    hourly_traffic = df.groupBy("hour") \
                      .agg(count("*").alias("trip_count")) \
                      .orderBy("hour")
    
    return hot_routes, pickup_hotspots, dropoff_hotspots, hourly_traffic

def save_results(df_list, output_dir="./output"):
    """保存结果"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    names = ["hot_routes", "pickup_hotspots", "dropoff_hotspots", "hourly_traffic"]
    
    for df, name in zip(df_list, names):
        # 保存为Parquet（Spark原生格式）
        df.write.parquet(f"{output_dir}/{name}.parquet", mode="overwrite")
        
        # 同时保存为CSV用于Streamlit预览
        df.toPandas().to_csv(f"{output_dir}/{name}.csv", index=False)
        print(f"已保存: {name}.parquet 和 {name}.csv")

def main():
    spark = create_spark_session()
    
    # 使用小样本数据测试
    print("开始处理数据...")
    df = load_data(spark, "data/yellow_tripdata_2023-01.parquet", "parquet")
    
    print("清洗数据...")
    df_clean = clean_data(df)
    print(f"清洗后数据: {df_clean.count()} 行")
    
    print("分析热门路线...")
    results = analyze_hot_routes(df_clean)
    
    print("保存结果...")
    save_results(results)
    
    # 预览结果
    print("\n=== 热门路线Top 10 ===")
    results[0].show(10)
    
    print("\n=== 热门上车点Top 10 ===")
    results[1].show(10)
    
    spark.stop()
    print("处理完成！")

if __name__ == "__main__":
    main()
    