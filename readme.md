## 1. Environments


### 1.1 Python (required)
python --version

Python 3.9.19

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple




### 1.2 Host ID (required)
vim config/settings.py

Set 1000 item args to your server nic.

"1000": {
    "func": CommonSniffApi.get_ip_address,
    "args": "ens2f0",
    "alias": "host_id",
},




### 1.3 Database & MQ (Option|If no database then Required)
cat services.help

Install docker at Data Server

Run docker command


#### 1.3.1 Config
**Modify Database & MQ Server IP**

config/settings.py

**Custom Agent Server Tasks.**

see: config/settings.py

config/tasks.py   |  Add Item | Del Item




### 1.4 If you want to increment item interface (Option)
Add interface at sniff/ directory.

Config config/settings.py

config/tasks.py   |  Add Item | Del Item




## 2. Run Demo
nohup python app.py &




## 3. Kill Process
ps -aux | grep app

kill {pid}


On my way.