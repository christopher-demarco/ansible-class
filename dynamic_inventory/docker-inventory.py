#!/usr/bin/env python

import json
import subprocess

def get_running_containers():

    # Run `docker ps` with the correct arguments
    format = '{{.ID}},{{.Image}},{{.Names}}'
    p = subprocess.Popen(
        ['docker', 'ps', '--format', format],
        stdout=subprocess.PIPE
        )

    # Compose the output into a list of dictionaries
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

# Put our containers in a group
inventory = {'containers': {}}
inventory['containers']['hosts'] = [c['container'] for c in containers]

# Set the connection variable for the group
inventory['containers']['vars'] = {
    "ansible_connection": "docker"
    }

# And output it!
print json.dumps(inventory)
