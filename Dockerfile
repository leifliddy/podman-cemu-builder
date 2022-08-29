FROM registry.fedoraproject.org/fedora:36

RUN dnf update -y &&\
    dnf install -y clang cmake cubeb-devel findutils freeglut-devel git gtk3-devel kernel-headers libgcrypt-devel libsecret-devel nasm perl-FindBin perl-File-Compare perl-File-Copy perl-IPC-Cmd pulseaudio-libs-devel rsync systemd-devel vcpkg vim-enhanced wget zip &&\
    find /root/ -type f | egrep 'anaconda-ks.cfg|anaconda-post-nochroot.log|anaconda-post.log|original-ks.cfg' | xargs rm -f &&\
    sed -i '/^alias rm.*$/d' /root/.bashrc &&\
    sed -i '/^alias cp.*$/d' /root/.bashrc &&\
    sed -i '/^alias mv.*$/d' /root/.bashrc &&\
    echo -e "\nalias vi='vim'" >> ~/.bashrc &&\
    echo 'defaultyes=True' >> /etc/dnf/dnf.conf &&\
    mkdir /root/cemu &&\
    git clone --recursive https://github.com/cemu-project/Cemu /root/cemu

# set login directory
WORKDIR /root

CMD ["/bin/bash"]
