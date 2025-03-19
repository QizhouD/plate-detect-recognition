离线安装依赖：
cd (.venv) PS D:\plate\packages>
pip install -r dev.txt




docker build -t plate-detection .
docker run -d -p 5000:5000 --name plate-detection-container plate-detection


docker stop plate-detection-container

docker rm plate-detection-container