

## 1. Server 服务部署
docker compose up -d


![界面展示](static/monitor.png)

## 2. Client 代理部署
### 2.1 Python

建议 Python 版本为 3.9以上，若低于该版本，依赖库的安装可能没有对应的版本

若希望在低版本运行，安装依赖时将 requirements.txt 中的版本限制移除再次安装尝试既可

```
python --version

Python 3.9.19

pip install -r requirements.txt
```



### 2.2 配置 Host ID
修改 settings.py 文件

`vim config/settings.py`

将监控项1000中的参数 args 更改为你的网卡名称

```
## Set 1000 item args to your server nic.

"1000": {
    "func": CommonSniffApi.get_ip_address,
    "args": "ens2f0",
    "alias": "host_id",
}
```



### 2.3 配置数据库和消息队列服务 Database & MQ
**修改配置文件中的数据库和消息队列的服务IP**

`vim config/settings.py`

例如：`10.121.177.161` 中存在已经部署的好的数据库和消息队列服务，将 IP 信息修改即可

```
message_queue = {
    "rabbitmq": {
        "host": "10.121.177.161",
        "port": "5672",
        "queue": "",
        "username": "",
        "passwd": "",
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

### 2.4 自定义监控任务
添加新的监控项仅需要三个步骤
1. 添加接口在 sniff 目录下
2. 配置 settings.py 文件
3. 修改 task.py 将新任务添加到任务列表


### 2.5. 监控代理运行
添加好自定义监控项后，挂在系统后台运行程序

cd client
nohup python app.py --task_name custom_task &


