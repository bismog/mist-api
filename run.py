import argparse
import requests
import json
import os
import datetime

class API():
    def __init__(self, server=None):
        self.server = server
        self.token_file = 'data/token.json'
        self.token = self.load_token()
        if not self.token or self.is_token_expired(self.token):
            self.token = self.get_token()
            self.save_token(self.token)
        self.token_id = self.token.get('id')

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
        with open(self.token_file, 'w') as file:
            json.dump({'token': token}, file)

    def get_token(self):
        url = f"http://{self.server}/api/v1/tokens"
        payload = json.dumps({
           "email": "cloud@astute-tec.com"
        })
        headers = {
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
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

    def do_add_platform(self, json_file):
        with open(json_file, 'r') as ff:
            data = json.load(ff)
        payload = json.dumps(data)
        url = f"http://{self.server}/api/v1/platforms"
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)


    def do_list_platforms(self):
        url = f"http://{self.server}/api/v1/platforms"
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)

    def do_list_clouds(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)
    
    def do_list_machines(self, platform_id, cloud_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_get_machine(self, platform_id, cloud_id, machine_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines/{machine_id}"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_list_volume_types(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/volume_types"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_list_images(self, platform_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/images"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_list_volumes(self, platform_id, cloud_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/volumes"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_get_volume(self, platform_id, cloud_id, volume_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/volumes/{volume_id}"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_list_networks(self, platform_id, cloud_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/networks"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_get_network(self, platform_id, cloud_id, network_id):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/networks/{network_id}"
        payload = json.dumps({"cached": False})
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

    def do_machine_action(self, platform_id, cloud_id, machine_id, json_file):
        url = f"http://{self.server}/api/v1/platforms/{platform_id}/clouds/{cloud_id}/machines/{machine_id}"
        with open(json_file, 'r') as ff:
            data = json.load(ff)
        payload = json.dumps(data)
        # payload = json.dumps({
        #    "action": "start"
        # })
        headers = {
           'Authorization': self.token_id,
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': self.server,
           'Connection': 'keep-alive',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', action='store', dest='server')
    subparsers = parser.add_subparsers(dest='subcommand', required=True)

    parser_list_platforms = subparsers.add_parser('list-platforms')

    parser_add_platform = subparsers.add_parser('add-platform')
    parser_add_platform.add_argument('json_file')

    parser_list_clouds = subparsers.add_parser('list-clouds')
    parser_list_clouds.add_argument('platform_id')

    parser_list_machines = subparsers.add_parser('list-machines')
    parser_list_machines.add_argument('platform_id')
    parser_list_machines.add_argument('cloud_id')

    parser_get_machine = subparsers.add_parser('get-machine')
    parser_get_machine.add_argument('platform_id')
    parser_get_machine.add_argument('cloud_id')
    parser_get_machine.add_argument('machine_id')

    parser_list_volume_types = subparsers.add_parser('list-volume-types')
    parser_list_volume_types.add_argument('platform_id')

    parser_list_volumes = subparsers.add_parser('list-volumes')
    parser_list_volumes.add_argument('platform_id')
    parser_list_volumes.add_argument('cloud_id')

    parser_get_volume = subparsers.add_parser('get-volume')
    parser_get_volume.add_argument('platform_id')
    parser_get_volume.add_argument('cloud_id')
    parser_get_volume.add_argument('volume_id')

    parser_list_images = subparsers.add_parser('list-images')
    parser_list_images.add_argument('platform_id')

    parser_list_networks = subparsers.add_parser('list-networks')
    parser_list_networks.add_argument('platform_id')
    parser_list_networks.add_argument('cloud_id')

    parser_get_network = subparsers.add_parser('get-network')
    parser_get_network.add_argument('platform_id')
    parser_get_network.add_argument('cloud_id')
    parser_get_network.add_argument('network_id')

    parser_get_network = subparsers.add_parser('machine-action')
    parser_get_network.add_argument('platform_id')
    parser_get_network.add_argument('cloud_id')
    parser_get_network.add_argument('machine_id')
    parser_get_network.add_argument('json_file')

    args = parser.parse_args()
    return args

def run_command(args, method):
    if args.subcommand == 'list-platforms':
        return method()
    elif args.subcommand == 'add-platform':
        json_file = args.json_file
        return method(json_file)
    else:
        platform_id = args.platform_id
        if args.subcommand in ('list-clouds', 'list-images', 'list-volume-types'):
            return method(platform_id)
        else:
            cloud_id = args.cloud_id
            if args.subcommand in ('list-machines', 'list-volumes', 'list-networks'):
                return method(platform_id, cloud_id)
            elif args.subcommand == 'get-machine':
                machine_id = args.machine_id
                return method(platform_id, cloud_id, machine_id)
            elif args.subcommand == 'get-volume':
                volume_id = args.volume_id
                return method(platform_id, cloud_id, volume_id)
            elif args.subcommand == 'get-network':
                network_id = args.network_id
                return method(platform_id, cloud_id, network_id)
            elif args.subcommand == 'machine-action':
                machine_id = args.machine_id
                json_file = args.json_file
                return method(platform_id, cloud_id, machine_id, json_file)
    return

def main():
    args = parse_argument()
    server = args.server or 'localhost'
    api = API(server=server)
    method_name = f"do_{args.subcommand.replace('-', '_')}"
    if hasattr(api, method_name):
        method = getattr(api, method_name)
        run_command(args, method)
    else:
        print(f'unknown command: {args.subcommand}')

if __name__ == "__main__":
    main()
