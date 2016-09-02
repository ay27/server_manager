#!/bin/bash

current_version=1

# 安装screen,为了支持jupyter的后台执行
apt-get install -y screen

# 安装新的脚本
cp manager.py /usr/bin/manager
chmod 755 /usr/bin/manager

# 删除上一版本的脚本
/root/remote_desktop.sh stop
rm /root/remote_desktop.sh

# 修改python3的默认路径
mv /usr/bin/python3 /usr/bin/python3.old
ln -s /usr/anaconda3/bin/python /usr/bin/python3

# 为了更好的管理平台,将端口从22改为10000, 3389改为10001
sed -i 's/^Port 22$/Port 10000/g' /etc/ssh/sshd_config
sed -i 's/^port=3389$/port=10001/g' /etc/xrdp/xrdp.ini

# 修改启动脚本, 删除remote_desktop相关
sed -i '/xrdp/d' /etc/supervisor/supervisord.conf
sed -i '/remote_desktop.sh/d' /etc/supervisor/supervisord.conf

# 增加python2 的jupyter kernel
/usr/anaconda2/bin/ipython kernel install

echo ${current_version} > /root/.manager_version
