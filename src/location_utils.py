"""
位置数据处理工具
"""
import pandas as pd
import numpy as np
from pathlib import Path
import json
import sys
import zipfile
# from path_utils import get_data_path, get_project_root



# 修复导入路径问题
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent  # src的父目录是项目根目录
sys.path.insert(0, str(project_root))

# 使用相对导入（.表示同一目录）
try:
    # 先尝试相对导入（当作为模块运行时）
    from .path_utils import get_data_path, get_project_root
    print("[DEBUG] 使用相对导入成功")
except ImportError:
    # 如果失败，使用绝对导入（当直接运行时）
    try:
        from src.path_utils import get_data_path, get_project_root
        print("[DEBUG] 使用绝对导入成功")
    except ImportError as e:
        print(f"[DEBUG] 导入失败: {e}")
        # 定义后备函数
        def get_project_root():
            return project_root
        
        def get_data_path():
            return project_root / "data" / "raw"  # 根据你的结构

class LocationDataManager:
    def __init__(self, data_path=None):
        """初始化位置数据管理器 - 只做初始化，不加载数据"""
        # 1. 设置数据目录
        self.data_dir = Path(data_path) if data_path else Path(get_data_path())
        
        # 2. 设置项目根目录
        self.project_root = Path(get_project_root())
        
        # ✅ 正确：__init__只做初始化，没有数据处理逻辑，没有return语句
        print(f"[DEBUG] LocationDataManager初始化完成: data_dir={self.data_dir}, project_root={self.project_root}")
    
    def load_taxi_zones(self):
        """加载出租车区域数据 - 从processed目录加载"""
        print(f"[DEBUG] load_taxi_zones 开始，数据目录: {self.data_dir}")
        
        # 文件优先级：先检查processed目录中的文件
        processed_files = [
            self.data_dir / "taxi_zones_processed.csv",      # 首选：已处理的文件
            self.data_dir / "taxi_zones_simplified.csv",
            self.data_dir / "taxi_zones.csv",
            self.data_dir / "taxi_zone_lookup.csv",
        ]
        
        for file_path in processed_files:
            print(f"[DEBUG] 检查文件: {file_path}")
            if file_path.exists():
                print(f"[DEBUG] ✓ 找到文件: {file_path}")
                try:
                    zones_df = pd.read_csv(file_path)
                    print(f"[DEBUG] 文件加载成功，形状: {zones_df.shape}")
                    
                    # 基本验证
                    if isinstance(zones_df, pd.Series):
                        zones_df = zones_df.to_frame()
                    
                    if zones_df.empty:
                        print(f"[DEBUG] 文件为空，继续查找")
                        continue
                    
                    # 标准化列名
                    zones_df.columns = zones_df.columns.str.lower()
                    
                    # 确保有必要的列
                    required_cols = ['location_id', 'latitude', 'longitude']
                    for col in required_cols:
                        if col not in zones_df.columns:
                            print(f"[DEBUG] 缺少列 '{col}'，使用模拟数据代替")
                            return self._create_simulated_zones()
                    
                    print(f"[DEBUG] 区域数据加载完成: {len(zones_df)} 个区域")
                    return zones_df
                    
                except Exception as e:
                    print(f"[DEBUG] 加载失败: {e}")
                    continue
        
        # 如果processed目录没有，回退到检查raw目录
        raw_dir = self.project_root / "data" / "raw"
        raw_files = [
            raw_dir / "taxi_zones_simplified.csv",
            raw_dir / "taxi_zones.csv",
            raw_dir / "taxi_zone_lookup.csv",
        ]
        
        for file_path in raw_files:
            if file_path.exists():
                print(f"[DEBUG] 在raw目录找到文件: {file_path}")
                try:
                    zones_df = pd.read_csv(file_path)
                    # 处理并保存到processed目录
                    zones_df = self._process_zones_data(zones_df)
                    processed_path = self.data_dir / "taxi_zones_processed.csv"
                    zones_df.to_csv(processed_path, index=False)
                    return zones_df
                except Exception as e:
                    print(f"[DEBUG] 处理raw文件失败: {e}")
                    continue
        
        # 最后的手段：创建模拟数据
        print("[DEBUG] 未找到任何区域数据文件，创建模拟数据...")
        return self._create_simulated_zones()
    
    def _process_zones_data(self, zones_df):
        """处理区域数据（从原始文件中提取）"""
        print(f"[DEBUG] 处理区域数据，原始形状: {zones_df.shape}")
        
        # 确保是DataFrame
        if isinstance(zones_df, pd.Series):
            print(f"[DEBUG] 警告：数据是Series，转换为DataFrame")
            zones_df = zones_df.to_frame()
        
        # 标准化列名
        if not zones_df.empty:
            zones_df.columns = zones_df.columns.str.lower()
            
            # 重命名列
            column_mapping = {}
            for col in zones_df.columns:
                col_lower = col.lower()
                if 'location' in col_lower:
                    column_mapping[col] = 'location_id'
                elif 'borough' in col_lower:
                    column_mapping[col] = 'borough'
                elif 'zone' in col_lower and 'service' not in col_lower:
                    column_mapping[col] = 'zone_name'
                elif 'lat' in col_lower or 'latitude' in col_lower:
                    column_mapping[col] = 'latitude'
                elif 'lon' in col_lower or 'longitude' in col_lower:
                    column_mapping[col] = 'longitude'
            
            if column_mapping:
                zones_df.rename(columns=column_mapping, inplace=True)
                print(f"[DEBUG] 列重命名完成")
        
        # 确保有必要的列
        if 'location_id' not in zones_df.columns or zones_df.empty:
            zones_df['location_id'] = range(1, len(zones_df) + 1)
        
        if 'latitude' not in zones_df.columns or 'longitude' not in zones_df.columns:
            zones_df = self._add_simulated_coordinates(zones_df)
        
        # 只保留需要的列
        required_cols = ['location_id', 'borough', 'zone_name', 'latitude', 'longitude']
        available_cols = [col for col in required_cols if col in zones_df.columns]
        zones_df = zones_df[available_cols]
        
        print(f"[DEBUG] 处理完成，最终形状: {zones_df.shape}")
        return zones_df
    
    def _add_simulated_coordinates(self, zones_df):
        """为区域数据添加模拟坐标"""
        print("为区域数据添加模拟坐标...")
        
        np.random.seed(42)
        
        # 基于区域ID分配坐标
        latitudes = []
        longitudes = []
        
        for location_id in zones_df['location_id']:
            # 基于位置ID生成可重复的坐标
            np.random.seed(int(location_id))
            
            # 纽约市大致范围
            base_lat = 40.7128
            base_lon = -74.0060
            
            # 根据区域ID分布坐标
            lat = base_lat + (location_id % 100) * 0.001
            lon = base_lon + ((location_id // 100) % 100) * 0.001
            
            # 添加一些随机变化
            lat += np.random.randn() * 0.005
            lon += np.random.randn() * 0.005
            
            latitudes.append(lat)
            longitudes.append(lon)
        
        zones_df['latitude'] = latitudes
        zones_df['longitude'] = longitudes
        
        return zones_df
    
    def _create_simulated_zones(self):
        """创建模拟区域数据"""
        print("创建模拟区域数据...")
        
        np.random.seed(42)
        
        # 创建263个区域（NYC标准）
        n_zones = 263
        
        # 区域分布
        boroughs = ['Manhattan'] * 60 + ['Brooklyn'] * 60 + ['Queens'] * 60 + ['Bronx'] * 40 + ['Staten Island'] * 40 + ['EWR'] * 3
        boroughs = boroughs[:n_zones]
        
        # 基础坐标
        borough_coords = {
            'Manhattan': (40.7831, -73.9712),
            'Brooklyn': (40.6782, -73.9442),
            'Queens': (40.7282, -73.7949),
            'Bronx': (40.8448, -73.8648),
            'Staten Island': (40.5795, -74.1502),
            'EWR': (40.6895, -74.1745)
        }
        
        zones_data = []
        
        for i in range(1, n_zones + 1):
            borough = boroughs[i-1]
            base_lat, base_lon = borough_coords.get(borough, (40.7128, -74.0060))
            
            # 在区域内分布
            lat = base_lat + np.random.randn() * 0.03
            lon = base_lon + np.random.randn() * 0.03
            
            zones_data.append({
                'location_id': i,
                'borough': borough,
                'zone_name': f'Zone_{i}',
                'latitude': lat,
                'longitude': lon
            })
        
        zones_df = pd.DataFrame(zones_data)
        
        # 保存
        processed_path = self.data_dir / "taxi_zones_processed.csv"
        processed_path.parent.mkdir(exist_ok=True)
        zones_df.to_csv(processed_path, index=False)
        
        print(f"已创建模拟区域数据: {len(zones_df)} 个区域")
        
        # 确保返回的是DataFrame
        if isinstance(zones_df, pd.Series):
            zones_df = zones_df.to_frame()
            print("[DEBUG] _create_simulated_zones: 已将Series转换为DataFrame")
        
        print(f"[DEBUG] _create_simulated_zones 返回类型: {type(zones_df)}")
        return zones_df
    
    def get_zone_centroids(self):
        """获取区域中心点"""
        zones_df = self.load_taxi_zones()
        
        if zones_df is not None and 'latitude' in zones_df.columns and 'longitude' in zones_df.columns:
            centroids = {
                row['location_id']: {
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'borough': row.get('borough', 'Unknown'),
                    'zone_name': row.get('zone_name', f'Zone_{row["location_id"]}')
                }
                for _, row in zones_df.iterrows()
            }
            return centroids
        
        return None
    
    def create_location_mapping(self):
        """创建位置映射文件（用于Streamlit）"""
        zones_df = self.load_taxi_zones()
        
        if zones_df is None:
            print("[DEBUG] create_location_mapping: zones_df 为 None")
            return None
        
        # 双重检查：确保是DataFrame且有必要的列
        if isinstance(zones_df, pd.Series):
            print("[DEBUG] create_location_mapping: zones_df 是 Series，转换为 DataFrame")
            zones_df = zones_df.to_frame()
        
        # 检查必要的列
        required_cols = ['location_id', 'latitude', 'longitude']
        for col in required_cols:
            if col not in zones_df.columns:
                print(f"[DEBUG] create_location_mapping: 缺少列 '{col}'，尝试修复...")
                if col == 'location_id':
                    zones_df['location_id'] = range(1, len(zones_df) + 1)
                elif col == 'latitude':
                    zones_df['latitude'] = 40.7128
                elif col == 'longitude':
                    zones_df['longitude'] = -74.0060
        
        print(f"[DEBUG] create_location_mapping: zones_df 类型: {type(zones_df)}, 形状: {zones_df.shape}")
        print(f"[DEBUG] create_location_mapping: 列名: {list(zones_df.columns)}")
        
        # 创建简化映射
        mapping = {}
        for _, row in zones_df.iterrows():
            try:
                location_id = int(row['location_id'])
                mapping[location_id] = {
                    'lat': float(row['latitude']),
                    'lon': float(row['longitude']),
                    'borough': str(row.get('borough', 'Unknown')),
                    'zone': str(row.get('zone_name', f'Zone_{location_id}'))
                }
            except Exception as e:
                print(f"[DEBUG] create_location_mapping: 处理行时出错: {e}")
                continue
        
        # 保存为JSON
        mapping_path = self.data_dir / "location_mapping.json"
        mapping_path.parent.mkdir(exist_ok=True)
        
        with open(mapping_path, 'w') as f:
            json.dump(mapping, f, indent=2)
        
        print(f"[DEBUG] 位置映射已保存: {mapping_path}, 包含 {len(mapping)} 个区域")
        return mapping_path

    def _extract_zip_if_needed(self, zip_path):
        """如果需要，解压ZIP文件并返回CSV文件路径"""
        if not zip_path.exists():
            return None
        
        target_dir = zip_path.parent
        
        # 检查是否已解压
        zip_name = zip_path.stem  # 去掉.zip后缀
        possible_csv_files = [
            target_dir / f"{zip_name}.csv",
            target_dir / zip_name / f"{zip_name}.csv",
            target_dir / zip_name / "taxi_zones.csv",
            target_dir / "taxi_zones.csv"
        ]
        
        # 检查是否已有CSV文件
        for csv_file in possible_csv_files:
            if csv_file.exists():
                print(f"[DEBUG] 找到CSV文件: {csv_file}")
                return csv_file
        
        # 需要解压
        try:
            print(f"[DEBUG] 解压ZIP文件: {zip_path}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 查看ZIP内容
                file_list = zip_ref.namelist()
                print(f"[DEBUG] ZIP包含 {len(file_list)} 个文件: {file_list[:5]}...")
                
                # 解压到临时目录
                extract_dir = target_dir / "temp_extract"
                zip_ref.extractall(extract_dir)
                
                # 查找CSV文件
                csv_files = list(extract_dir.rglob("*.csv"))
                if csv_files:
                    # 移动第一个CSV文件到目标目录
                    csv_file = csv_files[0]
                    target_csv = target_dir / csv_file.name
                    csv_file.rename(target_csv)
                    print(f"[DEBUG] 已提取CSV文件: {target_csv}")
                    return target_csv
        except Exception as e:
            print(f"[DEBUG] 解压失败: {e}")
        
        return None

def main():
    """测试位置数据管理器"""
    manager = LocationDataManager()
    
    print("加载区域数据...")
    zones_df = manager.load_taxi_zones()
    
    if zones_df is not None:
        print(f"区域数据形状: {zones_df.shape}")
        print(f"列名: {zones_df.columns.tolist()}")
        print("\n前5行数据:")
        print(zones_df.head())
        
        print("\n创建位置映射...")
        mapping_path = manager.create_location_mapping()
        if mapping_path:
            print(f"✓ 位置映射文件: {mapping_path}")

if __name__ == "__main__":
    main()