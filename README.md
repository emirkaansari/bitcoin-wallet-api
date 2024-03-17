# Async Bitcoin wallet API

## how to run?
### prerequisites:
- docker
- docker compose

```bash
$ docker-compose up -d --build 
$ docker-compose exec web alembic upgrade head
```

### the app will start running on
http://localhost:8002

### the apidocs are here: 
http://locahost:8002/docs

### run the tests
```bash
$ docker-compose exec web pytest
```
