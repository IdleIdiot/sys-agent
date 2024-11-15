## 1. 环境搭建


### 1.1 Python

建议 Python 版本为 3.9以上，若低于该版本，依赖库的安装可能没有对应的版本

若希望在低版本运行，安装依赖时将 requirements.txt 中的版本限制移除再次安装尝试既可

python --version

Python 3.9.19

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple




### 1.2 配置 Host ID
修改 settings.py 文件

vim config/settings.py

将监控项1000中的参数 args 更改为你的网卡名称

Set 1000 item args to your server nic.

"1000": {
    "func": CommonSniffApi.get_ip_address,
    "args": "ens2f0",
    "alias": "host_id",
},




### 1.3 配置数据库和消息队列服务 Database & MQ
如果已经有搭建好的服务，不用再重新部署服务

如果没有服务，可以参考 services.help 中的命令，部署服务


#### 1.3.1 Config
**修改配置文件中的数据库和消息队列的服务IP**

vim config/settings.py

例如：10.121.177.161 中存在已经部署的好的数据库和消息队列服务，将 IP 信息修改即可

```
message_queue = {
    "rabbitmq": {
        "host": "10.121.177.161",
        "port": "5672",
        "queue": "server-test",
        "username": "rabbit-user",
        "passwd": "123456",
    },
}


database = {
    "elasticsearch": {
        "ip": "10.121.177.161",
        "port": 9200,
        "user": "",
        "pwd": "",
    },
}
```

**自定义监控任务**


### 1.4 如何添加一个新的监控任务
见下方MR链接，一个新监控项的提交

[How to add GPU power](http://10.121.176.191:8280/automation/sys-agent/-/commit/4ec0764568a2ea1bbd8fc2b65ac7dfc45a058d0f#)


添加新的监控项仅需要三个步骤
1. 添加接口在 sniff 目录下
2. 配置 settings.py 文件
3. 修改 task.py 



## 2. 监控代理运行
添加好自定义监控项后，挂在系统后台运行程序

cd client
nohup python app.py &


## 3. 停止运行
ps -aux | grep app

kill {pid}
