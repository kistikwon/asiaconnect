FROM asifraza/kisti-mpi:latest

# mpi-operator mounts the .ssh folder from a Secret. For that to work, we need
# to disable UserKnownHostsFile to avoid write permissions.
# Disabling StrictModes avoids directory and files read permission checks.


#RUN useradd -rm -d /home/mpiuser -s /bin/bash -g root -G sudo -u 1001 mpiuser
#USER mpiuser
#WORKDIR /home/mpiuser
RUN /usr/bin/python -m pip install --upgrade pip
RUN pip install mpi4py

#RUN echo "    UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config && \
#    sed -i 's/#\(StrictModes \).*/\1no/g' /etc/ssh/sshd_config
#ADD . /var/tf_dist_mnist
#ENTRYPOINT ["python", "/var/tf_dist_mnist/dist_mnist.py"]



RUN mkdir /byounghyun
WORKDIR "/byounghyun"
RUN git clone https://github.com/MolSSI-Education/parallel-programming.git
WORKDIR "/byounghyun/parallel-programming/examples/mpi4py/example2/final"

CMD ["/bin/bash"]
