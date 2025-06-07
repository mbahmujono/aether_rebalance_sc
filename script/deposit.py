import boa
from boa.contracts.abi.abi_contract import ABIContract
from moccasin.config import get_active_network
from script._setup_script import setup_script
from moccasin.boa_tools import VyperContract

REFERRAL_CODE = 0

# Ini kode untuk deposit ke aave


def deposit_into_aave(
    pool_contract: ABIContract, token: VyperContract, amount: int
) -> int:
    active_network = get_active_network()
    allowed_amount = token.allowance(boa.env.eoa, pool_contract.address)
    if allowed_amount < amount:
        token.approve(pool_contract.address, amount)
    print(f"Depositing {token.name()} into Aave contract {pool_contract.address}")
    if active_network.chain_id == 1:  # Ethereum Mainnet
        print("Ethereum mainnet detected, using default supply method...")
        pool_contract.supply(token.address, amount, boa.env.eoa, REFERRAL_CODE)
    else: # L2 networks like Arbitrum
        print("L2 network detected, using L2Pool supply method...")
        l2_pool_contract = active_network.manifest_named("l2_pool", address=pool_contract.address)
        deposit_into_aave_l2(l2_pool_contract, pool_contract, token, amount)

def deposit_into_aave_l2(
    l2_pool_contract: ABIContract, 
    pool_contract: ABIContract,
    token: VyperContract,
    amount: int
):
    # Check allowance and approve if needed
    allowed_amount = token.allowance(boa.env.eoa, pool_contract.address)
    if allowed_amount < amount:
        token.approve(pool_contract.address, amount)
    
    # Dynamically fetch the asset ID (index) from the reserve data
    reserve_data = pool_contract.getReserveData(token.address)
    asset_id = reserve_data.id
    print(f"Fetched assetId from reserve data: {asset_id}")

    print(f"Preparing to deposit {token.name()} using L2Pool (assetId: {asset_id})...")

    # Shorten amount to uint128 to match L2Pool requirements
    shortened_amount = amount & ((1 << 128) - 1)

    # Manually encode calldata for L2Pool.supply
    referral_code = 0
    packed_data = asset_id | (shortened_amount << 16) | (referral_code << 144)
    encoded_args = packed_data.to_bytes(32, byteorder="big")
    
    print(f"Encoded calldata: {encoded_args.hex()}")

    # Call supply on L2Pool with manually packed calldata
    l2_pool_contract.supply(encoded_args)
    print(f"Deposited {amount / (1e6 if token.decimals() == 6 else 1e18)} {token.symbol()} using L2Pool.")


def run_deposit_script(usdc, weth):
    active_network = get_active_network()
    print("Connecting to Aave V3 pool...")
    aavev3_pool_address_provider = active_network.manifest_named(
        "aavev3_pool_address_provider"
    )
    pool_address: str = aavev3_pool_address_provider.getPool()
    pool_contract = active_network.manifest_named("pool", address=pool_address)
    # Deposit all USDC
    print(f"Using Aave V3 pool contract at {pool_contract.address}")
    print(f"Depositing ALL USDC into Aave V3 pool {pool_contract.address}...")
    usdc_balance = usdc.balanceOf(boa.env.eoa)
    if usdc_balance > 0:
        deposit_into_aave(pool_contract, usdc, usdc_balance)
        print(f"Deposited {usdc_balance / 1e6} USDC into Aave V3 pool.")
        
    # Deposit all WETH
    print(f"Depositing ALL WETH into Aave V3 pool {pool_contract.address}...")
    weth_balance = weth.balanceOf(boa.env.eoa)
    if weth_balance > 0:
        deposit_into_aave(pool_contract, weth, weth_balance)
        print(f"Deposited {weth_balance / 1e18} WETH into Aave V3 pool.")

    (
        totalCollateralBase,
        totalDebtBase,
        availableBorrowsBase,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = pool_contract.getUserAccountData(boa.env.eoa)
    print(f"""User account data:
        totalCollateralBase: {totalCollateralBase}
        totalDebtBase: {totalDebtBase}
        availableBorrowsBase: {availableBorrowsBase}
        currentLiquidationThreshold: {currentLiquidationThreshold}
        ltv: {ltv}
        healthFactor: {healthFactor}
          """)


def moccasin_main():
    usdc, weth, _, _ = setup_script()
    run_deposit_script(usdc, weth)
