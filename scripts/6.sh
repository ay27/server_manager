#!/bin/bash

current_version=6

echo "running update version "${current_version}

# 更换pip 源,指向阿里的源,速度更快
if [ ! -d "/root/.pip" ]; then
  mkdir /root/.pip
fi
echo "[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple
" > /root/.pip/pip.conf

# 安装新的脚本
rm /usr/bin/manager
cp manager.py /usr/bin/manager
chmod +x /usr/bin/manager


# 删除/root/.server_manager
rm -rf /root/.server_manager

echo ${current_version} > /root/.manager_version
