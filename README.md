# Ansible Collection - arbiza.firewall

# Docker

```
docker build --build-arg SSH_USER="$(whoami)" \
             --build-arg SSH_KEY="$(cat ~/.ssh/<your pub key>)" \
             -t local/firewall .
```

```
docker compose up -d
```

```
# ~/.ssh/config
Host 10.6.6.0/24
    StrictHostKeyChecking no
```
