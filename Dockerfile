FROM registry.fedoraproject.org/fedora:36

ENV vulkansdk vulkansdk-linux-x86_64-1.3.224.0.tar.gz
ENV vulkansdk_url https://sdk.lunarg.com/sdk/download/1.3.224.0/linux/vulkansdk-linux-x86_64-1.3.224.0.tar.gz

COPY files/vulkan-env.sh /etc/profile.d/vulkan-env.sh

RUN dnf update -y &&\
    dnf install -y alsa-lib-devel clang cmake doxygen findutils freeglut-devel git gtk3-devel libgcrypt-devel libsecret-devel llvm nasm perl-FindBin perl-File-Compare perl-File-Copy perl-IPC-Cmd pipewire-jack-audio-connection-kit-devel pulseaudio-libs-devel rsync speexdsp-devel systemd-devel vcpkg vim-enhanced vulkan-headers vulkan-loader wget zip &&\
    find /root/ -type f | egrep 'anaconda-ks.cfg|anaconda-post-nochroot.log|anaconda-post.log|original-ks.cfg' | xargs rm -f &&\
    sed -i '/^alias rm.*$/d' /root/.bashrc &&\
    sed -i '/^alias cp.*$/d' /root/.bashrc &&\
    sed -i '/^alias mv.*$/d' /root/.bashrc &&\
    echo -e "\nalias vi='vim'" >> ~/.bashrc &&\
    echo 'defaultyes=True' >> /etc/dnf/dnf.conf &&\
    mkdir /opt/vulkansdk /root/cemu &&\
    wget $vulkansdk_url -P /tmp &&\
    tar --strip-components=1 -xvf /tmp/$vulkansdk --directory=/opt/vulkansdk/ &&\
    git clone --recursive https://github.com/cemu-project/Cemu /root/cemu

# Commented out lines 250 and 251
COPY files/uniform_int_dist.h /usr/include/c++/12/bits/uniform_int_dist.h
# Changed line 10 to #if true
# Removed the curly brackets in line 134 and 144
COPY files/RendererShaderVk.cpp /root/cemu/src/Cafe/HW/Latte/Renderer/Vulkan/RendererShaderVk.cpp

WORKDIR /root

CMD ["/bin/bash"]
