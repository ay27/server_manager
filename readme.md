# Server Manager

author: ay27 <jinmian.y@gmail.com>

## 版本：6

1. 更换pip 源,现在使用pip 安装软件速度更快了
2. 加入了fix_pip 命令,现在可以使用`manager fix_pip` 命令修复pip 错误了

## 版本：5

1. 更新了TensorFlow 的版本
2. 修复一个在关闭远程桌面服务时出现的bug

## 版本：4

1. 更新了manager 工具升级策略
2. 加入了TensorFlow 支持，现在可以在系统中的python2.7 或 python3.5 环境中直接使用了，jupyter 环境同样支持TensorFlow

## 版本：3

1. 安装了gfortran，解决了matlab中需要编译Fortran依赖包的问题
2. 修复了一个manager 工具中的bug，该bug可能导致远程桌面服务无法正常关闭

## 版本：2

### 更新说明
1. 因为阿里云的软件源不稳定，因此将软件源改为ubuntu中国官方源
2. 安装build-essential，包括了gcc，g++，make，automake 等常用编译库
3. 安装了rz 和sz 命令，让windows 用户可以更方便地上传、下载文件
4. 完善了manager 工具

## 版本：1

### 更新说明

1. 将旧的管理脚本升级为manager 工具
2. 增加jupyter server的管理

### 安装
```shell
cd server_manager && ./install
```

将会安装在`/usr/bin/manager`

### 使用方法
```shell
manager {desktop, jupyter, update} {start, stop, restart, del}
```

#### 管理远程桌面
```shell
manager desktop start   # 启动远程桌面服务
manager desktop stop    # 停止服务
manager desktop restart # 重启服务
```

另外, 需要修改桌面的分辨率, 可以这样操作:
```shell
export GEOMETRY=1366x768    # 设置分辨率, 注意中间是小写x
manager desktop restart     # 设置完后重启服务
```

而需要修改远程桌面登陆密码，可以这样操作：

```shell
manager desktop stop		# 停止服务
vncpasswd					# 修改密码(该密码可以与用户密码不同)
```

#### 管理jupyter server

```shell
manager jupyter start   # 启动服务, 期间需要设置登陆jupyter 的密码
manager jupyter stop    # 停止服务
manager jupyter del     # 删除当前配置
```

#### 更新管理工具
```shell
manager update		# 将会自动获取最新的版本号，并更新
```
