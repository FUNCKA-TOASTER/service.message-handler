# ⚙️ TOASTER.MESSAGE-HANDLING-SERVICE

![main_img](https://github.com/STALCRAFT-FUNCKA/toaster.message-handling-service/assets/76991612/8bb6b3bf-8385-4d4b-80cc-e104d5283a9c)

## 📄 Информация ##

**TOASTER.MESSAGE-HANDLING-SERVICE** - сервис обработки событий, классифицированных как нажатие кнопки. Событие приходит от сервиса фетчинга, после чего обрабатывается. Праллельно производятся необходимые действия внутреннего\внешнего логирования.

### Входные данные:

**MessageEvent (message_new):**
```
content type: application\json

{
    "ts": 1709107923,
    "datetime": "2024-02-28 11:12:03",
    "event_type": "message_new", 
    "event_id": "8dd52b4d7c822b78db23db85bf351c7114e46b36", 
    "user_id": 206295116, 
    "user_name": "Руслан Башинский", 
    "user_nick": "oidaho", 
    "peer_id": 2000000002, 
    "peer_name": "FUNCKA | DEV | CHAT", 
    "chat_id": 2, 
    "cmid": 2708, 
    "text": "Hi!", 
    "reply": null, 
    "forward": [], 
    "attachments": []
}
```

Пример события, которое приходит от toaster.event-routing-service сервера на toaster.message-handling-service.

Далее, сервис определяет, какая команда была вызвана, а уже после - исполняет все действия, которые за этой командой сокрыты.


### Дополнительно

Docker setup:
```
docker network
    name: TOASTER
    ip_gateway: 172.18.0.1
    subnet: 172.18.0.0/16
    driver: bridge


docker image
    name: toaster.message-handling-service
    args:
        TOKEN: "..."
        GROUPID: "..."
        SQL_HOST: "..."
        SQL_PORT: "..."
        SQL_USER: "..."
        SQL_PSWD: "..."


docker container
    name: toaster.messaage-handling-service
    network_ip: 172.1.08.8

docker volumes:
    /var/log/TOASTER/toaster.message-handling-service:/service/logs
```     

Jenkins shell command:
```
imageName="toaster.message-handling-service"
containerName="toaster.message-handling-service"
localIP="172.18.0.8"
networkName="TOASTER"

#stop and remove old container
docker stop $containerName || true && docker rm -f $containerName || true

#remove old image
docker image rm $imageName || true

#build new image
docker build . -t $imageName \
--build-arg TOKEN=$TOKEN \
--build-arg GROUPID=$GROUPID \
--build-arg SQL_HOST=$SQL_HOST \
--build-arg SQL_PORT=$SQL_PORT \
--build-arg SQL_USER=$SQL_USER \
--build-arg SQL_PSWD=$SQL_PSWD

#run container
docker run -d \
--name $containerName \
--volume /var/log/TOASTER/$imageName:/service/logs \
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
