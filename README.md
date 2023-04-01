## Build a Python based microservice to convert Video files into audio file.

This is a python-Flask based microservice architecture to convert video files into mp3. Each services are dockerized and orchastrated using Kubernetes.

Architecture includes
- Gateway Service
- Authentication Service
- Notification Service
- Queue for asynchronus intercommunication service
- File Convertor Service
- Notification Service

Technologies used:
- Python
- Flask
- Docker
- Kubernetes
- RabbitMQ as message Queue
- Mongo DB
- Sql
- MongoDB

Endpoints:

To get JWT Token
> $ curl -X POST http://mp3converter.com/login -u renjith@gmail.com:Admin123

To upload Video
> $ curl -X POST -F 'file=@./{filename}' -H 'Authorization: Bearer {JWT}' http://mp3converter.com/upload

To download video
> $ curl --output mp3_download.mp3 -X GET -H 'Authorization: Bearer {JWT}' 'http://mp3converter.com/download?fid={mongo_id}'

