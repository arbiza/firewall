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
# Non-persistent rules
sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
```

```
# ~/.ssh/config
Host 10.6.6.0/24
    StrictHostKeyChecking no
```
