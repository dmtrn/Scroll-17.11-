import json
import random
import asyncio
import functools
from config import WALLETS, OKX_WALLETS
from utils.networks import *
from web3 import AsyncWeb3, AsyncHTTPProvider
from termcolor import cprint
from settings import (
    MIN_SLEEP,
    MAX_SLEEP,
    SLEEP_TIME_RETRY,
    MAXIMUM_RETRY,
    GAS_CONTROL,
    MAXIMUM_GWEI,
    SLEEP_TIME_GAS
)


async def sleep(self, min_time=MIN_SLEEP, max_time=MAX_SLEEP):
    duration = random.randint(min_time, max_time)
    print()
    self.client.logger.info(f"{self.client.info} {self.__class__.__name__} | 💤 Sleeping for {duration} seconds.")

    await asyncio.sleep(duration)


def create_okx_withdrawal_list():
    okx_data = {}
    w3 = AsyncWeb3()
    if WALLETS and OKX_WALLETS:
        with open('./data/okx_withdraw_list.json', 'w') as file:
            for private_key, okx_wallet in zip(WALLETS, OKX_WALLETS):
                okx_data[w3.eth.account.from_key(private_key).address] = okx_wallet
            json.dump(okx_data, file, indent=4)
        cprint('✅ Successfully added and saved OKX wallets data', 'light_blue')
        cprint('⚠️ Check all OKX deposit wallets by yourself to avoid problems', 'light_yellow', attrs=["blink"])
    else:
        cprint('❌ Put your wallets into files, before running this function', 'light_red')


async def check_proxies_status(proxies: list):
    tasks = []
    for proxy in proxies:
        tasks.append(check_proxy_status(proxy))
    await asyncio.gather(*tasks)


async def check_proxy_status(proxy:str):
    try:
        w3 = AsyncWeb3(AsyncHTTPProvider(random.choice(ScrollRPC.rpc), request_kwargs={"proxy": f"http://{proxy}"}))
        if await w3.is_connected():
            cprint(f'✅ Proxy {proxy[proxy.find("@"):]} successfully connected to Scroll RPC', 'light_green')
            return True
        cprint(f"❌ Proxy: {proxy} can`t connect to Ethereum RPC", 'light_red')
        return False
    except Exception as error:
        cprint(f"❌ Bad proxy: {proxy} | Error: {error} ", 'red')
        return False


def repeater(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        attempts = 0
        class_name = self.__class__.__name__
        while True:
            try:
                return await func(self, *args, **kwargs)
            except Exception as error:

                await asyncio.sleep(1)
                self.client.logger.error(
                    f"{self.client.info} {class_name} | {error} | Try[{attempts + 1}/{MAXIMUM_RETRY + 1}]")
                await asyncio.sleep(1)

                attempts += 1
                if attempts > MAXIMUM_RETRY:
                    break

                await sleep(self, SLEEP_TIME_RETRY, SLEEP_TIME_RETRY)
        self.client.logger.error(f"{self.client.info} {class_name} | Tries are over, launching next module.")
    return wrapper


def gas_checker(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        if GAS_CONTROL:
            class_name = self.__class__.__name__
            await asyncio.sleep(1)
            print()
            self.client.logger.info(f"{self.client.info} {class_name} | Checking for gas price")
            w3 = AsyncWeb3(AsyncHTTPProvider(random.choice(Ethereum.rpc), request_kwargs=self.client.request_kwargs))
            while True:
                gas = round(AsyncWeb3.from_wei(await w3.eth.gas_price, 'gwei'), 3)
                if gas < MAXIMUM_GWEI:
                    await asyncio.sleep(1)
                    self.client.logger.success(f"{self.client.info} {class_name} | {gas} Gwei | Gas price is good")
                    await asyncio.sleep(1)
                    return await func(self, *args, **kwargs)
                else:
                    await asyncio.sleep(1)
                    self.client.logger.warning(
                        f"{self.client.info} {class_name} | {gas} Gwei | Gas is too high."
                        f" Next check in {SLEEP_TIME_GAS} second")
                    await asyncio.sleep(SLEEP_TIME_GAS)
        return await func(self, *args, **kwargs)
    return wrapper
