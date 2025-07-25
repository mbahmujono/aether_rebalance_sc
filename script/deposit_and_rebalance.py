from script.deposit import run_deposit_script
from script._setup_script import setup_script
from script.rebalance import rebalance, SIX_DECIMALS, EIGHTEEN_DECIMALS, get_price
import boa


def moccasin_main():
    usdc, weth, a_usdc, a_weth = setup_script()
    run_deposit_script(
        usdc, weth
    )  # Probably redundant and uneeded... but just in case.
    
    starting_usdc_balance = usdc.balanceOf(boa.env.eoa)
    starting_weth_balance = weth.balanceOf(boa.env.eoa)

    print(f"Wallet after deposit USDC balance: {starting_usdc_balance / 1e6} USDC")
    print(f"Wallet after deposit WETH balance: {starting_weth_balance / 1e18} WETH")
    
    rebalance(usdc, weth, a_usdc, a_weth)
    run_deposit_script(usdc, weth)

    a_usdc_balance = a_usdc.balanceOf(boa.env.eoa)
    a_weth_balance = a_weth.balanceOf(boa.env.eoa)
    
    print(f"Wallet after rebalance USDC balance: {starting_usdc_balance / 1e6} USDC")
    print(f"Wallet after rebalance WETH balance: {starting_weth_balance / 1e18} WETH")

    print(f"Current Aave USDC balance: {a_usdc_balance / SIX_DECIMALS} USDC")
    print(f"Current Aave WETH balance: {a_weth_balance / EIGHTEEN_DECIMALS} WETH")

    a_usdc_balance_normalized = a_usdc_balance / SIX_DECIMALS
    a_weth_balance_normalized = a_weth_balance / EIGHTEEN_DECIMALS

    usdc_value = a_usdc_balance_normalized * get_price("usdc_usd_price_feed")
    weth_value = a_weth_balance_normalized * get_price("eth_usd_price_feed")
    
    print(f"Current USDC value: ${usdc_value:.2f}")
    print(f"Current WETH value: ${weth_value:.2f}")

    total_value = usdc_value + weth_value
    print(f"Current percent allocation of USDC: {usdc_value / total_value * 100:.2f}%")
    print(f"Current percent allocation of WETH: {weth_value / total_value * 100:.2f}%")
