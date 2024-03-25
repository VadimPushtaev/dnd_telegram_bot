CONTAINER_NAME="dnd_bot"
IMAGE_NAME="dnd_bot"

docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
docker build -t $IMAGE_NAME .
docker run -d --name $CONTAINER_NAME $IMAGE_NAME
