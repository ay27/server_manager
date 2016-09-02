#!/bin/bash

current_version=2

echo "running update version "${current_version}

# 把阿里云的软件源替换成中科大的软件源
function backup_sources()
{
    echo -e "Backup your sources.list.\n"
    sudo mv /etc/apt/sources.list /etc/apt/sources.list.`date +%F-%R:%S`
}

function update_sources()
{
    local COMP="main restricted universe multiverse"
    local mirror="$1"
    local tmp=$(mktemp)
    local VERSION="trusty"

	echo "deb $mirror $VERSION $COMP" >> $tmp
	echo "deb $mirror $VERSION-updates $COMP" >> $tmp
	echo "deb $mirror $VERSION-backports $COMP" >> $tmp
	echo "deb $mirror $VERSION-security $COMP" >> $tmp
	echo "deb $mirror $VERSION-proposed $COMP" >> $tmp
	echo "deb-src $mirror $VERSION $COMP" >> $tmp
	echo "deb-src $mirror $VERSION-updates $COMP" >> $tmp
	echo "deb-src $mirror $VERSION-backports $COMP" >> $tmp
	echo "deb-src $mirror $VERSION-security $COMP" >> $tmp
	echo "deb-src $mirror $VERSION-proposed $COMP" >> $tmp

    sudo mv "$tmp" /etc/apt/sources.list
    # echo -e "Your sources has been updated, and maybe you want to run \"sudo apt-get update\" now.\n";
}

backup_sources
update_sources http://mirrors.ustc.edu.cn/ubuntu/
apt-get update

# 安装build-essential
apt-get install -y build-essential
# 安装rz与sz服务，方便windows用户
wget http://www.ohse.de/uwe/releases/lrzsz-0.12.20.tar.gz
tar zxvf lrzsz-0.12.20.tar.gz && cd lrzsz-0.12.20
./configure && make && make install
cd .. && rm -rf lrzsz-0.12.20
ln -s /usr/local/bin/lrz /usr/local/bin/rz
ln -s /usr/local/bin/lsz /usr/local/bin/sz

# 安装新的脚本
rm /usr/bin/manager
cp manager.py /usr/bin/manager
chmod +x /usr/bin/manager

echo ${current_version} > /root/.manager_version
