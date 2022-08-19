# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
from random import randrange
import time
import threading
import socket
import sys
import traceback

HOSTNAME = socket.gethostname()

URL_SOURCE = 'https://polygon-rpc.com/'


def get_current_time():
    return str(datetime.now())


def fetch_jsonrpc_api(url, method, request_data):
    result = "No Value"
    headers = {'Content-Type': 'application/json'}

    r = ""
    tag = "[fetch_jsonrpc_api-{}-{}]".format(url, method)
    try:
        r = requests.post(url, data=json.dumps(request_data), headers=headers, timeout=30)
        data = json.loads(r.text)
        if 'error' in data:
            print "[{}] [{}] [{}] data is {}".format(
                get_current_time(), HOSTNAME, tag, data
            )
            return None

        result = data['result']

    except requests.exceptions.HTTPError as e:
        msg = "[{}] [{}] [{}] got requests.exceptions.HTTPError: {}".format(
            get_current_time(), HOSTNAME, tag, e
        )
        print msg
        send_alarm_to_author(msg)
    except requests.exceptions.RequestException as e:
        msg = "[{}] [{}] [{}] got requests.exceptions.RequestException: {}".format(
            get_current_time(), HOSTNAME, tag, e
        )
        print msg
        send_alarm_to_author(msg)
    except Exception as e:
        if r:
            msg = "[{}] [{}] [{}] exception, r.text is: {}, error is {}".format(
                get_current_time(), HOSTNAME, tag, r.text, e
            )
        else:
            msg = "[{}] [{}] [{}] exception, error is {}".format(
                get_current_time(), HOSTNAME, tag, e
            )
        print msg
        traceback.print_exc()
        send_alarm_to_author(msg)

    return result


def eth_getLogs(url, from_block, to_block):
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getLogs",
        "params": [
            {
                "address": "0x0000000000000000000000000000000000001010",
                "fromBlock": hex(from_block),
                "toBlock": hex(to_block),
                "topics": [
                    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
                ]
            }
        ],
        "id": 2547338
    }

    return fetch_jsonrpc_api(url, 'eth_gasPrice', data)


if __name__ == '__main__':
    delta = 2000
    from_block = start = 15341653
    to_block = end = 15381034

    total_count = 0
    total_value = 0
    while from_block <= end:
        if from_block + delta <= end:
            to_block = from_block + delta
        else:
            to_block = end

        data = eth_getLogs(URL_SOURCE, from_block, to_block)

        print "\n====[from={}, {}] [to={}, {}]====".format(from_block, hex(from_block), to_block, hex(to_block))

        count = 0
        value = 0
        for log in data:
            count += 1
            value += int(log['data'], 16)

        total_count += count
        total_value += value
        print "count: {}, value: {}".format(count, value)
        print "total_count: {}, total_value: {}".format(total_count, total_value)
        from_block = to_block + 1




