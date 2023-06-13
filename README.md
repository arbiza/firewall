# Ansible Collection - arbiza.firewall

This Ansible Collection deploys a firewall intended for Linux servers exposed to the Internet. At the current state, it supports Iptables only.

I've used this firewall for a long time as a bash script; now, I re-wrote it using Ansible.

## Features

- Allows loopback traffic
- Allows DNS queries
- Allows HTTP and HTTPS output for system updates
- Allows ICMP type 8
- RFC 4890 - ICMPv6
- Rules applied for both IPv4 and IPv6, unless the source or destination has been specified using an IP address
- Port Knocking

Apart from the above, it blocks all other incoming and outcoming connections, except what is explicitly open.

## Usage instructions

### Instalation

```shell
ansible-galaxy collection install arbiza.firewall
```

### Roles and Modules

_Please, check the [playbook.yml](playbook.yml) for an extensive example._

#### Role 'arbiza.firewall.iptables'

__Variables available:__

- input | output:
  - ports:
    - one specific port, like 22 or ssh
    - a range using the format first:last
  - protocol:
    - protocol name or number, as in /etc/protocols
    - all
  - src (for input) | dest (for output):
    - when omitted, the rule will apply to any source/destination for IPv4 and IPv6
    - ipv4 or ipv6 plain address
    - ipv4/mask or ipv6/mask

__Example__:

```yaml
input:
  - ports: 25
    protocol: tcp
    src: 10.10.10.0/24
output:
  - ports: 25
    protocol: tcp
    dest: 10.10.10.0/24
```

- port_knocking - list of dictionaries containing:
  - 'open': port to open when knocking succeeds
  - 'ports': list of ports that have to be knocked
  - 'duration': time in seconds the port defined in 'open' will accept connections - default is 60

__Example__:

```yaml
- open: 22
  ports: [26896, 4099, 63793]
  duration: 30
```

#### Module 'arbiza.firewall.knock'

This is a port knocking module which will knock at as many servers are listed in parallel (it uses threads).

The module will fail when knocking any of the listed servers fails.

__Example__:

```yaml
- name: Knock, knock, knock
  arbiza.firewall.knock:
    knock_at:
      - host: 10.10.10.1
        ports: [26896, 4099, 63793]
      - host: 10.10.10.2
        ports: [27536, 9908, 64333]
```

## 'Lab'

You can try this collection using the playbook, inventory, and container configuration it provides.

### Requirements

- Container engine (e.g.: Docker)
- Ansible

### Running

Enable containers access to the Internet (required to install Iptables):

```shell
# Non-persistent rules
sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
```

The following disables host-key checking for the containers.

Add the following to '~/.ssh/config' file:

```shell
# ~/.ssh/config
Host 10.6.6.0/24
    StrictHostKeyChecking no
```

Build the image and run the containers with these commands. The image will have your user configured and SSH public key so that you can access it without a password.

```shell
# Run these commands in this project's root directory

docker build --build-arg SSH_USER="$(whoami)" \
             --build-arg SSH_KEY="$(cat ~/.ssh/<your pub key>)" \
             -t local/firewall .

docker compose up -d
```

SSH into the containers:

```shell
ssh 10.6.6.6
ssh 10.6.6.7
```

Run the playbook:

```shell
# 1st run
ansible-playbook playbook.yml -i inventory.yml --skip-tags knock

# from the 2nd run
ansible-playbook playbook.yml -i inventory.yml

# reload
ansible-playbook playbook.yml -i inventory.yml --tags reload

# stop - disables the firewall; allows everything
ansible-playbook playbook.yml -i inventory.yml --tags stop

# port knocking only
ansible-playbook playbook.yml -i inventory.yml --tags knock

```
