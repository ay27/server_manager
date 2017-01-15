#!/bin/bash

current_version=5

echo "running update version "${current_version}

# update tensorflow
/usr/anaconda2/bin/pip uninstall -y tensorflow
/usr/anaconda2/bin/pip install tensorflow

# install TensorFlow in Python3.5 with CPU Only
/usr/anaconda3/bin/pip uninstall -y tensorflow
/usr/anaconda3/bin/pip install tensorflow

# 安装新的脚本
rm /usr/bin/manager
cp manager.py /usr/bin/manager
chmod +x /usr/bin/manager


# 删除/root/.server_manager
rm -rf /root/.server_manager

echo ${current_version} > /root/.manager_version
