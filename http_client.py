#!/usr/bin/env python
from aiohttp import ClientSession
import asyncio
import logging

class HTTP_client:
    def __init__(self):
        logging.debug('Initialized HTTP_Client')
        self.session = ClientSession()

    async def get_request(self, url, headers={}):
        logging.debug('Doing request to: ' + url + ' using headers: ' + str(headers) + ' and token: ' + token)
        async with self.session.get(url, headers=headers) as response:
            response = await response.text()
            logging.debug("Response from request to url: " + response)
