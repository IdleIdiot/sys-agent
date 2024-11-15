#!/bin/bash

# 更新系统包列表
sudo apt-get update -y

# 检查Docker是否已安装
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Installing Docker..."
    sudo apt-get install -y docker.io
else
    echo "Docker is already installed."
fi

# 检查Docker Compose是否已安装
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose is already installed."
fi

# 检查Docker配置文件是否存在
if [ ! -f /etc/docker/daemon.json ]; then
    echo "Configuring Docker with a registry mirror..."
    sudo mkdir -p /etc/docker
    sudo tee /etc/docker/daemon.json <<-EOF
    {
      "registry-mirrors": ["https://hub.geekery.cn"]
    }
EOF
else
    echo "Docker configuration file already exists."
    # 如果需要检查镜像源是否已配置，可以进一步添加检查逻辑
fi

# 重启Docker服务以使更改生效
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "Docker and Docker Compose have been installed and configured successfully."

mkdir -p ./es
chmod -R 777 ./es

# install iostat