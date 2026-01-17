# create_unified_output.py
import pandas as pd
import json
from pathlib import Path
import shutil

def create_unified_output():
    """创建统一的输出结构供app.py使用"""
    project_root = Path(__file__).parent
    
    # 目标统一目录
    unified_dir = project_root / "output" / "unified"
    unified_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔍 搜索分析结果...")
    
    # 搜索所有可能的输出
    found_data = []
    
    for subdir in ["pandas", "spark_simple", "spark_advanced"]:
        source_dir = project_root / "output" / subdir
        if source_dir.exists():
            csv_files = list(source_dir.glob("*.csv"))
            if csv_files:
                found_data.append({
                    "dir": subdir,
                    "csv_count": len(csv_files),
                    "files": csv_files
                })
                print(f"  ✓ 找到 {subdir}: {len(csv_files)} 个CSV文件")
    
    if not found_data:
        print("❌ 未找到任何分析结果")
        return False
    
    # 选择数据最多的源
    found_data.sort(key=lambda x: x["csv_count"], reverse=True)
    source_info = found_data[0]
    source_dir = project_root / "output" / source_info["dir"]
    
    print(f"📂 使用 {source_info['dir']} 作为数据源")
    
    # 复制/重命名CSV文件到统一目录
    for csv_file in source_info["files"]:
        dest_file = unified_dir / csv_file.name
        shutil.copy2(csv_file, dest_file)
        print(f"  📄 复制: {csv_file.name}")
    
    # 创建统一的报告文件
    report_data = {
        "source": source_info["dir"],
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_count": len(source_info["files"]),
        "files": [f.name for f in source_info["files"]]
    }
    
    # 保存为JSON
    report_path = unified_dir / "analysis_report.json"
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"📝 创建报告: {report_path}")
    
    # 也创建文本报告
    txt_report = f"""数据分析报告
==============

数据源: {source_info['dir']}
生成时间: {report_data['timestamp']}
文件数量: {len(source_info['files'])}

文件列表:
"""
    for i, file_name in enumerate(report_data["files"], 1):
        file_path = source_dir / file_name
        if file_path.exists():
            file_size = file_path.stat().st_size / 1024  # KB
            txt_report += f"{i}. {file_name} ({file_size:.1f} KB)\n"
    
    txt_report_path = unified_dir / "report.txt"
    with open(txt_report_path, 'w') as f:
        f.write(txt_report)
    
    print(f"📝 创建文本报告: {txt_report_path}")
    
    # 显示文件统计
    print("\n📊 统一输出统计:")
    for file in unified_dir.iterdir():
        if file.is_file():
            size_kb = file.stat().st_size / 1024
            print(f"  {file.name:30} {size_kb:6.1f} KB")
    
    print(f"\n✅ 统一输出创建完成: {unified_dir}")
    return True

if __name__ == "__main__":
    create_unified_output()