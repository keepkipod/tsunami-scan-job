#!/usr/bin/env python3

from redis import Redis
from os import environ
import yaml
import argparse


QUEUE = 'scan-queue'


def get_parser():
    parser = argparse.ArgumentParser(description='Feed redis queue with list of ips')
    parser.add_argument('-f', '--file-path',
                        required=False,
                        dest='path',
                        default='ips.yaml',
                        help='Specify file path containing ip addresses to scan. Default=ips.yaml')
    return parser


def push(*values):
    redis_connection.rpush(QUEUE, *values)


args = get_parser().parse_args()
args_dict = vars(args)

with open(args_dict["path"], "r") as stream:
    try:
        ip_list = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        
if "NODE_IP" in environ and "NODE_PORT":
    redis_connection = Redis(host=environ.get('NODE_IP'), port=environ.get('NODE_PORT'), db=0)
else:
    print("Missing ENV VARs NODE_PORT & NODE_PORT")

for ip in ip_list['targets']:
    print(f'{ip} enqueuing')
    push(ip)
print('Done enqueue all ip addresses')
