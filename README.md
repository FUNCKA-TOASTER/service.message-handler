# ⚙️ SERVICE.MESSAGE-HANDLER

![main_img](https://github.com/STALCRAFT-FUNCKA/toaster.message-handling-service/assets/76991612/8bb6b3bf-8385-4d4b-80cc-e104d5283a9c)

## 📄 Информация

**SERVICE.MESSAGE-HANDLER** - сервис обработки событий, классифицированных как нажатие "message". Событие приходит от сервиса фетчинга, после чего обрабатывается. Праллельно производятся необходимые действия внутреннего\внешнего логирования.

### Входные данные

```python
class Event:
    event_id: int
    event_type: str

    peer: Peer
    user: User
    message: Message

```

```python
class Message(NamedTuple):
    cmid: int
    text: str
    reply: Optional[Reply]
    forward: List[Reply]
    attachments: List[str]
```

```python
class Peer(NamedTuple):
    bpid: int
    cid: int
    name: str
```

```python
class User(NamedTuple):
    uuid: int
    name: str
    firstname: str
    lastname: str
    nick: str
```

Пример события, которое приходит от toaster.event-routing-service сервера на toaster.message-handling-service.

Далее, сервис определяет, какая команда была вызвана, а уже после - исполняет все действия, которые за этой командой сокрыты.

### Выходные данные

Каждый раз, когда какой-то из фильтров или систем реагируют на нарушения\определенные условия, сервису необходимо тоже что-то отправить в шину Redis.
Реакция какого-либо филтьра или системы подразумевает применение каких-то санкций в сторону пользователя.
Отсюда появляется новый тип события "Punishment". Оно значительно проще события "Event", но играет не меньшую роль в работе сервисов.

```python
class Punishment:
    punishment_type: str
    comment: str
    cmids: Union[int, List[int]]
    bpid: int
    uuid: int
    points: Optional[int]
    mode: Optional[str]
```

### Дополнительно

Docker setup:

```shell
docker network
    name: TOASTER
    ip_gateway: 172.18.0.1
    subnet: 172.18.0.0/24
    driver: bridge


docker image
    name: service.message-handler
    args:
        TOKEN: "..."
        GROUPID: "..."
        SQL_HOST: "..."
        SQL_PORT: "..."
        SQL_USER: "..."
        SQL_PSWD: "..."


docker container
    name: service.message-handler
    network_ip: 172.1.08.8

```

Jenkins shell command:

```shell
imageName="service.message-handler"
containerName="service.message-handler"
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
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
