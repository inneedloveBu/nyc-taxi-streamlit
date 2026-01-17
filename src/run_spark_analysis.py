#!/usr/bin/env python
"""
运行Spark分析的便捷脚本 - 更新为从src目录运行
"""
import subprocess
import sys
from pathlib import Path

# 添加项目根目录到Python路径
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))

def run_spark_analysis():
    """运行Spark分析"""
    print("🚀 开始Spark数据分析...")
    print("=" * 60)
    
    # 选项1：简单分析（快速）
    print("\n选项1: 简单分析 (快速)")
    print("选项2: 完整分析 (包含聚类分析)")
    
    choice = input("\n请选择分析模式 (1/2, 默认1): ").strip()
    
    if choice == "2":
        cmd = [sys.executable, "src/spark_advanced_processor.py"]
    else:
        cmd = [sys.executable, "src/spark_advanced_processor.py", "--simple"]
    
    try:
        # 运行Spark分析
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("⚠️  警告信息:", result.stderr)
        
        print("✅ Spark分析完成！")
        
        # 询问是否启动Streamlit应用
        launch_app = input("\n是否启动Streamlit应用? (y/n, 默认y): ").strip().lower()
        if launch_app != "n":
            print("启动Streamlit应用...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "src/app.py"])
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Spark分析失败: {e}")
        print(f"错误输出: {e.stderr}")
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    run_spark_analysis()