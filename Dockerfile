FROM jferlez/fastbatllnn-deps:latest

ARG USER_NAME
ARG UID
ARG GID
ARG CORES

RUN sed -i '16i Port 3000' /etc/ssh/sshd_config

# Delete some groups that overlap with MacOS standard user groups
RUN delgroup --only-if-empty dialout
RUN delgroup --only-if-empty fax
RUN delgroup --only-if-empty voice

RUN addgroup --gid ${GID} ${USER_NAME}
RUN useradd -rm -d /home/${USER_NAME} -s /bin/bash -g ${USER_NAME} -G sudo -u ${UID} ${USER_NAME}
RUN echo "${USER_NAME}:${USER_NAME}" | chpasswd
RUN mkdir -p /home/${USER_NAME}/.ssh

RUN mkdir -p /home/${USER_NAME}/results
RUN mkdir -p /media/azuredata
RUN chown -R ${UID}:${UID} /media/azuredata

# switch to unpriviledged user, and configure remote access
WORKDIR /home/${USER_NAME}/tools
RUN chown -R ${UID}:${GID} /home/${USER_NAME}

USER ${USER_NAME}
RUN ssh-keygen -t rsa -q -f /home/${USER_NAME}/.ssh/id_rsa -N ""
RUN cat /home/${USER_NAME}/.ssh/id_rsa.pub >> /home/${USER_NAME}/.ssh/authorized_keys

# Now copy over FastBATLLNN code
RUN git clone --recursive https://github.com/jferlez/FastBATLLNN

WORKDIR /home/${USER_NAME}
RUN git clone https://github.com/jferlez/ACC_Experiments_LTIReach acc23ltireach

WORKDIR /home/${USER_NAME}
RUN sed -i "4i export PYTHONPATH=/home/${USER_NAME}/tools/FastBATLLNN:/home/${USER_NAME}/tools/FastBATLLNN/HyperplaneRegionEnum:/home/${USER_NAME}/tools/FastBATLLNN/TLLnet:/home/${USER_NAME}/tools/nnenum/src/nnenum" /home/${USER_NAME}/.bashrc
RUN echo "export TERM=xterm-256color" >> /home/${USER_NAME}/.bashrc
RUN echo "export COLORTERM=truecolor" >> /home/${USER_NAME}/.bashrc
RUN echo "export TERM_PROGRAM=iTerm2.app" >> /home/${USER_NAME}/.bashrc
RUN echo "set-option -gs default-terminal \"tmux-256color\" # Optional" >> /home/${USER_NAME}/.tmux.conf
RUN echo "set-option -gas terminal-overrides \"*:Tc\"" >> /home/${USER_NAME}/.tmux.conf
RUN echo "set-option -gas terminal-overrides \"*:RGB\"" >> /home/${USER_NAME}/.tmux.conf

USER root
RUN chown -R ${UID}:${GID} /home/${USER_NAME}/

COPY ./DockerConfig/startup.sh /usr/local/bin/startup.sh
RUN chmod 755 /usr/local/bin/startup.sh

ENTRYPOINT [ "/usr/local/bin/startup.sh" ]
