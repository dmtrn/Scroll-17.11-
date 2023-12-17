import random
import json

from termcolor import cprint
from config import WALLETS
from settings import (
    AUTO_ROUTES_MODULES_USING,
    CLASSIC_ROUTES_MODULES_USING,
    MAX_UNQ_CONTACTS,
    WITHDRAW_LP,
    TX_COUNT
)


def classic_routes_gen():
    with open('./data/wallets.json', 'w') as file:
        accounts_data = {}
        for num, private_key in enumerate(WALLETS, 1):
            data = classic_generate_route()
            account_data = {
                "current_step": 0,
                "route": data
            }
            accounts_data[private_key] = account_data
        json.dump(accounts_data, file, indent=4)
    cprint(f'\n✅ Successfully generated {len(accounts_data)} classic routes in data/wallets.json\n', 'light_blue')


def auto_routes_gen():
    with open('./data/wallets.json', 'w') as file:
        accounts_data = {}
        for num, private_key in enumerate(WALLETS, 1):
            data = auto_generate_route()
            account_data = {
                "current_step": 0,
                "route": data
            }
            accounts_data[private_key] = account_data
        json.dump(accounts_data, file, indent=4)
    cprint(f'\n✅ Successfully generated {len(accounts_data)} auto routes in data/wallets.json\n', 'light_blue')


def auto_generate_route():
    route = []
    bridge_choice = []

    if AUTO_ROUTES_MODULES_USING['okx_withdraw']:
        route.append(('okx_withdraw', 0, 1))

    if WITHDRAW_LP:
        route.extend(withdraw_liquidity_modules)

    while len(route) < random.randint(*TX_COUNT):
        mod = random.choice(available_modules)
        mod_name, mod_priority, mod_max_count = mod

        if mod_max_count != 0 and route.count(mod) == mod_max_count:
            continue
        if AUTO_ROUTES_MODULES_USING[mod_name]:
            if not MAX_UNQ_CONTACTS:
                route.append(mod)
            else:
                if mod in route and len(route) < sum(list(AUTO_ROUTES_MODULES_USING.values())) - 4:
                    continue
                route.append(mod)

    if AUTO_ROUTES_MODULES_USING['bridge_rhino']:
        bridge_choice.append(('bridge_rhino', 1, 1))
    if AUTO_ROUTES_MODULES_USING['bridge_layerswap']:
        bridge_choice.append(('bridge_layerswap', 1, 1))
    if AUTO_ROUTES_MODULES_USING['bridge_orbiter']:
        bridge_choice.append(('bridge_orbiter', 1, 1))
    if AUTO_ROUTES_MODULES_USING['bridge_scroll']:
        bridge_choice.append(('bridge_scroll', 1, 1))

    route.append(random.choice(bridge_choice))

    random.shuffle(route)

    data = sorted(route, key=lambda x: x[1])
    route_new = []
    for i in data:
        if i[0] in dependencies:
            route_new.append(i[0])
            route_new.append(dependencies[i[0]])
            continue
        route_new.append(i[0])

    return route_new


def classic_generate_route():
    route = []
    for i in CLASSIC_ROUTES_MODULES_USING:
        module = random.choice(i)
        if module is None:
            continue
        route.append(module)
    return route


available_modules = [
    # module name, priority, max_count
    ('okx_withdraw', 0, 1),
    ('add_liquidity_syncswap', 2, 1),
    ('deposit_layerbank', 2, 0),
    ('enable_collateral_layerbank', 2, 0),
    ('swap_izumi', 2, 0),
    ('swap_openocean', 2, 0),
    ('swap_syncswap', 2, 0),
    ('swap_scrollswap', 2, 0),
    ('wrap_eth', 2, 0),
    ('mint_zerius', 2, 0),
    ('deploy_contract', 1, 1),
    ('bridge_zerius', 3, 0),
    ('create_omnisea', 3, 0),
    ('create_safe', 3, 1),
    # ('mint_and_bridge_l2telegraph', 3, 0),
    ('refuel_merkly', 3, 0),
    ('send_message_dmail', 3, 0),
    # ('send_message_l2telegraph', 3, 0),
    ('transfer_eth', 3, 0),
    ('transfer_eth_to_myself', 3, 0),
    ('withdraw_scroll', 3, 0),
    ('okx_deposit', 4, 1),
    ('okx_collect_from_sub', 5, 1),
]

withdraw_liquidity_modules = [
    # ('withdraw_liquidity_spacefi', 3, 1),
    ('withdraw_liquidity_syncswap', 3, 1),
]

dependencies = {
    'deposit_layerbank': 'withdraw_layerbank',
    'enable_collateral_layerbank': 'disable_collateral_layerbank',
    'wrap_eth': 'unwrap_eth'
}
