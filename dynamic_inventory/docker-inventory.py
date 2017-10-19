#!/usr/bin/env python

import json
import subprocess

def get_running_containers():

    format = '{{.ID}},{{.Image}},{{.Names}}'
    p = subprocess.Popen(
        ['docker', 'ps', '--format', format],
        stdout=subprocess.PIPE
        )

    return [
        dict(
            zip(
                ('container', 'image', 'name'),
                line.split(',')
                )
            )
        for line in p.communicate()[0].rstrip().split('\n')
        ]

containers = get_running_containers()
inventory = {'containers': {}}
inventory['containers']['hosts'] = [c['container'] for c in containers]

inventory['containers']['vars'] = {
    "ansible_connection": "docker"
    }
print json.dumps(inventory)
