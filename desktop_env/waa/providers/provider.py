import docker
import logging
import os
import shutil
import time
import socket
import platform
import psutil # 需要 pip install psutil
import requests
from pathlib import Path
from filelock import FileLock

logger = logging.getLogger("desktopenv.providers.docker")
LOCK_TIMEOUT = 30

class WindowsDockerProvider:
    def __init__(self, 
                 image_name="windowsarena/winarena-v2:latest", 
                 vm_storage_path="./storage", 
                 vm_backup_path="./storage_backup",
                 ram_size="8G",
                 cpu_cores="4"):
        """
        Args:
            image_name: Docker 镜像名称
            vm_storage_path: 挂载到容器内的运行目录
            vm_backup_path: 干净的快照源目录
        """
        self.client = docker.from_env()
        self.image_name = image_name
        
        # 转换为绝对路径
        self.vm_storage_path = os.path.abspath(vm_storage_path)
        self.vm_backup_path = os.path.abspath(vm_backup_path)
        
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        
        # --- 端口状态 ---
        self.container = None
        self.server_port = None    # 映射到容器 5000 (Agent API)
        self.rdp_port = None       # 映射到容器 3389 (RDP)
        self.chromium_port = None  # 映射到容器 9222 (Chrome DevTools) <--- 新增
        
        # 锁文件路径
        temp_dir = Path(os.getenv('TEMP') if platform.system() == 'Windows' else '/tmp')
        self.lock_file = temp_dir / "win_docker_port.lck"

    def _get_used_ports(self):
        """
        获取当前系统所有被占用的端口 (参考 Linux Provider 实现)
        """
        # 1. 获取系统占用的端口
        system_ports = set(conn.laddr.port for conn in psutil.net_connections())
        
        # 2. 获取 Docker 容器映射占用的端口 (防止 Docker 自身未完全释放)
        docker_ports = set()
        try:
            for container in self.client.containers.list():
                ports = container.attrs['NetworkSettings']['Ports']
                if ports:
                    for port_mappings in ports.values():
                        if port_mappings:
                            docker_ports.update(int(p['HostPort']) for p in port_mappings)
        except Exception as e:
            logger.warning(f"Error checking docker ports: {e}")
        
        return system_ports | docker_ports

    def _get_available_port(self, start_port: int, exclude_ports: set = None) -> int:
        """
        寻找可用端口
        Args:
            start_port: 起始扫描端口
            exclude_ports: 本次分配中已经预选的端口 (避免分配重复)
        """
        if exclude_ports is None:
            exclude_ports = set()

        used_ports = self._get_used_ports()
        port = start_port
        
        # 扫描直到 65535
        while port < 65535:
            if port not in used_ports and port not in exclude_ports:
                return port
            port += 1
            
        raise RuntimeError(f"No free ports available starting from {start_port}")

    def _wait_for_server(self, timeout=180):
        """等待 Windows Agent (5000端口) 启动"""
        start_time = time.time()
        # 注意：这里使用动态分配的 server_port
        url = f"http://127.0.0.1:{self.server_port}/screenshot" 
        
        logger.info(f"Waiting for Windows Agent at {url}...")
        while time.time() - start_time < timeout:
            try:
                requests.get(url, timeout=2)
                logger.info("Windows Agent is ready!")
                return True
            except requests.exceptions.RequestException:
                time.sleep(2)
        
        raise TimeoutError("Windows Agent failed to start within timeout.")

    def start_emulator(self, headless=True):
        """
        启动 Docker 容器，动态分配 3 个端口
        """
        lock = FileLock(str(self.lock_file), timeout=LOCK_TIMEOUT)
        # 使用文件锁，防止多进程并行测试时端口冲突
        try:
            with lock:
                # 1. 动态申请端口
                self.server_port = self._get_available_port(5000)
                
                self.rdp_port = self._get_available_port(
                    3389, 
                    exclude_ports={self.server_port}
                )
                
                self.chromium_port = self._get_available_port(
                    9222, 
                    exclude_ports={self.server_port, self.rdp_port}
                )

                self.brower_port = self._get_available_port(
                    8006, 
                    exclude_ports={self.server_port, self.rdp_port, self.chromium_port}
                )

                logger.info(f"Allocated ports -> API: {self.server_port}, RDP: {self.rdp_port}, Chrome: {self.chromium_port}, Browser(?): {self.brower_port}")

                # 2. 准备 Docker 参数
                devices = []
                if os.path.exists("/dev/kvm"):
                    devices.append("/dev/kvm")
                
                # 添加外网代理
                environment = {
                    "RAM_SIZE": self.ram_size,
                    "CPU_CORES": self.cpu_cores,
                    "KVM": "Y" if devices else "N",
                    "HTTPS_PROXY": "http://10.1.8.5:23128",
                    "HTTP_PROXY": "http://10.1.8.5:23128",
                    "NO_PROXY": "127.0.0.1,localhost"
                }

                # 3. 启动容器
                logger.info(f"Starting container using storage: {self.vm_storage_path}")
                self.container = self.client.containers.run(
                    self.image_name,
                    detach=True,
                    remove=True, 
                    devices=devices,
                    cap_add=["NET_ADMIN"],
                    ports={
                        '5000/tcp': self.server_port,   # Agent API
                        '3389/tcp': self.rdp_port,      # RDP
                        '9222/tcp': self.chromium_port,  # Chrome DevTools <--- 关键映射
                        '8006/tcp': self.brower_port
                    },
                    volumes={
                        self.vm_storage_path: {'bind': '/storage', 'mode': 'rw'}
                    },
                    environment=environment,
                    extra_hosts={"host.docker.internal": "host-gateway"},
                    name=f"win_vm_{self.server_port}" # 给容器起个名字方便调试
                )
                
                # 4. 等待服务就绪
                self._wait_for_server()
                
        except Exception as e:
            logger.error(f"Failed to start container: {e}")
            # 如果启动失败，清理残留
            self.stop_emulator()
            raise e

    def stop_emulator(self):
        """停止并移除容器"""
        if self.container:
            try:
                logger.info("Stopping container...")
                self.container.stop(timeout=10)
            except Exception as e:
                logger.warning(f"Error stopping container: {e}")
            finally:
                self.container = None
                # 清空端口记录
                self.server_port = None
                self.rdp_port = None
                self.chromium_port = None

    def revert_to_snapshot(self):
        """
        回滚快照：停止 -> 替换文件 -> 启动
        """
        logger.info("Reverting snapshot...")
        self.stop_emulator()
        
        try:
            # 清理旧数据
            if os.path.exists(self.vm_storage_path):
                # 简单粗暴但有效：删除整个目录再重建
                shutil.rmtree(self.vm_storage_path, ignore_errors=True)
            
            # 从备份恢复
            if os.path.exists(self.vm_backup_path):
                shutil.copytree(self.vm_backup_path, self.vm_storage_path)
                logger.info("Snapshot files restored.")
            else:
                os.makedirs(self.vm_storage_path, exist_ok=True)
                logger.warning(f"Backup path {self.vm_backup_path} not found, initialized empty storage.")

        except Exception as e:
            logger.error(f"Snapshot revert failed: {e}")
            raise e

        self.start_emulator()

    def get_connection_info(self):
        """
        返回完整的连接信息给 DesktopEnv
        """
        if not all([self.server_port, self.rdp_port, self.chromium_port]):
            logger.warning("Ports are not fully allocated yet.")
            
        return {
            "ip": "127.0.0.1",
            "server_port": self.server_port,
            "rdp_port": self.rdp_port,
            "chromium_port": self.chromium_port,  # <--- 返回这个端口
            "browser_port": self.brower_port
        }