import boa
from moccasin.config import get_active_network, Network
from boa.contracts.abi.abi_contract import ABIContract
from typing import Tuple

STARTING_ETH_BALANCE = int(1000e18)
STARTING_USDC_BALANCE = int(1000e6)
STARTING_WETH_BALANCE = int(13.5e18)


def _add_eth_balance():
    boa.env.set_balance(boa.env.eoa, STARTING_ETH_BALANCE)
    print(f"Added {STARTING_ETH_BALANCE} wei to {boa.env.eoa}")

def _add_token_balance(usdc: ABIContract, weth: ABIContract, active_network: Network):
    my_address = boa.env.eoa
    print(f'wallet address: {my_address}')
    print(f"Adding {STARTING_USDC_BALANCE} USDC and {STARTING_WETH_BALANCE} WETH to {my_address}")
    # Ensure the USDC contract is set up correctly
    with boa.env.prank(usdc.owner()):
        usdc.updateMasterMinter(my_address)
    usdc.configureMinter(my_address, STARTING_USDC_BALANCE)
    usdc.mint(my_address, STARTING_USDC_BALANCE)
    print(f"Added {STARTING_USDC_BALANCE} USDC to {my_address}")
    
    #deposit weth
    weth.deposit(value=STARTING_WETH_BALANCE)
    print(f"Deposited {STARTING_WETH_BALANCE} WETH to {my_address}")

def setup_script() -> Tuple[ABIContract, ABIContract, ABIContract, ABIContract]:
    active_network = get_active_network()
    print(f"Active network: {active_network.name}")
    
    
    usdc = active_network.manifest_named("usdc")
    weth = active_network.manifest_named("weth")
    print(f"USDC contract address: {usdc.address}")
    print(f"WETH contract address: {weth.address}")

    aave_protocol_data_provider = active_network.manifest_named(
        "aave_protocol_data_provider"
    )

    if active_network.is_local_or_forked_network():
        print("Setting up local network with initial balances...")
        _add_eth_balance()
        _add_token_balance(usdc, weth, active_network)
    
    print("checking starting balances...")
    starting_usdc_balance = usdc.balanceOf(boa.env.eoa)
    starting_weth_balance = weth.balanceOf(boa.env.eoa)

    print(f"Starting USDC balance: {starting_usdc_balance}")
    print(f"Starting WETH balance: {starting_weth_balance}")
    
    print("Getting atokens, this may take a while...")
    a_tokens = aave_protocol_data_provider.getAllATokens()
    a_usdc = None
    a_weth = None
    print("Fetching aTokens... done")
    
    token_prefix = "aEth" if active_network.chain_id == 1 else "aArb"
    for a_token in a_tokens:
        if a_token[0] == f"{token_prefix}USDC":
            print(f"Found aETHUSDC/aArbUSDC at {a_token[1]}")
            a_usdc = active_network.manifest_named("usdc", address=a_token[1])
        if a_token[0] == f"{token_prefix}WETH":
            print(f"Found aETHWETH/aArbWETH at {a_token[1]}")
            a_weth = active_network.manifest_named("usdc", address=a_token[1])
            
    starting_usdc_balance = usdc.balanceOf(boa.env.eoa)
    starting_weth_balance = weth.balanceOf(boa.env.eoa)

    print(f"Starting USDC balance: {starting_usdc_balance / 1e6} USDC")
    print(f"Starting WETH balance: {starting_weth_balance / 1e18} WETH")
    print(f"Starting aUSDC balance: {a_usdc.balanceOf(boa.env.eoa)}")
    print(f"Starting aWETH balance: {a_weth.balanceOf(boa.env.eoa)}")
    
    return usdc, weth, a_usdc, a_weth
    
def moccasin_main():
    """
    This function is called by Moccasin to set up the local environment.
    It initializes the balances for the EOA and returns the contract instances.
    """
    setup_script()
    
    # Return dummy contract instances for compatibility
    return (None, None, None, None)