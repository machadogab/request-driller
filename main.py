#!/usr/bin/env python

import logging
import optparse
import uvloop
import asyncio
from http_client import HTTP_client

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
## TODO:
## - Parse certificates and use them for MTLS
## - Parse files containing tokens and params and urls
## - add options on how to split the usage of tokens and certificates
## - add option to parse a config json file containing multiple requests and their respective configurations
parser = optparse.OptionParser()
parser.add_option('-H', '--headers', action="append", dest="headers", help="headers to be added to the requests")
parser.add_option('--token', action="store", dest="token", help="a valid token, or a path to a file containg one token per line")
parser.add_option('--certificate', action="store", dest="cert", help="path to the certificate for mtls or for a file containing a path per line")
parser.add_option('-d', '--debug', action="store_true", dest="debug", help="Debug flag", default=False)
parser.add_option('--url', action="store", dest="url", help="Target url or path to a file containg one url per line")
parser.add_option('--urlparams', action="append", dest="url_params", help="If you want to target a url with multiple id, eg: www.example.com/user/1, you can use this with /user/1, /user/2")

options, args = parser.parse_args()

def usage():
    print("Options:")
    print("  -H, --headers \t custom headers for the requests, eg: -H \"X-header: X-value\"")
    print("  -T, --token \t\t token to be used doing the requests or file containing one token per line, eg: -T \"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9adQssw5c\"")
    print("  --certificate \t path to certificate, eg: --certificate \"~/dev/cert.pem\"")
    print("  --url \t\t target url to the requests, or file containg one url per line, eg: --url \"www.example.com\"")
    print("  --urlparams \t\t If you want to target a url with multiple id, eg: www.example.com/user/1, you can use this with /user/1, /user/2")
    print("  --d \t\t\t debug flag, default is false")
    print()
    print()
    print("Usage: python main.py --url example.com -H \"X-header: X-value\" --urlparam /user/321 --token 123321312312")
if options.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if not options.url:
    usage()
    exit()

def parse_headers(headers = []):
    parsed_headers = {}
    for header in headers:
        values = header.split(':')
        parsed_headers[values[0]] = values[1]
    return parsed_headers

if options.headers:
    headers = parse_headers(options.headers)
else:
    headers = {}

if options.token:
    headers["Authorization"] = options.token

async def run():
    client = HTTP_client()
    tasks = []

    if options.url_params:
        for params in range(200000):
                task = asyncio.ensure_future(client.get_request(options.url, headers=headers))
                tasks.append(task)
    else:
        task = asyncio.ensure_future(client.get_request(options.url, headers=headers))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run())
loop.run_until_complete(future)
