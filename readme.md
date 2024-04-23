## Environments

### Python(required)
python --version
Python 3.9.19

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

### Host ID(required)
vim config/settings.py
Set 1000 item args to your server nic.

"1000": {
    "func": CommonSniffApi.get_ip_address,
    "args": "ens2f0",
    "alias": "host_id",
},

### Database & MQ(Option|If no database then Required)
cat services.help
Install docker at Data Server
Run docker command

#### Config
** Modify Database & MQ Server IP **
config/settings.py

** Custom Agent Server Tasks. **
see: config/settings.py
config/tasks.py   |  Add Item | Del Item


#### If you want to increment item interface(Option)
Add interface at sniff/ directory.
Config config/settings.py
config/tasks.py   |  Add Item | Del Item

## Run Demo
nohup python app.py &


## Kill Process
ps -aux | grep app
kill {pid}