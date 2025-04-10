#!/usr/bin/env python3

import argparse
import requests
import json
import os
import datetime
# import logging

# logging.basicConfig(level=logging.INFO)

class API():
    def __init__(self, server=None):
        self.server = server
        self.token_file = 'data/token.json'
        self.token = self.load_token()
        if not self.token or self.is_token_expired(self.token):
            self.token = self.create_token()
            self.save_token(self.token)
        self.token_id = self.token.get('id')

    def is_cached(self):
        cached = os.getenv('CACHED')
        if cached in ('TRUE', 'true', 'YES', 'yes', 'ON', 'on', 1):
            return True
        return False

    def is_verbose(self):
        cached = os.getenv('VERBOSE')
        if cached in ('TRUE', 'true', 'YES', 'yes', 'ON', 'on', 1):
            return True
        return False

    def is_token_expired(self, token):
        created_at = token.get('created_at')
        ttl = token.get('ttl')
        created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")
        created_at = created_at.replace(tzinfo=datetime.timezone.utc)
        expiration_time = created_at + datetime.timedelta(seconds=ttl-5)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        return current_time > expiration_time

    def load_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                data = json.load(file)
                return data.get('token')
        return None

    def save_token(self, token):
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        with open(self.token_file, 'w') as file:
            json.dump({'token': token}, file)

    def do_get(self, url, payload=None):
        if not payload:
            payload = dict()
        payload['cached'] = True if self.is_cached() else False
        data = json.dumps(payload)
        headers = {
           'Authorization': self.token_id,
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        if self.is_verbose():
            print(f"URL: {url}")
            print(f"HEADERS: {headers}")
            print(f"REQUEST BODY: {data}")
        response = requests.request("GET", url, headers=headers, data=data)
        print(response.text)

    def do_post(self, url, json_file=None):
        if not json_file:
            payload = {}
        else:
            with open(json_file, 'r') as ff:
                data = json.load(ff)
            payload = json.dumps(data)

        headers = {
           'Authorization': self.token_id,
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def do_patch(self, url, json_file):
        with open(json_file, 'r') as ff:
            data = json.load(ff)
        payload = json.dumps(data)
        headers = {
           'Authorization': self.token_id,
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("PATCH", url, headers=headers, data=payload)
        print(response.text)

    def do_delete(self, url):
        headers = {
           'Authorization': self.token_id,
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("DELETE", url, headers=headers)
        print(response.text)


    def create_token(self):
        url = f"http://{self.server}/api/v1/tokens"
        payload = json.dumps({
           "email": "cloud@astute-tec.com"
        })
        headers = {
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.content)
        token = {}
        token['id'] = data.get('token')
        token['created_at'] = data.get('created_at')
        token['ttl'] = data.get('ttl')
        return token

    def do_list_tokens(self):
        url = f"http://{self.server}/api/v1/tokens"
        payload = json.dumps(
            {
                "email":"cloud@astute-tec.com"
            })
        self.do_get(url, payload=payload)

    def do_add_platform(self, json_file):
        url = f"http://{self.server}/api/v1/platforms"
        with open(json_file, 'r') as ff:
            data = json.load(ff)
        payload = json.dumps(data)
        headers = {
           'Authorization': self.token_id,
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def do_update_platform(self, json_file):
        url = f"http://{self.server}/api/v1/platforms"
        self.do_patch(url, json_file)

    def do_ping_platform(self, platform_id):
        url = f"http://{self.server}/api/v1/platform/ping"
        payload = {
            "platform_id": platform_id
        }
        headers = {
           'Authorization': self.token_id,
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def do_delete_platform(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}"
        self.do_delete(url)

    def do_list_platforms(self):
        url = f"http://{self.server}/api/v1/platforms"
        headers = {
           'Authorization': self.token_id,
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)



    def do_list_clouds(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds"
        self.do_get(url)
    
    def do_list_volume_types(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/volume_types"
        self.do_get(url)

    def do_list_images(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/images"
        self.do_get(url)

    def do_get_image(self, platform_id, image_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/images/{image_id}"
        self.do_get(url)

    def do_list_sizes(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/sizes"
        self.do_get(url)

    def do_get_size(self, platform_id, size_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/sizes/{size_id}"
        self.do_get(url)

    def do_list_templates(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/templates"
        self.do_get(url)

    def do_get_template(self, platform_id, template_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/templates/{template_id}"
        self.do_get(url)

    def do_list_pf_networks(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/networks"
        self.do_get(url)

    def do_list_clusters(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clusters"
        self.do_get(url)

    def do_list_hosts(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/hosts"
        self.do_get(url)

    def do_list_machines(self, platform_id, cloud_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines"
        self.do_get(url)

    def do_create_machine(self, platform_id, cloud_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines"
        self.do_post(url, json_file)

    def do_create_machine_from_template(self, platform_id, cloud_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines-from-template"
        self.do_post(url, json_file)

    def do_get_machine(self, platform_id, cloud_id, machine_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines/{machine_id}"
        self.do_get(url)

    def do_get_machine_console(self, platform_id, cloud_id, machine_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines/{machine_id}/console"
        self.do_get(url)

    def do_list_volumes(self, platform_id, cloud_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/volumes"
        self.do_get(url)

    def do_get_volume(self, platform_id, cloud_id, volume_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/volumes/{volume_id}"
        self.do_get(url)

    def do_list_networks(self, platform_id, cloud_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/networks"
        self.do_get(url)

    def do_get_network(self, platform_id, cloud_id, network_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/networks/{network_id}"
        self.do_get(url)

    def do_machine_action(self, platform_id, cloud_id, machine_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines/{machine_id}"
        self.do_post(url, json_file)

    def do_template_action(self, platform_id, template_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/templates/{template_id}/action"
        self.do_post(url, json_file)

    def do_delete_machine(self, platform_id, cloud_id, machine_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines/{machine_id}"
        self.do_delete(url)

    def do_delete_template(self, platform_id, template_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/templates/{template_id}"
        self.do_delete(url)

    def do_list_security_groups(self, platform_id, cloud_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/security-groups"
        self.do_get(url)

    def do_sync_volume_type(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/volume_type/sync"
        self.do_post(url)

    def do_sync_cloud(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/cloud/sync"
        self.do_post(url)

    def do_sync_cluster(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/cluster/sync"
        self.do_post(url)

    def do_sync_image(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/image/sync"
        self.do_post(url)

    def do_sync_host(self, platform_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/host/sync"
        self.do_post(url, json_file)

    def do_sync_machine(self, platform_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/machine/sync"
        self.do_post(url, json_file)

    def do_sync_pf_network(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/network/sync"
        self.do_post(url)

    def do_sync_network(self, platform_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/network/sync"
        self.do_post(url, json_file=json_file)

    def do_sync_volume(self, platform_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/volume/sync"
        self.do_post(url, json_file)

    def do_sync_template(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/template/sync"
        self.do_post(url)

    def do_poll_image(self, platform_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/image/update_poller"
        self.do_post(url, json_file)

    def do_poll_template(self, platform_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/template/update_poller"
        self.do_post(url, json_file)

    def do_poll_host(self, platform_id, cluster_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clusters/{cluster_id}/update_poller"
        self.do_post(url, json_file)

    def do_poll_machine(self, platform_id, cloud_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/update_poller"
        self.do_post(url, json_file)

    def do_poll_volume(self, platform_id, cloud_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/update_volume_poller"
        self.do_post(url, json_file)


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', action='store', dest='server')
    parser.add_argument('-c', '--cached', action='store_true', help="Fetch data in cached mode(default:False)")
    parser.add_argument('-v', '--verbose', action='store_true')
    subparsers = parser.add_subparsers(dest='subcommand', required=True)

    parser_list_platforms = subparsers.add_parser('list-platforms')

    parser_list_tokens = subparsers.add_parser('list-tokens')

    parser_add_platform = subparsers.add_parser('add-platform')
    parser_add_platform.add_argument('json_file')

    parser_update_platform = subparsers.add_parser('update-platform')
    parser_update_platform.add_argument('json_file')

    parser_ping_platform = subparsers.add_parser('ping-platform')
    parser_ping_platform.add_argument('platform_id')

    parser_delete_platform = subparsers.add_parser('delete-platform')
    parser_delete_platform.add_argument('platform_id')

    parser_list_clouds = subparsers.add_parser('list-clouds')
    parser_list_clouds.add_argument('platform_id')

    parser_list_images = subparsers.add_parser('list-images')
    parser_list_images.add_argument('platform_id')

    parser_list_sizes = subparsers.add_parser('list-sizes')
    parser_list_sizes.add_argument('platform_id')

    parser_get_size = subparsers.add_parser('get-size')
    parser_get_size.add_argument('platform_id')
    parser_get_size.add_argument('size_id')

    parser_get_image = subparsers.add_parser('get-image')
    parser_get_image.add_argument('platform_id')
    parser_get_image.add_argument('image_id')

    parser_list_templates = subparsers.add_parser('list-templates')
    parser_list_templates.add_argument('platform_id')

    parser_get_template = subparsers.add_parser('get-template')
    parser_get_template.add_argument('platform_id')
    parser_get_template.add_argument('template_id')

    parser_list_clusters = subparsers.add_parser('list-clusters')
    parser_list_clusters.add_argument('platform_id')

    parser_list_hosts = subparsers.add_parser('list-hosts')
    parser_list_hosts.add_argument('platform_id')

    parser_list_machines = subparsers.add_parser('list-machines')
    parser_list_machines.add_argument('platform_id')
    parser_list_machines.add_argument('cloud_id')

    parser_create_machine = subparsers.add_parser('create-machine')
    parser_create_machine.add_argument('platform_id')
    parser_create_machine.add_argument('cloud_id')
    parser_create_machine.add_argument('json_file')

    parser_create_machine_from_templ = subparsers.add_parser('create-machine-from-template')
    parser_create_machine_from_templ.add_argument('platform_id')
    parser_create_machine_from_templ.add_argument('cloud_id')
    parser_create_machine_from_templ.add_argument('json_file')

    parser_get_machine = subparsers.add_parser('get-machine')
    parser_get_machine.add_argument('platform_id')
    parser_get_machine.add_argument('cloud_id')
    parser_get_machine.add_argument('machine_id')

    parser_delete_machine = subparsers.add_parser('delete-machine')
    parser_delete_machine.add_argument('platform_id')
    parser_delete_machine.add_argument('cloud_id')
    parser_delete_machine.add_argument('machine_id')

    parser_delete_template = subparsers.add_parser('delete-template')
    parser_delete_template.add_argument('platform_id')
    parser_delete_template.add_argument('template_id')

    parser_list_volume_types = subparsers.add_parser('list-volume-types')
    parser_list_volume_types.add_argument('platform_id')

    parser_list_pf_networks = subparsers.add_parser('list-pf-networks')
    parser_list_pf_networks.add_argument('platform_id')

    parser_list_volumes = subparsers.add_parser('list-volumes')
    parser_list_volumes.add_argument('platform_id')
    parser_list_volumes.add_argument('cloud_id')

    parser_get_volume = subparsers.add_parser('get-volume')
    parser_get_volume.add_argument('platform_id')
    parser_get_volume.add_argument('cloud_id')
    parser_get_volume.add_argument('volume_id')

    parser_list_networks = subparsers.add_parser('list-networks')
    parser_list_networks.add_argument('platform_id')
    parser_list_networks.add_argument('cloud_id')

    parser_get_network = subparsers.add_parser('get-network')
    parser_get_network.add_argument('platform_id')
    parser_get_network.add_argument('cloud_id')
    parser_get_network.add_argument('network_id')

    parser_machine_action = subparsers.add_parser('machine-action')
    parser_machine_action.add_argument('platform_id')
    parser_machine_action.add_argument('cloud_id')
    parser_machine_action.add_argument('machine_id')
    parser_machine_action.add_argument('json_file')

    parser_list_sgs = subparsers.add_parser('list-security-groups')
    parser_list_sgs.add_argument('platform_id')
    parser_list_sgs.add_argument('cloud_id')

    parser_sync_volume_type = subparsers.add_parser('sync-volume-type')
    parser_sync_volume_type.add_argument('platform_id')

    parser_sync_cloud = subparsers.add_parser('sync-cloud')
    parser_sync_cloud.add_argument('platform_id')

    parser_sync_cluster = subparsers.add_parser('sync-cluster')
    parser_sync_cluster.add_argument('platform_id')

    parser_sync_image = subparsers.add_parser('sync-image')
    parser_sync_image.add_argument('platform_id')

    parser_sync_size = subparsers.add_parser('sync-image')
    parser_sync_size.add_argument('platform_id')

    parser_sync_host = subparsers.add_parser('sync-host')
    parser_sync_host.add_argument('platform_id')
    parser_sync_host.add_argument('json_file')

    parser_sync_machine = subparsers.add_parser('sync-machine')
    parser_sync_machine.add_argument('platform_id')
    parser_sync_machine.add_argument('json_file')

    parser_sync_pf_network = subparsers.add_parser('sync-pf-network')
    parser_sync_pf_network.add_argument('platform_id')

    parser_sync_network = subparsers.add_parser('sync-network')
    parser_sync_network.add_argument('platform_id')
    parser_sync_network.add_argument('json_file')

    parser_sync_volume = subparsers.add_parser('sync-volume')
    parser_sync_volume.add_argument('platform_id')
    parser_sync_volume.add_argument('json_file')

    parser_sync_template = subparsers.add_parser('sync-template')
    parser_sync_template.add_argument('platform_id')

    parser_poll_image = subparsers.add_parser('poll-image')
    parser_poll_image.add_argument('platform_id')
    parser_poll_image.add_argument('json_file')

    parser_poll_template = subparsers.add_parser('poll-template')
    parser_poll_template.add_argument('platform_id')
    parser_poll_template.add_argument('json_file')

    parser_poll_host = subparsers.add_parser('poll-host')
    parser_poll_host.add_argument('platform_id')
    parser_poll_host.add_argument('cluster_id')
    parser_poll_host.add_argument('json_file')

    parser_poll_machine = subparsers.add_parser('poll-machine')
    parser_poll_machine.add_argument('platform_id')
    parser_poll_machine.add_argument('cloud_id')
    parser_poll_machine.add_argument('json_file')

    parser_poll_volume = subparsers.add_parser('poll-volume')
    parser_poll_volume.add_argument('platform_id')
    parser_poll_volume.add_argument('cloud_id')
    parser_poll_volume.add_argument('json_file')

    parser_template_action = subparsers.add_parser('template-action')
    parser_template_action.add_argument('platform_id') 
    parser_template_action.add_argument('template_id') 
    parser_template_action.add_argument('json_file') 

    args = parser.parse_args()
    return args

def run_command(args, method):
    if args.subcommand in ('list-platforms','list-tokens'):
        return method()
    elif args.subcommand in ('add-platform','update-platform'):
        return method(args.json_file)
    else:
        if args.subcommand in ('list-clouds','list-images','list-sizes','list-templates',
            'list-volume-types','list-pf-networks','ping-platform','delete-platform',
            'list-clusters','list-hosts'):
            return method(args.platform_id)
        elif args.subcommand in ('get-size'):
            return method(args.platform_id, args.size_id)
        elif args.subcommand in ('get-image'):
            return method(args.platform_id, args.image_id)
        elif args.subcommand in ('get-template', 'delete-template'):
            return method(args.platform_id, args.template_id)
        elif args.subcommand in ('sync-volume-type','sync-cloud','sync-cluster',
            'sync-pf-network','sync-image','sync-template'):
            return method(args.platform_id)
        elif args.subcommand in ('sync-host','sync-machine','sync-network','sync-volume',
            'poll-image','poll-template'):
            return method(args.platform_id, args.json_file)
        else:
            if args.subcommand in ('list-machines','list-volumes','list-networks',
                'list-security-groups'):
                return method(args.platform_id, args.cloud_id)
            elif args.subcommand in ('poll-host'):
                return method(args.platform_id, args.cluster_id, args.json_file)
            elif args.subcommand in ('create-machine','create-machine-from-template',
                'poll-machine','poll-volume'):
                return method(args.platform_id, args.cloud_id, args.json_file)
            elif args.subcommand in ('get-machine', 'delete-machine'):
                return method(args.platform_id, args.cloud_id, args.machine_id)
            elif args.subcommand == 'get-volume':
                return method(args.platform_id, args.cloud_id, args.volume_id)
            elif args.subcommand == 'get-network':
                return method(args.platform_id, args.cloud_id, args.network_id)
            elif args.subcommand == 'machine-action':
                return method(args.platform_id, args.cloud_id, args.machine_id, args.json_file)
            elif args.subcommand == 'template-action':
                return method(args.platform_id, args.template_id, args.json_file)
    return

def main():
    args = parse_argument()
    server = args.server or 'localhost'
    if args.cached:
        os.environ['CACHED'] = 'TRUE'
    if args.verbose:
        os.environ['VERBOSE'] = 'TRUE'
    api = API(server=server)
    method_name = f"do_{args.subcommand.replace('-', '_')}"
    if hasattr(api, method_name):
        method = getattr(api, method_name)
        run_command(args, method)
    else:
        print(f'unknown command: {args.subcommand}')

if __name__ == "__main__":
    main()
