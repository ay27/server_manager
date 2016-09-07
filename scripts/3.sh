#!/bin/bash

current_version=3

echo "running update version "${current_version}

# 安装gfortran，解决matlab编译问题
apt-get install -y gfortran

# 安装新的脚本
rm /usr/bin/manager
cp manager.py /usr/bin/manager
chmod +x /usr/bin/manager

echo ${current_version} > /root/.manager_version
