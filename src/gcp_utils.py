"""
GCP工具函数
"""
import os
import yaml
from pathlib import Path
from google.cloud import storage, dataproc_v1, bigquery
from google.oauth2 import service_account

class GCPManager:
    def __init__(self, config_path=None):
        """初始化GCP管理器"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "gcp_config.yaml"
        
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            print(f"⚠️  配置文件不存在: {self.config_path}")
            print("创建默认配置文件...")
            self.create_default_config()
        
        # ✅ 正确：加载配置并保存为实例变量，不返回
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)  # 改为赋值给 self.config
        
        print(f"✅ GCP配置已加载: {self.config_path}")
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            'gcp': {
                'project_id': 'YOUR_PROJECT_ID',
                'region': 'us-central1',
                'zone': 'us-central1-a',
                'storage': {
                    'bucket_name': 'nyc-taxi-data-bucket',
                    'raw_data_path': 'raw/',
                    'processed_data_path': 'processed/'
                },
                'dataproc': {
                    'cluster_name': 'nyc-taxi-cluster',
                    'master_machine_type': 'n1-standard-4',
                    'worker_machine_type': 'n1-standard-4',
                    'num_workers': 2,
                    'image_version': '2.0-debian10'
                },
                'bigquery': {
                    'dataset_id': 'nyc_taxi_analysis',
                    'results_table': 'analysis_results'
                }
            }
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        print(f"✅ 默认配置文件已创建: {self.config_path}")
        print("请编辑此文件并填写你的GCP项目信息")
    
    def get_credentials(self):
        """获取GCP凭据"""
        # 从环境变量获取凭据文件路径
        creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if creds_path and Path(creds_path).exists():
            return service_account.Credentials.from_service_account_file(creds_path)
        else:
            print("⚠️  未找到GCP凭据文件")
            print("请设置 GOOGLE_APPLICATION_CREDENTIALS 环境变量")
            return None
    
    def upload_to_gcs(self, local_path, destination_path=None):
        """上传文件到Google Cloud Storage"""
        if not self.credentials:
            print("❌ 无有效凭据，无法上传到GCS")
            return None
        
        bucket_name = self.config['gcp']['storage']['bucket_name']
        
        try:
            storage_client = storage.Client(
                credentials=self.credentials,
                project=self.config['gcp']['project_id']
            )
            
            bucket = storage_client.bucket(bucket_name)
            
            # 如果bucket不存在，创建它
            if not bucket.exists():
                bucket = storage_client.create_bucket(bucket_name)
                print(f"✅ 创建Bucket: {bucket_name}")
            
            # 确定目标路径
            if destination_path is None:
                destination_path = f"raw/{Path(local_path).name}"
            
            # 上传文件
            blob = bucket.blob(destination_path)
            blob.upload_from_filename(str(local_path))
            
            print(f"✅ 文件已上传: gs://{bucket_name}/{destination_path}")
            return f"gs://{bucket_name}/{destination_path}"
            
        except Exception as e:
            print(f"❌ 上传到GCS失败: {e}")
            return None
    
    def create_dataproc_cluster(self):
        """创建Dataproc集群"""
        if not self.credentials:
            print("❌ 无有效凭据，无法创建Dataproc集群")
            return None
        
        try:
            # 初始化客户端
            cluster_client = dataproc_v1.ClusterControllerClient(
                client_options={
                    'api_endpoint': f"{self.config['gcp']['region']}-dataproc.googleapis.com:443"
                },
                credentials=self.credentials
            )
            
            # 集群配置
            cluster_config = {
                'project_id': self.config['gcp']['project_id'],
                'cluster_name': self.config['gcp']['dataproc']['cluster_name'],
                'config': {
                    'gce_cluster_config': {
                        'zone_uri': self.config['gcp']['zone'],
                        'metadata': {
                            'enable-oslogin': 'TRUE'
                        }
                    },
                    'master_config': {
                        'num_instances': 1,
                        'machine_type_uri': self.config['gcp']['dataproc']['master_machine_type'],
                        'disk_config': {
                            'boot_disk_size_gb': 500
                        }
                    },
                    'worker_config': {
                        'num_instances': self.config['gcp']['dataproc']['num_workers'],
                        'machine_type_uri': self.config['gcp']['dataproc']['worker_machine_type'],
                        'disk_config': {
                            'boot_disk_size_gb': 500
                        }
                    },
                    'software_config': {
                        'image_version': self.config['gcp']['dataproc']['image_version']
                    }
                }
            }
            
            # 创建集群
            operation = cluster_client.create_cluster(
                project_id=self.config['gcp']['project_id'],
                region=self.config['gcp']['region'],
                cluster=cluster_config
            )
            
            print("🚀 正在创建Dataproc集群...")
            result = operation.result()
            print(f"✅ Dataproc集群已创建: {result.cluster_name}")
            
            return result
            
        except Exception as e:
            print(f"❌ 创建Dataproc集群失败: {e}")
            return None
    
    def submit_spark_job(self, main_python_file, args=None):
        """提交Spark作业到Dataproc"""
        if not self.credentials:
            print("❌ 无有效凭据，无法提交Spark作业")
            return None
        
        try:
            job_client = dataproc_v1.JobControllerClient(
                client_options={
                    'api_endpoint': f"{self.config['gcp']['region']}-dataproc.googleapis.com:443"
                },
                credentials=self.credentials
            )
            
            # 作业配置
            job_config = {
                'placement': {
                    'cluster_name': self.config['gcp']['dataproc']['cluster_name']
                },
                'pyspark_job': {
                    'main_python_file_uri': main_python_file,
                    'args': args or []
                }
            }
            
            # 提交作业
            operation = job_client.submit_job(
                project_id=self.config['gcp']['project_id'],
                region=self.config['gcp']['region'],
                job=job_config
            )
            
            print("🚀 正在提交Spark作业...")
            result = operation.result()
            print(f"✅ Spark作业已提交: {result.job_uuid}")
            
            return result
            
        except Exception as e:
            print(f"❌ 提交Spark作业失败: {e}")
            return None

def main():
    """测试GCP功能"""
    print("🔧 测试GCP工具...")
    
    gcp = GCPManager()
    
    # 测试配置加载
    print(f"项目ID: {gcp.config['gcp']['project_id']}")
    print(f"区域: {gcp.config['gcp']['region']}")
    
    # 测试凭据
    if gcp.credentials:
        print("✅ GCP凭据有效")
    else:
        print("❌ 无有效凭据")

if __name__ == "__main__":
    main()