import os
import platform
import re
import sys
import time
from datetime import datetime

import psutil
from flask import Blueprint, render_template, jsonify

from applications.common.utils.rights import authorize

bp = Blueprint('adminMonitor', __name__, url_prefix='/monitor')


# 系统监控
@bp.get('/')
@authorize("system:monitor:main")
def main():
    # 主机名称
    hostname = platform.node()
    # 系统版本
    system_version = platform.platform()
    # python版本
    python_version = platform.python_version()
    # 逻辑cpu数量
    cpu_count = psutil.cpu_count()
    # cpu使用率
    cpus_percent = psutil.cpu_percent(interval=0.1, percpu=False)  # percpu 获取主使用率
    # 内存
    memory_information = psutil.virtual_memory()
    # 内存使用率
    memory_usage = memory_information.percent
    memory_used: int = memory_information.used
    memory_total: int = memory_information.total
    memory_free: int = memory_information.free
    # 磁盘信息

    disk_partitions_list = []
    # 判断是否在容器中
    if not os.path.exists('/.dockerenv'):
        disk_partitions = psutil.disk_partitions()
        for i in disk_partitions:
            try:
                # 在Windows上使用mountpoint，Linux/Mac上使用device
                # mountpoint更可靠，因为它指向实际可访问的路径
                disk_path = getattr(i, 'mountpoint', None) or i.device
                
                # 验证路径是否有效（Windows上检查是否为有效驱动器）
                if platform.system() == 'Windows':
                    # Windows上只处理有效的驱动器路径（如 C:\）
                    if not disk_path or len(disk_path) < 2 or disk_path[1] != ':':
                        continue
                    # 确保路径存在且可访问
                    if not os.path.exists(disk_path):
                        continue
                
                a = psutil.disk_usage(disk_path)
                disk_partitions_dict = {
                    'device': i.device,
                    'mountpoint': getattr(i, 'mountpoint', i.device),
                    'fstype': i.fstype,
                    'total': a.total,
                    'used': a.used,
                    'free': a.free,
                    'percent': a.percent
                }
                disk_partitions_list.append(disk_partitions_dict)
            except (OSError, PermissionError, SystemError, ValueError) as e:
                # 跳过无法访问的设备（如CD-ROM、网络驱动器、无效路径等）
                continue

    # 开机时间
    boot_time = datetime.fromtimestamp(psutil.boot_time()).replace(microsecond=0)
    up_time = datetime.now().replace(microsecond=0) - boot_time
    up_time_list = re.split(r':', str(up_time))
    up_time_format = " {} 小时{} 分钟{} 秒".format(up_time_list[0], up_time_list[1], up_time_list[2])

    # 当前时间
    time_now = time.strftime('%H:%M:%S ', time.localtime(time.time()))
    return render_template(
        'system/monitor.html',
        hostname=hostname,
        system_version=system_version,
        python_version=python_version,
        cpus_percent=cpus_percent,
        memory_usage=memory_usage,
        cpu_count=cpu_count,
        memory_used=memory_used,
        memory_total=memory_total,
        memory_free=memory_free,
        boot_time=boot_time,
        up_time_format=up_time_format,
        disk_partitions_list=disk_partitions_list,
        time_now=time_now
    )


# 图表 api
@bp.get('/polling')
@authorize("system:monitor:main")
def ajax_polling():
    # 获取cpu使用率
    cpus_percent = psutil.cpu_percent(interval=0.1, percpu=False)  # percpu 获取主使用率
    # 获取内存使用率
    memory_information = psutil.virtual_memory()
    memory_usage = memory_information.percent
    time_now = time.strftime('%H:%M:%S ', time.localtime(time.time()))
    return jsonify(cups_percent=cpus_percent, memory_used=memory_usage, time_now=time_now)


# 关闭程序
@bp.get('/kill')
@authorize("system:monitor:main", log=True)
def kill():
    for proc in psutil.process_iter():
        if proc.pid == os.getpid():
            proc.kill()
    sys.exit(1)
