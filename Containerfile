FROM registry.fedoraproject.org/fedora:37

COPY files/bashrc /root/.bashrc

RUN dnf update -y &&\
    dnf install -y bison clang cmake cubeb-devel findutils freeglut-devel git glm-devel gtk3-devel kernel-headers libgcrypt-devel libsecret-devel nasm ninja-build perl-FindBin perl-File-Compare perl-File-Copy perl-IPC-Cmd rsync systemd-devel vcpkg vim-enhanced wget zip zlib-devel &&\
    find /root/ -type f | egrep 'anaconda-ks.cfg|anaconda-post-nochroot.log|anaconda-post.log|original-ks.cfg' | xargs rm -f &&\
    echo 'defaultyes=True' >> /etc/dnf/dnf.conf &&\
    mkdir /root/.bashrc.d

# set login directory
WORKDIR /root

CMD ["/bin/bash"]
