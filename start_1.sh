docker stop $(sudo docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker-compose -f ./docker-compose.yml up