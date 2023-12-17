from modules import Aggregator
from utils.tools import gas_checker, repeater
from settings import SLIPPAGE_PERCENT
from config import OPENOCEAN_CONTRACT, SCROLL_TOKENS, ETH_MASK, HELP_SOFTWARE


class OpenOcean(Aggregator):
    async def build_swap_transaction(self, from_token_address: str, to_token_address: str, amount: float):

        url = f'https://open-api.openocean.finance/v3/{self.client.chain_id}/swap_quote'

        params = {
            'chain': self.client.chain_id,
            'inTokenAddress': from_token_address,
            'outTokenAddress': to_token_address,
            'amount': amount,
            'gasPrice': str(self.client.w3.from_wei(await self.client.w3.eth.gas_price, 'gwei')),
            'slippage': SLIPPAGE_PERCENT,
            'account': self.client.address
        } | {'referrer': '0x000000a679C2FB345dDEfbaE3c42beE92c0Fb7A5', 'referrerFee': 1} if HELP_SOFTWARE else {}

        return await self.make_request(url=url, params=params)

    @repeater
    @gas_checker
    async def swap(self, help_add_liquidity:bool = False, amount_to_help:int = 0):

        from_token_name, to_token_name, amount, amount_in_wei = await self.client.get_auto_amount()

        if help_add_liquidity:
            to_token_name = 'ETH'
            decimals = 6
            eth_price = await self.client.get_token_price('ethereum')

            amount = round(amount_to_help * eth_price, 4)
            amount_in_wei = int(amount * 10 ** decimals)

        self.client.logger.info(
            f'{self.client.info} OpenOcean | Swap on OpenOcean: {amount} {from_token_name} -> {to_token_name}')

        from_token_address = ETH_MASK if from_token_name == "ETH" else SCROLL_TOKENS[from_token_name]
        to_token_address = ETH_MASK if to_token_name == "ETH" else SCROLL_TOKENS[to_token_name]

        swap_quote_data = await self.build_swap_transaction(from_token_address, to_token_address, amount)

        if from_token_address != ETH_MASK:
            await self.client.check_for_approved(from_token_address, OPENOCEAN_CONTRACT["router"], amount_in_wei)

        tx_params = (await self.client.prepare_transaction()) | {
            "to": swap_quote_data["data"]["to"],
            "data": swap_quote_data["data"]["data"],
            "value": int(swap_quote_data["data"]["value"])
        }

        tx_hash = await self.client.send_transaction(tx_params)

        await self.client.verify_transaction(tx_hash)
