#!/usr/bin/env python
"""
测试Spark环境的脚本
"""
import sys
from pathlib import Path
import subprocess

# 添加项目根目录到Python路径
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))

def test_python_environment():
    """测试Python环境"""
    print("🔍 测试Python环境...")
    
    import platform
    version = platform.python_version()
    print(f"✅ Python版本: {version}")
    
    return version.startswith('3.')

def test_dependencies():
    """测试依赖包"""
    print("\n🔍 测试依赖包...")
    
    required_packages = ['pandas', 'numpy', 'streamlit', 'plotly']
    optional_packages = ['pyspark', 'findspark', 'pyarrow']
    
    all_ok = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            all_ok = False
    
    print("\n可选包:")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"⚠️  {package} 未安装（可选）")
    
    return all_ok

def test_java():
    """测试Java安装"""
    print("\n🔍 测试Java安装（Spark需要）...")
    
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True, check=True)
        print("✅ Java已安装:")
        print(result.stderr.split('\n')[0])  # 显示第一行
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Java未安装或未正确配置（Spark需要Java）")
        print("   可以在不安装Java的情况下使用Pandas模式")
        return False

def test_spark():
    """测试Spark"""
    print("\n🔍 测试Spark...")
    
    try:
        import findspark
        findspark.init()
        
        from pyspark.sql import SparkSession
        
        # 创建Spark会话
        spark = SparkSession.builder \
            .appName("SparkTest") \
            .master("local[*]") \
            .getOrCreate()
        
        print("✅ Spark会话创建成功")
        
        # 测试基本功能
        data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
        df = spark.createDataFrame(data, ["Name", "Value"])
        
        print(f"✅ DataFrame创建成功: {df.count()} 行")
        df.show()
        
        spark.stop()
        print("✅ Spark会话已关闭")
        
        return True
    except ImportError:
        print("⚠️  PySpark未安装，将使用Pandas模式")
        return False
    except Exception as e:
        print(f"❌ Spark测试失败: {e}")
        return False

def test_path_utils():
    """测试路径工具"""
    print("\n🔍 测试路径工具...")
    
    try:
        from src.path_utils import get_project_root, get_data_path
        
        project_root = get_project_root()
        data_path = get_data_path()
        
        print(f"✅ 项目根目录: {project_root}")
        print(f"✅ 数据目录: {data_path}")
        
        # 检查目录是否存在
        if project_root.exists():
            print("✅ 项目目录存在")
        else:
            print("❌ 项目目录不存在")
            
        return True
    except Exception as e:
        print(f"❌ 路径工具测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("NYC Taxi 项目环境测试")
    print("=" * 60)
    
    tests = [
        ("Python环境", test_python_environment),
        ("依赖包", test_dependencies),
        ("Java", test_java),
        ("路径工具", test_path_utils),
        ("Spark", test_spark)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("测试汇总:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:15} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！环境配置正确。")
    else:
        print("⚠️  部分测试失败，但项目仍可运行（使用Pandas模式）。")
    
    print("\n下一步:")
    print("1. 运行分析: python run_analysis.py")
    print("2. 启动应用: python run_app.py")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)