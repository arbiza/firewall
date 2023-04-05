# Copyright 2023 Lucas Arbiza <lucas@arbiza.com.br>
#
# Dockerfile to create a Debian-based container running iptables
#
# BUILDING:
#   docker build -t --build-arg SSH_USER="$(whoami)" --build-arg SSH_KEY="~/.ssh/id_ed25519.pub)" <image name> .
#
# RUNNING:
#   docker run --rm --cap-add NET_ADMIN -ti <image name>

FROM debian:bullseye-slim

ARG SSH_USER
ARG SSH_KEY

RUN apt-get update && apt-get install -y iptables openssh-server

RUN useradd -rm -d /home/${SSH_USER} -s /bin/bash -g root -G sudo -u 1000 ${SSH_USER}
RUN mkdir /home/${SSH_USER}/.ssh
RUN echo "${SSH_KEY}" > /home/${SSH_USER}/.ssh/authorized_keys
RUN chmod 600 /home/${SSH_USER}/.ssh && chmod 400 /home/${SSH_USER}/.ssh/*

RUN service ssh start
EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]
