# Ansible Collection - arbiza.firewall

- ports:
  - one specific port, like 22 or ssh
  - a range using the format first:last
- protocol:
  - protocol name or number, as in /etc/protocols
  - all
- src | dest:
  - when omitted, the rule will apply to any source/destination for IPv4 and IPv6
  - ipv4 or ipv6 plain address
  - ipv4/mask or ipv6/mask

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

Path:

```
.../ansible_collections/arbiza/firewall/
```

```
# ansible.cfg
[defaults]
collections_paths = /home/larbiza/projects/
```
