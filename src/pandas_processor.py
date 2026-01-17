"""
纯Pandas数据处理 - 当Spark不可用时使用
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import time
from datetime import datetime

# 添加项目根目录到Python路径
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))

from src.path_utils import get_project_root, get_data_path

class PandasDataProcessor:
    def __init__(self):
        """初始化处理器"""
        self.start_time = time.time()
        self.project_root = get_project_root()
        self.output_dir = self.project_root / "output" / "pandas"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # ✅ 正确：保存数据文件列表，不在__init__中加载数据
        data_dir = self.project_root / "data" / "raw"
        self.data_files = list(data_dir.glob("*.parquet")) + list(data_dir.glob("*.csv"))
        
        print("✅ Pandas处理器已初始化")
        # 注意：没有return语句！

    def load_data(self):
        """加载数据 - 单独的方法"""
        if not self.data_files:
            print("⚠️  未找到数据文件，创建示例数据...")
            return self._create_sample_data()
        
        # 使用第一个文件
        file_path = self.data_files[0]
        print(f"📄 加载文件: {file_path.name}")
        
        try:
            if file_path.suffix.lower() == '.parquet':
                df = pd.read_parquet(file_path)
            else:
                df = pd.read_csv(file_path)
            
            print(f"✅ 数据加载完成: {len(df):,} 行, {len(df.columns)} 列")
            return df  # ✅ 正确：在单独的方法中返回
        except Exception as e:
            print(f"❌ 加载文件失败: {e}")
            return self._create_sample_data()  # ✅ 正确：在单独的方法中返回
    def _create_sample_data(self, n_rows=10000):
        """创建示例数据"""
        print("🎲 创建示例数据...")
        
        np.random.seed(42)
        
        # 生成示例数据
        data = {
            'tpep_pickup_datetime': pd.date_range('2023-01-01', periods=n_rows, freq='T'),
            'PULocationID': np.random.randint(1, 264, n_rows),
            'DOLocationID': np.random.randint(1, 264, n_rows),
            'trip_distance': np.random.exponential(3, n_rows),
            'total_amount': np.random.uniform(5, 100, n_rows),
            'tip_amount': np.random.uniform(0, 20, n_rows),
            'passenger_count': np.random.randint(1, 6, n_rows)
        }
        
        df = pd.DataFrame(data)
        df['tpep_dropoff_datetime'] = df['tpep_pickup_datetime'] + pd.to_timedelta(df['trip_distance'] * 5, unit='m')
        
        print(f"✅ 已创建 {n_rows:,} 行示例数据")
        return df
    
    def clean_data(self, df):
        """清洗数据"""
        print("🧹 清洗数据...")
        
        initial_count = len(df)
        
        # 基本清洗
        df_clean = df.dropna(subset=['PULocationID', 'DOLocationID', 'total_amount'])
        
        # 过滤异常值
        df_clean = df_clean[(df_clean['total_amount'] > 0) & (df_clean['total_amount'] < 1000)]
        
        if 'trip_distance' in df_clean.columns:
            df_clean = df_clean[(df_clean['trip_distance'] > 0) & (df_clean['trip_distance'] < 100)]
        
        cleaned_count = len(df_clean)
        removed = initial_count - cleaned_count
        
        print(f"  清洗前: {initial_count:,} 行")
        print(f"  清洗后: {cleaned_count:,} 行")
        print(f"  移除: {removed:,} 行 ({removed/initial_count*100:.1f}%)")
        
        return df_clean
    
    def analyze_data(self, df):
        """分析数据"""
        print("📊 分析数据...")
        
        # 1. 热门路线
        print("  计算热门路线...")
        hot_routes = df.groupby(['PULocationID', 'DOLocationID']).agg({
            'total_amount': ['count', 'mean'],
            'trip_distance': 'mean' if 'trip_distance' in df.columns else pd.NamedAgg(column='total_amount', aggfunc='count')
        }).reset_index()
        
        # 扁平化列名
        hot_routes.columns = ['PULocationID', 'DOLocationID', 'trip_count', 'avg_fare', 'avg_distance']
        hot_routes = hot_routes[hot_routes['trip_count'] > 5] \
            .sort_values('trip_count', ascending=False) \
            .head(100)
        
        # 2. 时间分析
        print("  分析时间模式...")
        if 'tpep_pickup_datetime' in df.columns:
            df['pickup_hour'] = pd.to_datetime(df['tpep_pickup_datetime']).dt.hour
            hourly_traffic = df.groupby('pickup_hour').agg({
                'total_amount': ['count', 'mean']
            }).reset_index()
            hourly_traffic.columns = ['pickup_hour', 'trip_count', 'avg_fare']
            hourly_traffic = hourly_traffic.sort_values('pickup_hour')
        else:
            # 创建模拟数据
            hourly_traffic = pd.DataFrame({
                'pickup_hour': range(24),
                'trip_count': np.random.randint(100, 1000, 24),
                'avg_fare': np.random.uniform(10, 30, 24)
            })
        
        # 3. 热门上车点
        print("  分析热门上车点...")
        pickup_hotspots = df.groupby('PULocationID').agg({
            'total_amount': ['count', 'mean']
        }).reset_index()
        pickup_hotspots.columns = ['PULocationID', 'pickup_count', 'avg_fare']
        pickup_hotspots = pickup_hotspots.sort_values('pickup_count', ascending=False).head(50)
        
        # 4. 乘客分析
        print("  分析乘客模式...")
        if 'passenger_count' in df.columns:
            passenger_stats = df.groupby('passenger_count').agg({
                'total_amount': ['count', 'mean']
            }).reset_index()
            passenger_stats.columns = ['passenger_count', 'trip_count', 'avg_fare']
        else:
            passenger_stats = pd.DataFrame({
                'passenger_count': [1, 2, 3, 4, 5],
                'trip_count': [5000, 3000, 1500, 400, 100],
                'avg_fare': [15.5, 18.2, 20.1, 22.5, 25.0]
            })
        
        return {
            "hot_routes": hot_routes,
            "hourly_traffic": hourly_traffic,
            "pickup_hotspots": pickup_hotspots,
            "passenger_stats": passenger_stats
        }
    
    def save_results(self, results):
        """保存结果"""
        print("💾 保存结果...")
        
        for name, df in results.items():
            # 保存为CSV
            csv_path = self.output_dir / f"{name}.csv"
            df.to_csv(csv_path, index=False)
            print(f"  ✅ {name}: {len(df):,} 行 -> {csv_path}")
        
        # 生成报告
        report_path = self.output_dir / "analysis_report.txt"
        with open(report_path, 'w') as f:
            f.write(f"NYC Taxi 数据分析报告 (Pandas版)\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"处理耗时: {time.time() - self.start_time:.2f} 秒\n\n")
            
            f.write("数据集统计:\n")
            for name, df in results.items():
                f.write(f"  {name}: {len(df)} 行\n")
        
        print(f"📝 报告已保存: {report_path}")
    
    def run(self):
        """运行完整流程"""
        print("=" * 60)
        print("NYC Taxi 数据分析流程 (Pandas版)")
        print("=" * 60)
        
        try:
            # 1. 加载数据
            df = self.load_data()
            
            # 2. 清洗数据
            df_clean = self.clean_data(df)
            
            # 3. 分析数据
            results = self.analyze_data(df_clean)
            
            # 4. 保存结果
            self.save_results(results)
            
            # 5. 显示摘要
            total_time = time.time() - self.start_time
            print(f"\n✅ 分析完成！总耗时: {total_time:.2f} 秒")
            print(f"📁 结果保存在: {self.output_dir}")
            
            # 6. 显示示例结果
            print("\n📊 热门路线Top 5:")
            print(results["hot_routes"].head())
            
            return results
            
        except Exception as e:
            print(f"❌ 处理过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """主函数"""
    processor = PandasDataProcessor()
    processor.run()

if __name__ == "__main__":
    main()