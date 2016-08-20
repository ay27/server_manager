# Server Manager

author: ay27 <me@ay27.com>

## 安装
```shell
./install
```

将会安装在`/usr/bin/manager`

## 使用方法
```shell
manager {desktop, jupyter} {start, stop, restart, del}
```

### 管理远程桌面
```shell
manager desktop start   # 启动远程桌面服务
manager desktop stop    # 停止服务
manager desktop restart # 重启服务
manager desktop del     # 删除当前配置
```

另外, 需要修改桌面的分辨率, 可以这样操作:
```
export GEOMETRY=1366x768    # 设置分辨率, 注意中间是小写x
manager desktop restart     # 设置完后重启服务
```

### 管理jupyter server
```shell
manager jupyter start   # 启动服务, 期间需要设置登陆jupyter 的密码
manager jupyter stop    # 停止服务
manager jupyter del     # 删除当前配置
```