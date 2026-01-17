"""
云端Spark处理器 - 在GCP Dataproc上运行
"""
import sys
from pathlib import Path
import argparse

# 添加项目根目录到Python路径
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))

def process_on_gcp(input_path, output_path):
    """在GCP上处理数据"""
    print(f"🚀 开始GCP数据处理...")
    print(f"输入路径: {input_path}")
    print(f"输出路径: {output_path}")
    
    try:
        # 这里可以添加需要在Dataproc上运行的Spark代码
        # 由于这是要在集群上运行的，代码需要独立
        
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import *
        
        # 创建Spark会话
        spark = SparkSession.builder \
            .appName("NYCTaxiGCPProcessor") \
            .getOrCreate()
        
        # 从GCS读取数据
        print(f"从GCS读取数据: {input_path}")
        df = spark.read.parquet(input_path)
        
        print(f"数据加载完成: {df.count():,} 行")
        
        # 数据清洗
        df_clean = df.filter(
            (col("PULocationID").isNotNull()) &
            (col("DOLocationID").isNotNull()) &
            (col("total_amount") > 0) &
            (col("total_amount") < 1000)
        )
        
        # 热门路线分析
        hot_routes = df_clean.groupBy("PULocationID", "DOLocationID") \
                           .agg(
                               count("*").alias("trip_count"),
                               avg("trip_distance").alias("avg_distance"),
                               avg("total_amount").alias("avg_fare"),
                               avg("tip_amount").alias("avg_tip")
                           ) \
                           .orderBy(desc("trip_count")) \
                           .limit(1000)
        
        # 保存结果到GCS
        print(f"保存结果到GCS: {output_path}")
        hot_routes.write \
            .mode("overwrite") \
            .parquet(output_path)
        
        print(f"✅ GCP数据处理完成")
        print(f"结果行数: {hot_routes.count():,}")
        
        # 显示示例结果
        print("\n📊 热门路线Top 5:")
        hot_routes.show(5, truncate=False)
        
        spark.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ GCP数据处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数 - 用于在Dataproc上运行"""
    parser = argparse.ArgumentParser(description="GCP Spark处理器")
    parser.add_argument("--input", required=True, help="输入数据路径 (GCS)")
    parser.add_argument("--output", required=True, help="输出数据路径 (GCS)")
    
    args = parser.parse_args()
    
    success = process_on_gcp(args.input, args.output)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()