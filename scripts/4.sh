#!/bin/bash

current_version=4

echo "running update version "${current_version}

# install TensorFlow in Python2.7 with CPU Only
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0-cp27-none-linux_x86_64.whl
/usr/anaconda2/bin/pip install $TF_BINARY_URL

# install TensorFlow in Python3.5 with CPU Only
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0-cp35-cp35m-linux_x86_64.whl
/usr/anaconda3/bin/pip install $TF_BINARY_URL

# 安装新的脚本
rm /usr/bin/manager
cp manager.py /usr/bin/manager
chmod +x /usr/bin/manager


# 删除/root/.server_manager
rm -rf /root/.server_manager

echo ${current_version} > /root/.manager_version
