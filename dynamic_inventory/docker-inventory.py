#!/usr/bin/env python

import argparse
import json
import subprocess

def get_running_containers():

    # Run `docker ps` with the correct arguments
    format = '{{.ID}};{{.Image}};{{.Names}};{{.Labels}}'
    p = subprocess.Popen(
        ['docker', 'ps', '--format', format],
        stdout=subprocess.PIPE
        )

    # Compose the output into a list of dictionaries
    containers =  [
        dict(
            zip(
                ('container', 'image', 'name', 'labels'),
                line.split(';')
                )
            )
        for line in p.communicate()[0].rstrip().split('\n')
    ]
    for c in containers:
        c['labels'] = parse_labels(c['labels'])
    return containers


def parse_labels(labels):
    return dict( [ l.split('=') for l in labels.split(',') ] )


if __name__ == '__main__':

    # Process arguments
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='List all groups')
    group.add_argument('--host', type=str, help='Limit to only one host')
    args = p.parse_args()

    containers = get_running_containers()

    # Put our containers in a top-level group
    inventory = {'containers': {}}
    inventory['containers']['hosts'] = [c['name'] for c in containers]


    # Set the connection variable for everything
    inventory['containers']['vars'] = {
        'ansible_connection': 'docker'
        }


    # Make groups based on labels
    for c in containers:
        group = c['labels'].get('group')
        if group in inventory:
            inventory[group]['hosts'].append(c['name'])
        else:
            inventory[group] = {'hosts': [c['name']]}
    
    
    # Set per-host vars based on labels
    for c in containers:
        for k, v in c['labels'].items():
            if k.startswith('ansible'):
                group = c['name']
                if group in inventory:
                    inventory[group]['vars'][k] = v
                else:
                    inventory[group] = {'hosts': [group], 'vars': {k: v}}

    # Output
    if args.list:
        print json.dumps(inventory)
    else:
        vars_dict = {}
        for d in [
                v.get('vars')
                  for k, v in inventory.items()
                if args.host in v.get('hosts') and v.get('vars')
                ]:
            vars_dict.update(d)
        print json.dumps(vars_dict)
