"""
高级Spark处理器 - 基于你NLP项目的经验
"""
import sys
import time
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.path_utils import get_data_path, get_project_root
import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans

class AdvancedNYCDataProcessor:
    def __init__(self, app_name="NYCTaxiAdvancedProcessor", master="local[*]"):
        """初始化Spark会话 - 借鉴你NLP项目的配置"""
        self.start_time = time.time()
        self.project_root = get_project_root()
        self.output_dir = self.project_root / "output" / "spark_advanced"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建Spark会话（使用你熟悉的配置方式）
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .master(master) \
            .config("spark.executor.memory", "2g") \
            .config("spark.driver.memory", "2g") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.sql.repl.eagerEval.enabled", "true") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.ui.port", "4040") \
            .config("spark.logConf", "true") \
            .getOrCreate()
        
        # 设置日志级别
        self.spark.sparkContext.setLogLevel("WARN")
        print(f"✅ Spark会话已创建: {app_name}")
        
    def load_and_validate_data(self, file_pattern="*.parquet"):
        """加载并验证数据"""
        print("📂 加载数据...")
        
        data_dir = self.project_root / "data" / "raw"
        
        # 查找所有数据文件
        data_files = list(data_dir.glob(file_pattern))
        
        if not data_files:
            # 如果没有找到数据文件，创建示例数据
            print("⚠️  未找到数据文件，创建示例数据...")
            df = self._create_sample_spark_data()
            # 保存为Parquet
            sample_path = data_dir / "yellow_tripdata_sample.parquet"
            df.write.parquet(str(sample_path), mode="overwrite")
            return df
        else:
            # 加载第一个文件（或多个文件）
            file_path = data_files[0]
            print(f"📄 加载文件: {file_path.name}")
            
            if file_path.suffix.lower() == '.parquet':
                df = self.spark.read.parquet(str(file_path))
            elif file_path.suffix.lower() == '.csv':
                df = self.spark.read.csv(str(file_path), header=True, inferSchema=True)
            else:
                raise ValueError(f"不支持的文件格式: {file_path.suffix}")
        
        # 数据验证
        print("🔍 数据验证...")
        print(f"  数据形状: {df.count():,} 行 × {len(df.columns)} 列")
        print(f"  列名: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}")
        df.printSchema()
        
        # 显示数据样本
        print("📋 数据样本:")
        df.show(5, truncate=False)
        
        return df
    
    def _create_sample_spark_data(self, n_rows=10000):
        """创建Spark示例数据（当没有真实数据时）"""
        print("🎲 创建Spark示例数据...")
        
        from pyspark.sql.types import StructType, StructField
        from pyspark.sql.types import IntegerType, DoubleType, TimestampType, StringType
        
        schema = StructType([
            StructField("VendorID", IntegerType(), True),
            StructField("tpep_pickup_datetime", TimestampType(), True),
            StructField("tpep_dropoff_datetime", TimestampType(), True),
            StructField("passenger_count", IntegerType(), True),
            StructField("trip_distance", DoubleType(), True),
            StructField("PULocationID", IntegerType(), True),
            StructField("DOLocationID", IntegerType(), True),
            StructField("RatecodeID", IntegerType(), True),
            StructField("store_and_fwd_flag", StringType(), True),
            StructField("payment_type", IntegerType(), True),
            StructField("fare_amount", DoubleType(), True),
            StructField("extra", DoubleType(), True),
            StructField("mta_tax", DoubleType(), True),
            StructField("tip_amount", DoubleType(), True),
            StructField("tolls_amount", DoubleType(), True),
            StructField("improvement_surcharge", DoubleType(), True),
            StructField("total_amount", DoubleType(), True),
            StructField("congestion_surcharge", DoubleType(), True),
        ])
        
        # 创建示例数据
        np.random.seed(42)
        
        # 生成数据
        data = []
        base_time = datetime(2023, 1, 1)
        
        for i in range(n_rows):
            pickup_time = base_time + pd.Timedelta(minutes=np.random.randint(0, 30*24*60))
            dropoff_time = pickup_time + pd.Timedelta(minutes=np.random.randint(5, 60))
            
            trip_distance = np.random.exponential(3)  # 大多数行程较短
            if trip_distance > 50:  # 限制异常值
                trip_distance = 50
                
            fare_amount = 2.5 + trip_distance * 2.5 + np.random.randn() * 3
            if fare_amount < 2.5:
                fare_amount = 2.5
                
            tip_amount = fare_amount * np.random.choice([0, 0.1, 0.15, 0.2], p=[0.2, 0.3, 0.4, 0.1])
            
            row = (
                1,  # VendorID
                pickup_time,  # tpep_pickup_datetime
                dropoff_time,  # tpep_dropoff_datetime
                np.random.randint(1, 6),  # passenger_count
                round(trip_distance, 2),  # trip_distance
                np.random.randint(1, 264),  # PULocationID
                np.random.randint(1, 264),  # DOLocationID
                np.random.choice([1, 2, 3, 4, 5, 6]),  # RatecodeID
                "N",  # store_and_fwd_flag
                np.random.choice([1, 2, 3, 4, 5, 6]),  # payment_type
                round(fare_amount, 2),  # fare_amount
                round(np.random.choice([0, 0.5, 1.0]), 2),  # extra
                0.5,  # mta_tax
                round(tip_amount, 2),  # tip_amount
                round(np.random.choice([0, 1.25, 4.5, 5.76]), 2),  # tolls_amount
                0.3,  # improvement_surcharge
                round(fare_amount + tip_amount + 0.5 + 0.3, 2),  # total_amount
                round(np.random.choice([0, 2.5]), 2),  # congestion_surcharge
            )
            data.append(row)
        
        df = self.spark.createDataFrame(data, schema=schema)
        print(f"✅ 已创建 {n_rows:,} 行示例数据")
        return df
    
    def preprocess_data(self, df):
        """数据预处理"""
        print("🧹 数据预处理...")
        
        initial_count = df.count()
        
        # 1. 基本清洗
        df_clean = df.filter(
            (col("PULocationID").isNotNull()) &
            (col("DOLocationID").isNotNull()) &
            (col("tpep_pickup_datetime").isNotNull()) &
            (col("tpep_dropoff_datetime").isNotNull()) &
            (col("total_amount") > 0) &
            (col("total_amount") < 1000) &
            (col("trip_distance") > 0) &
            (col("trip_distance") < 100) &
            (col("passenger_count") > 0) &
            (col("passenger_count") <= 6)
        )
        
        # 2. 添加时间特征
        df_clean = df_clean.withColumn("pickup_hour", hour(col("tpep_pickup_datetime"))) \
                          .withColumn("pickup_day", dayofmonth(col("tpep_pickup_datetime"))) \
                          .withColumn("pickup_dayofweek", dayofweek(col("tpep_pickup_datetime"))) \
                          .withColumn("pickup_month", month(col("tpep_pickup_datetime"))) \
                          .withColumn("trip_duration_minutes", 
                                     (unix_timestamp(col("tpep_dropoff_datetime")) - 
                                      unix_timestamp(col("tpep_pickup_datetime"))) / 60)
        
        # 3. 计算衍生特征
        df_clean = df_clean.withColumn("speed_mph", 
                                      when(col("trip_duration_minutes") > 0,
                                           col("trip_distance") / (col("trip_duration_minutes") / 60))
                                      .otherwise(0))
        
        df_clean = df_clean.withColumn("tip_percentage",
                                      when(col("fare_amount") > 0,
                                           (col("tip_amount") / col("fare_amount")) * 100)
                                      .otherwise(0))
        
        # 4. 移除异常值
        df_clean = df_clean.filter(
            (col("trip_duration_minutes") > 0) &
            (col("trip_duration_minutes") < 180) &  # 3小时以内
            (col("speed_mph") < 100) &  # 合理速度
            (col("tip_percentage") < 100)  # 小费不超过车费
        )
        
        cleaned_count = df_clean.count()
        removed_percent = ((initial_count - cleaned_count) / initial_count * 100) if initial_count > 0 else 0
        
        print(f"  清洗前: {initial_count:,} 行")
        print(f"  清洗后: {cleaned_count:,} 行")
        print(f"  移除: {initial_count - cleaned_count:,} 行 ({removed_percent:.2f}%)")
        
        return df_clean
    
    def analyze_basic_metrics(self, df):
        """基础指标分析"""
        print("📊 基础指标分析...")
        
        # 1. 热门路线（前100）
        hot_routes = df.groupBy("PULocationID", "DOLocationID") \
                      .agg(
                          count("*").alias("trip_count"),
                          avg("trip_distance").alias("avg_distance"),
                          avg("total_amount").alias("avg_fare"),
                          avg("trip_duration_minutes").alias("avg_duration"),
                          avg("tip_amount").alias("avg_tip"),
                          stddev("total_amount").alias("fare_std")
                      ) \
                      .filter(col("trip_count") > 5) \
                      .orderBy(desc("trip_count")) \
                      .limit(100)
        
        # 2. 区域热度分析
        pickup_hotspots = df.groupBy("PULocationID") \
                           .agg(
                               count("*").alias("pickup_count"),
                               avg("total_amount").alias("avg_fare"),
                               avg("trip_distance").alias("avg_distance"),
                               avg("trip_duration_minutes").alias("avg_duration")
                           ) \
                           .orderBy(desc("pickup_count")) \
                           .limit(50)
        
        dropoff_hotspots = df.groupBy("DOLocationID") \
                            .agg(
                                count("*").alias("dropoff_count"),
                                avg("total_amount").alias("avg_fare")
                            ) \
                            .orderBy(desc("dropoff_count")) \
                            .limit(50)
        
        # 3. 时间分析
        hourly_traffic = df.groupBy("pickup_hour") \
                          .agg(
                              count("*").alias("trip_count"),
                              avg("total_amount").alias("avg_fare"),
                              avg("trip_distance").alias("avg_distance"),
                              avg("tip_percentage").alias("avg_tip_percentage")
                          ) \
                          .orderBy("pickup_hour")
        
        # 4. 星期分析
        daily_traffic = df.groupBy("pickup_dayofweek") \
                         .agg(
                             count("*").alias("trip_count"),
                             avg("total_amount").alias("avg_fare"),
                             avg("tip_amount").alias("avg_tip")
                         ) \
                         .orderBy("pickup_dayofweek")
        
        # 5. 乘客数量分析
        passenger_stats = df.groupBy("passenger_count") \
                           .agg(
                               count("*").alias("trip_count"),
                               avg("total_amount").alias("avg_fare"),
                               avg("trip_distance").alias("avg_distance")
                           ) \
                           .filter(col("passenger_count").isNotNull()) \
                           .orderBy("passenger_count")
        
        return {
            "hot_routes": hot_routes,
            "pickup_hotspots": pickup_hotspots,
            "dropoff_hotspots": dropoff_hotspots,
            "hourly_traffic": hourly_traffic,
            "daily_traffic": daily_traffic,
            "passenger_stats": passenger_stats
        }
    
    def analyze_advanced_metrics(self, df):
        """高级分析（聚类等）"""
        print("🔬 高级分析...")
        
        try:
            # 1. 费用聚类分析
            fare_features = df.select("trip_distance", "trip_duration_minutes", "total_amount")
            
            # 创建特征向量
            assembler = VectorAssembler(
                inputCols=["trip_distance", "trip_duration_minutes", "total_amount"],
                outputCol="features"
            )
            
            fare_features_vector = assembler.transform(fare_features).select("features")
            
            # 标准化
            scaler = StandardScaler(
                inputCol="features",
                outputCol="scaled_features",
                withStd=True,
                withMean=True
            )
            
            scaler_model = scaler.fit(fare_features_vector)
            scaled_data = scaler_model.transform(fare_features_vector)
            
            # KMeans聚类
            kmeans = KMeans(k=3, seed=42, featuresCol="scaled_features")
            kmeans_model = kmeans.fit(scaled_data)
            
            # 预测聚类
            clustered = kmeans_model.transform(scaled_data)
            
            # 将聚类结果添加回原始数据
            df_with_cluster = df.withColumn("row_idx", monotonically_increasing_id())
            clustered_with_idx = clustered.withColumn("row_idx", monotonically_increasing_id())
            
            df_clustered = df_with_cluster.join(clustered_with_idx.select("row_idx", "prediction"), 
                                               on="row_idx").drop("row_idx")
            
            # 聚类统计
            cluster_stats = df_clustered.groupBy("prediction") \
                                       .agg(
                                           count("*").alias("trip_count"),
                                           avg("trip_distance").alias("avg_distance"),
                                           avg("total_amount").alias("avg_fare"),
                                           avg("trip_duration_minutes").alias("avg_duration")
                                       ) \
                                       .orderBy("prediction")
            
            # 2. 计算行程效率指标
            efficiency_stats = df.withColumn("fare_per_mile", 
                                           col("total_amount") / col("trip_distance")) \
                                .filter(col("fare_per_mile") > 0) \
                                .groupBy("pickup_hour") \
                                .agg(
                                    avg("fare_per_mile").alias("avg_fare_per_mile"),
                                    avg("speed_mph").alias("avg_speed"),
                                    count("*").alias("trip_count")
                                ) \
                                .orderBy("pickup_hour")
            
            return {
                "cluster_stats": cluster_stats,
                "efficiency_stats": efficiency_stats,
                "df_clustered": df_clustered
            }
            
        except Exception as e:
            print(f"⚠️  高级分析失败: {e}")
            print("  使用基础分析代替...")
            return {}
    
    def save_results(self, basic_results, advanced_results=None):
        """保存分析结果"""
        print("💾 保存结果...")
        
        # 保存基础结果
        for name, df in basic_results.items():
            # 保存为Parquet
            parquet_path = self.output_dir / f"{name}.parquet"
            df.write.parquet(str(parquet_path), mode="overwrite")
            
            # 保存为CSV（用于Streamlit）
            csv_path = self.output_dir / f"{name}.csv"
            pandas_df = df.toPandas()
            pandas_df.to_csv(csv_path, index=False)
            
            print(f"  ✅ {name}: {len(pandas_df):,} 行 -> {csv_path}")
        
        # 保存高级分析结果
        if advanced_results:
            for name, df in advanced_results.items():
                if name == "df_clustered":
                    # 保存聚类数据（抽样）
                    sample_df = df.sample(0.1)  # 10%样本
                    csv_path = self.output_dir / f"{name}_sample.csv"
                    sample_df.toPandas().to_csv(csv_path, index=False)
                    print(f"  ✅ {name}_sample: {sample_df.count():,} 行")
                elif isinstance(df, pd.DataFrame):
                    csv_path = self.output_dir / f"{name}.csv"
                    df.to_csv(csv_path, index=False)
                else:
                    csv_path = self.output_dir / f"{name}.csv"
                    df.toPandas().to_csv(csv_path, index=False)
        
        # 生成汇总报告
        self._generate_summary_report(basic_results)
    
    def _generate_summary_report(self, results):
        """生成汇总报告"""
        print("📝 生成汇总报告...")
        
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processing_time_seconds": round(time.time() - self.start_time, 2),
            "datasets": {}
        }
        
        for name, df in results.items():
            count = df.count()
            report["datasets"][name] = {
                "row_count": count,
                "column_count": len(df.columns),
                "sample_data": df.limit(3).toPandas().to_dict(orient="records") if count > 0 else []
            }
        
        # 保存报告为JSON
        import json
        report_path = self.output_dir / "analysis_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"  ✅ 报告已保存: {report_path}")
        
        # 打印关键指标
        print("\n📈 关键指标:")
        if "hot_routes" in results:
            top_routes = results["hot_routes"].limit(3).toPandas()
            print(f"  最热门路线: {top_routes.iloc[0]['PULocationID']} -> {top_routes.iloc[0]['DOLocationID']} "
                  f"({top_routes.iloc[0]['trip_count']} 次行程)")
        
        if "hourly_traffic" in results:
            peak_hour = results["hourly_traffic"].orderBy(desc("trip_count")).first()
            if peak_hour:
                print(f"  高峰时段: {int(peak_hour['pickup_hour'])}:00 "
                      f"({peak_hour['trip_count']} 次行程)")
    
    def run(self, use_advanced=True):
        """运行完整流程"""
        print("=" * 60)
        print("🚀 NYC Taxi 高级数据分析流程")
        print("=" * 60)
        
        try:
            # 1. 加载数据
            df_raw = self.load_and_validate_data()
            
            # 2. 数据预处理
            df_clean = self.preprocess_data(df_raw)
            
            # 3. 基础分析
            basic_results = self.analyze_basic_metrics(df_clean)
            
            # 4. 高级分析（可选）
            advanced_results = None
            if use_advanced:
                advanced_results = self.analyze_advanced_metrics(df_clean)
            
            # 5. 保存结果
            self.save_results(basic_results, advanced_results)
            
            # 6. 显示执行时间
            total_time = time.time() - self.start_time
            print(f"\n✅ 分析完成！总耗时: {total_time:.2f} 秒")
            print(f"📁 结果保存在: {self.output_dir}")
            
            return basic_results, advanced_results
            
        except Exception as e:
            print(f"❌ 处理过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            return None, None
        
        finally:
            # 清理资源
            self.spark.stop()
            print("🔄 Spark会话已关闭")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NYC Taxi 高级数据分析")
    parser.add_argument("--simple", action="store_true", help="使用简单模式（跳过高级分析）")
    parser.add_argument("--sample", action="store_true", help="使用样本数据")
    
    args = parser.parse_args()
    
    # 运行处理器
    processor = AdvancedNYCDataProcessor()
    
    # 根据参数决定是否使用高级分析
    use_advanced = not args.simple
    
    print(f"使用{'高级' if use_advanced else '基础'}分析模式")
    
    processor.run(use_advanced=use_advanced)

if __name__ == "__main__":
    main()