#!/usr/bin/python3

import argparse
import os
import rpm
import selinux
import subprocess
import sys
import time
from podman import PodmanClient
from termcolor import cprint


podman_image_name     = 'cemu_build_env'
podman_container_name = 'cemu_builder'
container_hostname    = 'cemu_builder'


def print_yes():
    cprint(' [YES]', 'green')


def print_no():
    cprint(' [NO]', 'red')


def print_soft_no():
    cprint(' [NO]', 'yellow', attrs=['bold','dark'])


def print_success():
    cprint(' [SUCCESS]', 'green')


def print_failure():
    cprint(' [FAILURE]', 'red')


def check_podman_installed():
    cprint('{0:.<70}'.format('PODMAN: is podman installed'), 'yellow', end='')
    podman_installed = None
    ts = rpm.TransactionSet()
    rpm_listing = ts.dbMatch()

    for rpm_pkg in rpm_listing:
        if rpm_pkg['name'] == 'podman':
            podman_installed = True

    if podman_installed:
        print_yes()
    else:
        print_no()
        cprint('\npodman is not installed', 'magenta')
        cprint('Exiting...', 'red')
        sys.exit(1)


def ensure_podman_socket_running():
    if os.geteuid() == 0:
        user = ''
    else:
        user = '--user '

    cmd_str = f'systemctl {user} is-active --quiet podman.socket'
    cmd = cmd_str.split()
    cmd_output = subprocess.run(cmd)

    if cmd_output.returncode == 0:
        return

    cprint('PODMAN: starting podman.socket...', 'yellow')

    cmd_str = f'systemctl {user}start podman.socket'
    cmd = cmd_str.split()
    cmd_output = subprocess.run(cmd, capture_output=True, universal_newlines=True)

    if args.debug:
        cprint('DEBUG: running command:', 'yellow')
        cprint(f'{cmd_str}', 'yellow', attrs=['bold'])

    if cmd_output.returncode != 0:
        err_output = cmd_output.stderr.rstrip()
        cprint(err_output, 'red', attrs=['bold'])
        sys.exit(2)


def ensure_image_exists():
    cprint('{0:.<70}'.format('PODMAN: checking if image exists'), 'yellow', end='')
    podman_image = client.images.list(filters = {'reference' : podman_image_name})

    if podman_image:
        print_yes()
    else:
        print_soft_no()
        cprint('PODMAN: building image...', 'yellow')
        cur_dir = os.path.dirname(os.path.realpath(__file__))

        if args.debug:
            podman_build_image_manual = f'podman build --squash -t {podman_image_name} .'
            cprint('DEBUG: to manually build the image:', 'yellow')
            cprint(f'{podman_build_image_manual}', 'yellow', attrs=['bold'])

        cmd_output = subprocess.run(['podman', 'build', '--squash', '-t', podman_image_name, cur_dir], universal_newlines=True)

        cprint('{0:.<70}'.format('PODMAN: build image'), 'yellow', end='')

        if cmd_output.returncode != 0:
            print_failure()
            cprint('Exiting...', 'red')
            sys.exit(3)
        else:
            print_success()


def ensure_image_removed():
    cprint('{0:.<70}'.format('PODMAN: checking if image exists'), 'yellow', end='')
    podman_image_exists = client.images.list(filters = {'reference' : podman_image_name})

    if podman_image_exists:
        print_yes()
        cprint('PODMAN: removing image...', 'yellow')
        client.images.remove(image=podman_image_name)
    else:
        print_soft_no()


def ensure_container_exists_and_running():
    cprint('{0:.<70}'.format('PODMAN: checking if container exists'), 'yellow', end='')
    container_exists = client.containers.list(all=True, filters = {'name' : podman_container_name})

    if container_exists:
        print_yes()
        podman_container = client.containers.get(podman_container_name)
        container_status = podman_container.status

        cprint('{0:.<70}'.format('PODMAN: checking if container is running'), 'yellow', end='')

        if container_status == 'running':
            print_yes()
        else:
            print_soft_no()
            cprint('PODMAN: starting container...', 'yellow')
            podman_container.start()
            ensure_container_exists_and_running()
    else:
        print_soft_no()
        run_container()
        ensure_container_exists_and_running()


def create_mounts_dict(host_mount, container_mount):
    mounts = {
               'type':   'bind',
               'source': host_mount,
               'target': container_mount,
             }

    return mounts


def ensure_container_stopped_removed(remove_container=True):
    cprint('{0:.<70}'.format('PODMAN: checking if container exists'), 'yellow', end='')
    container_exists = client.containers.list(all=True, filters = {'name' : podman_container_name})

    if container_exists:
        print_yes()
        podman_container = client.containers.get(podman_container_name)
        container_status = podman_container.status

        cprint('{0:.<70}'.format('PODMAN: checking if container is running'), 'yellow', end='')

        if container_status != 'exited':
            print_yes()
            cprint('PODMAN: stopping container...', 'yellow')
            podman_container.stop()
            if remove_container:
                time.sleep(3)
        else:
            print_soft_no()

        if remove_container:
            cprint('PODMAN: removing container...', 'yellow')
            podman_container.remove()

    else:
        print_soft_no()


def set_selinux_context_t():
    cprint('{0:.<70}'.format('PODMAN: selinux label check'), 'yellow', end='')
    mount_dirs_and_files = ['output', 'build.scripts', 'build.scripts/01-build.cemu.sh']
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    container_context_t = 'container_file_t'

    for element in mount_dirs_and_files:
        element_path = f'{cur_dir}/{element}'
        ret, element_context = selinux.getfilecon(element_path)

        if ret < 0:
            print_failure()
            cprint(f'selinux.getfilecon({element_path}) failed....exiting', red)
            sys.exit(3)

        element_context_t = element_context.split(":")[2]
        if element_context_t != container_context_t:
            element_context = element_context.replace(element_context_t, container_context_t)
            selinux.setfilecon(element_path, element_context)

    print_yes()

def run_container():
    # ensure ./output and ./build.scripts have the container_file_t label set
    if selinux.is_selinux_enabled():
        set_selinux_context_t()

    cprint('PODMAN: run container...', 'yellow')
    bind_volumes          = []
    cur_dir               = os.path.dirname(os.path.realpath(__file__))
    bind_volumes.append(create_mounts_dict(f'{cur_dir}/output', '/output'))
    bind_volumes.append(create_mounts_dict(f'{cur_dir}/build.scripts', '/root/scripts'))

    if args.debug:
        podman_run_cmd_manual = f'podman run -d -it -v $(pwd)/output:/output -v $(pwd)/build.scripts:/root/scripts -h {container_hostname} --name {podman_container_name} {podman_image_name}\n'
        cprint('DEBUG: to manually run the container:', 'yellow')
        cprint(f'{podman_run_cmd_manual}', 'yellow', attrs=['bold'])

    client.containers.run(image=podman_image_name, name=podman_container_name, hostname=container_hostname, detach=True, tty=True, privileged=False, mounts=bind_volumes)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('--debug',
                        action='store_true',
                        help='display debug messages',
                        default=False)
    group.add_argument('--rebuild',
                        action='store_true',
                        help='remove podman image and container if they exist, '
                             'then build (new) podman image and run container',
                        default=False)
    group.add_argument('--rerun',
                        action='store_true',
                        help='remove the containers if they exist, then (re-)run them',
                        default=False)
    group.add_argument('--rm_image',
                        action='store_true',
                        help='remove podman image and container if they exist',
                        default=False)
    group.add_argument('--rm_container',
                        action='store_true',
                        help='remove container if it exists',
                        default=False)
    group.add_argument('--stop_container',
                        help='stop podman container it exists and is running',
                        action='store_true',
                        default=False)

    args = parser.parse_args()
    check_podman_installed()
    ensure_podman_socket_running()

    if os.geteuid() == 0:
        client = PodmanClient(base_url='unix:/run/podman/podman.sock')
    else:
        client = PodmanClient()

    if args.rm_image or args.rebuild:
        ensure_container_stopped_removed()
        ensure_image_removed()
        if args.rm_image: sys.exit()

    if args.rm_container or args.rerun:
        ensure_container_stopped_removed()
        if args.rm_container: sys.exit()

    if args.stop_container:
        ensure_container_stopped_removed(remove_container=False)
        sys.exit()

    cprint('{0:.<70}'.format('PODMAN: image name'), 'yellow', end='')
    cprint(f' {podman_image_name}', 'cyan')

    ensure_image_exists()

    cprint('{0:.<70}'.format('PODMAN: container name'), 'yellow', end='')
    cprint(f' {podman_container_name}', 'cyan')

    ensure_container_exists_and_running()
    cprint('PODMAN: to login to the container run:', 'yellow')
    cprint(f'podman exec -it {podman_container_name} /bin/bash\n', 'green')
