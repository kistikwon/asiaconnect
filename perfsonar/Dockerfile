FROM perfsonar/testpoint:systemd

RUN psconfig remote add --configure-archives http://134.75.115.137/psconfig/test.json
RUN mkdir /perfsonar
WORKDIR "/perfsonar"
#ENTRYPOINT ["tail", "-f", "/dev/null"]

#CMD ["/bin/bash"]
