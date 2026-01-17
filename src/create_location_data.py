# create_location_data.py
"""
创建位置数据预处理脚本
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
current_file = Path(__file__).resolve()
project_root = current_file.parent
sys.path.append(str(project_root))

from location_utils import LocationDataManager

def main():
    print("=" * 60)
    print("NYC Taxi 位置数据预处理工具")
    print("=" * 60)
    
    # 创建位置数据管理器
    manager = LocationDataManager(project_root)
    
    # 1. 加载区域数据
    print("\n1. 加载区域数据...")
    zones_df = manager.load_taxi_zones()
    
    if zones_df is not None and not zones_df.empty:
        print(f"✓ 成功加载区域数据")
        print(f"  行数: {len(zones_df)}")
        print(f"  列名: {', '.join(zones_df.columns.tolist())}")
        print(f"  行政区分布:")
        if 'borough' in zones_df.columns:
            borough_counts = zones_df['borough'].value_counts()
            for borough, count in borough_counts.items():
                print(f"    {borough}: {count} 个区域")
    else:
        print("✗ 加载区域数据失败")
        return
    
    # 2. 创建位置映射
    print("\n2. 创建位置映射...")
    mapping_path = manager.create_location_mapping()
    
    if mapping_path:
        print(f"✓ 位置映射已创建: {mapping_path}")
        
        # 显示映射统计
        import json
        with open(mapping_path, 'r') as f:
            mapping = json.load(f)
        
        print(f"  包含 {len(mapping)} 个区域")
        
        # 显示前10个区域
        print("\n  前10个区域示例:")
        for i, (zone_id, info) in enumerate(list(mapping.items())[:10]):
            print(f"    {zone_id}: {info.get('zone', 'Unknown')} ({info.get('borough', 'Unknown')})")
    else:
        print("✗ 创建位置映射失败")
    
    print("\n" + "=" * 60)
    print("位置数据预处理完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()