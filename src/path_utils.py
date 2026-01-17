import os
import sys
from pathlib import Path

def get_project_root():
    """获取项目根目录 - 更新为从src目录向上两级"""
    # 因为此文件在src目录中，向上两级到项目根目录
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    return project_root

# 示例修改，使其返回容器内基于 /app 的路径

def get_data_path():
    """获取数据目录 - 指向processed目录"""
    project_root = get_project_root()
    processed_path = project_root / "data" / "processed"
    
    # 确保目录存在
    processed_path.mkdir(parents=True, exist_ok=True)
    
    print(f"[DEBUG] get_data_path: 返回处理后的数据目录 {processed_path}")
    return processed_path
    
    # # 可能的路径列表（按优先级）
    # possible_paths = [
    #     project_root / "data",                     # 本地开发
    #     project_root / "data" / "processed",       # 本地处理后的数据
    #     Path("/app/data/processed"),               # Docker容器内路径
    #     Path("/app/data"),                         # Docker容器内根数据路径
    # ]
    
    # # 检查哪个路径存在
    # for path in possible_paths:
    #     if path.exists():
    #         print(f"[DEBUG] get_data_path: 使用路径 {path}")
    #         return path
    
    # # 如果都不存在，创建并返回本地数据目录
    # local_data_path = project_root / "data"
    # local_data_path.mkdir(parents=True, exist_ok=True)
    # print(f"[DEBUG] get_data_path: 创建并返回路径 {local_data_path}")
    # return local_data_path



def get_relative_path(from_file, to_path):
    """获取相对路径"""
    from_dir = Path(from_file).parent
    return (from_dir / to_path).resolve()

# 测试代码
if __name__ == "__main__":
    print(f"项目根目录: {get_project_root()}")
    print(f"数据目录: {get_data_path()}")