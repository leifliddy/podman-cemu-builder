# podman-cemu-build
This project builds the cemu source from https://github.com/cemu-project/Cemu   
\
Ok, so this setup assumes that you're running **Fedora 36** and want to compile cemu   
\
**ensure these packages are installed**
```
dnf install podman python3-podman python3-termcolor   
```

**enable (and start) podman.socket**  
if running the script as a normal user
```
systemctl --user enable --now podman.socket
```
 if running the script as root (although there's no need to run this as root)
 ```
systemctl enable --now podman.socket
```

**build cemu**
```
git clone https://github.com/leifliddy/podman-cemu-build.git
cd podman-cemu-build  

# this will build the image and run the container   
./script-podman.py

# login to the container 
podman exec -it cemu_builder /bin/bash

# once inside the container, run this script to build cemu
/root/scripts/01-build.cemu.sh

# the resulting Cemu binary will copied to the /output directory which is shared with the host system

# exit container
Control+D or exit
```

**script-podman.py options**  
these should be pretty self-explanatory
```
usage: script-podman.py [-h] [--debug] [--rebuild | --rerun | --rm_image | --rm_container | --stop_container]

options:
  -h, --help        show this help message and exit
  --debug           display debug messages
  --rebuild         remove podman image and container if they exist, then build (new) podman image and run container
  --rerun           remove the container if it exists, then (re-)run it
  --rm_image        remove podman image and container if they exist
  --rm_container    remove container if it exists
  --stop_container  stop podman container if it exists and is running
```
