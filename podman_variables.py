#!/usr/bin/python3

import os


cur_dir                 = os.path.dirname(os.path.realpath(__file__))

image_name              = 'cemu_build_env'
container_name          = 'cemu_builder'
container_hostname      = 'cemu_builder'
container_script        = '/root/scripts/01-build.cemu.sh'

scripts_dir_host        = f'{cur_dir}/build.scripts'
scripts_dir_container   = '/root/scripts'
output_dir_host         = f'{cur_dir}/output'
output_dir_container    = '/output'

# used in debug output
podman_vol_str          = f'-v {scripts_dir_host}:{scripts_dir_container} -v {output_dir_host}:{output_dir_container}'

# ensure bind mounted directories have the container_file_t label set
mount_dirs_selinux = [scripts_dir_host, output_dir_host]

bind_volumes = []
bind_volumes.append({'source': f'{scripts_dir_host}', 'target': f'{scripts_dir_container}', 'type': 'bind'})
bind_volumes.append({'source': f'{output_dir_host}', 'target': f'{output_dir_container}', 'type': 'bind'})
