## Environments

### Python
python --version
Python 3.9.19

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

### Database & MQ
cat services.help
Install docker at Data Server
Run docker command

### Config
#### Modify Database & MQ Server IP
config/settings.py

#### Custom Agent Server Tasks.
see: config/settings.py
config/tasks.py   |  Add Item | Del Item


#### If you want to increment item interface
Add interface at sniff/ directory.
Config config/settings.py
config/tasks.py   |  Add Item | Del Item

## Demo
nohup python app.py &