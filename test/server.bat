@echo off
cd ..
docker build . -t my-docker-image-tag
docker run -p 8080:8080 --name=my-docker-container-name my-docker-image-tag
pause