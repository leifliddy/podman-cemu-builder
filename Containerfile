FROM registry.fedoraproject.org/fedora:39

COPY files/bashrc /root/.bashrc
COPY files/bashrc-default /root/.bashrc.d/default

RUN dnf update -y &&\
    dnf install -y bison clang cmake cubeb-devel findutils freeglut-devel git glm-devel gtk3-devel kernel-headers libgcrypt-devel libsecret-devel libtool libusb1-devel nasm ninja-build python3-pip perl-open perl-FindBin perl-File-Compare perl-File-Copy perl-IPC-Cmd rsync systemd-devel vcpkg vim-enhanced wayland-protocols-devel wget zip zlib-devel &&\
    pip3 install jinja2 passlib &&\
    find /root/ -type f | grep -E 'anaconda-ks.cfg|anaconda-post-nochroot.log|anaconda-post.log|original-ks.cfg' | xargs rm -f &&\
    echo 'defaultyes=True' >> /etc/dnf/dnf.conf

# set login directory
WORKDIR /root

CMD ["/bin/bash"]
