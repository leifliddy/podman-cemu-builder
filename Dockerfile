FROM registry.fedoraproject.org/fedora:36

RUN dnf update -y &&\
    dnf install -y alsa-lib-devel clang cmake doxygen findutils freeglut-devel git gtk3-devel libgcrypt-devel libsecret-devel llvm nasm perl-FindBin perl-File-Compare perl-File-Copy perl-IPC-Cmd pipewire-jack-audio-connection-kit-devel pulseaudio-libs-devel rsync speexdsp-devel systemd-devel vcpkg vim-enhanced vulkan-headers vulkan-loader wget zip &&\
    find /root/ -type f | egrep 'anaconda-ks.cfg|anaconda-post-nochroot.log|anaconda-post.log|original-ks.cfg' | xargs rm -f &&\
    sed -i '/^alias rm.*$/d' /root/.bashrc &&\
    sed -i '/^alias cp.*$/d' /root/.bashrc &&\
    sed -i '/^alias mv.*$/d' /root/.bashrc &&\
    echo -e "\nalias vi='vim'" >> ~/.bashrc &&\
    echo 'defaultyes=True' >> /etc/dnf/dnf.conf &&\
    mkdir /root/cemu &&\
    git clone --recursive https://github.com/cemu-project/Cemu /root/cemu

WORKDIR /root

CMD ["/bin/bash"]
