#!/bin/bash

current_version=4

echo "running update version "${current_version}

# 安装新的脚本
rm /usr/bin/manager
cp manager.py /usr/bin/manager
chmod +x /usr/bin/manager


# 删除/root/.server_manager
rm -rf /root/.server_manager

echo ${current_version} > /root/.manager_version
