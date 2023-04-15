# Copyright 2023 Lucas Arbiza <lucas@arbiza.com.br>
#
# Dockerfile to create a Debian-based container running iptables
# 
# It provides the user with ssh-key-based authentication and sudo privileges.
#
# BUILDING:
#   docker build --build-arg SSH_USER="$(whoami)" \
#                --build-arg SSH_KEY="$(cat ~/.ssh/<your pub key>)" \
#                -t <image name> .
#
# RUNNING:
#   docker run -d --rm --cap-add NET_ADMIN <image name>

FROM debian:bullseye-slim

ARG SSH_USER
ARG SSH_KEY

RUN apt-get update && apt-get install -y iptables openssh-server sudo python3

# User creation and password
RUN useradd -rm -d /home/${SSH_USER} -s /bin/bash -g root -G sudo -u 1000 ${SSH_USER}
RUN echo "${SSH_USER}:docker" | chpasswd

# SSH key-based login
RUN mkdir /home/${SSH_USER}/.ssh
RUN echo "${SSH_KEY}" > /home/${SSH_USER}/.ssh/authorized_keys
RUN chown -R ${SSH_USER} /home/${SSH_USER}/.ssh
RUN chmod 700 /home/${SSH_USER}/.ssh && chmod 600 /home/${SSH_USER}/.ssh/*

# SSH server configuration
RUN sed -i 's/#PubkeyAuthentication/PubkeyAuthentication/' /etc/ssh/sshd_config

# sudo without password
RUN echo "${SSH_USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${SSH_USER}

RUN service ssh start
EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]
