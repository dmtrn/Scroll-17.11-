from aiohttp import ClientSession
from abc import ABC, abstractmethod
from settings import LAYERSWAP_API_KEY, OKX_API_KEY, OKX_API_PASSPHRAS, OKX_API_SECRET, OKX_DEPOSIT_NETWORK


class DEX(ABC):
    @abstractmethod
    async def swap(self):
        pass


class CEX(ABC):
    def __init__(self, client):
        self.client = client

        #self.network_id = OKX_DEPOSIT_NETWORK
        self.api_key = OKX_API_KEY
        self.api_secret = OKX_API_SECRET
        self.passphras = OKX_API_PASSPHRAS

    @abstractmethod
    async def deposit(self):
        pass

    @abstractmethod
    async def withdraw(self):
        pass

    async def make_request(self, method:str = 'GET', url:str = None, data:str = None, params:dict = None,
                           headers:dict = None, module_name:str = 'Request'):

        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, data=data,
                                       params=params, proxy=self.client.proxy) as response:

                data = await response.json()
                if data['code'] != 0 and data['msg'] != '':
                    error = f"Error code: {data['code']} Msg: {data['msg']}"
                    raise RuntimeError(f"Bad request to OKX({module_name}): {error}")
                else:
                    #self.logger.success(f"{self.info} {module_name}")
                    return data['data']


class Aggregator(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    async def swap(self):
        pass

    async def make_request(self, method:str = 'GET', url:str = None, headers:dict = None, params: dict = None,
                           data:str = None, json:dict = None):

        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, data=data,
                                       params=params, json=json, proxy=self.client.proxy) as response:

                data = await response.json()
                if response.status == 200:
                    return data
                raise RuntimeError(f"Bad request to {self.__class__.__name__} API: {response.status}")


class Bridge(ABC):
    def __init__(self, client):
        self.client = client

        if self.__class__.__name__ == 'LayerSwap':
            self.headers = {
                'X-LS-APIKEY': f'{LAYERSWAP_API_KEY}',
                'Content-Type': 'application/json'
            }
        elif self.__class__.__name__ == 'Rhino':
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }

    @abstractmethod
    async def bridge(self, *args, **kwargs):
        pass

    async def make_request(self, method:str = 'GET', url:str = None, headers:dict = None, params: dict = None,
                           data:str = None, json:dict = None):

        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, data=data,
                                       params=params, json=json, proxy=self.client.proxy) as response:

                data = await response.json()
                if response.status in [200, 201]:
                    return data
                raise RuntimeError(f"Bad request to {self.__class__.__name__} API: {response.status}")


class Refuel(ABC):
    @abstractmethod
    async def refuel(self):
        pass


class Messenger(ABC):
    @abstractmethod
    async def send_message(self):
        pass


class Landing(ABC):
    @abstractmethod
    async def deposit(self):
        pass

    @abstractmethod
    async def withdraw(self):
        pass

    @abstractmethod
    async def enable_collateral(self):
        pass

    @abstractmethod
    async def disable_collateral(self):
        pass


class Minter(ABC):
    @abstractmethod
    async def mint(self):
        pass


class Creator(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    async def create(self):
        pass


class Blockchain(ABC):
    @abstractmethod
    async def deposit(self):
        pass

    @abstractmethod
    async def withdraw(self):
        pass

    @abstractmethod
    async def transfer_eth(self):
        pass

    @abstractmethod
    async def wrap_eth(self):
        pass

    @abstractmethod
    async def unwrap_eth(self):
        pass
