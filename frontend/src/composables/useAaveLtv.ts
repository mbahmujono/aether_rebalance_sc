import { ref, watch, type Ref } from 'vue'
import { createPublicClient, http } from 'viem'
import { arbitrum, mainnet, base } from 'viem/chains'
import { useChainId } from '@wagmi/vue'
import type { Address, Chain } from 'viem'

const UiPoolDataProviderAbi = [
  {
    inputs: [
      { internalType: 'address', name: 'provider', type: 'address' },
      { internalType: 'address', name: 'user', type: 'address' }
    ],
    name: 'getUserReservesData',
    outputs: [
      {
        components: [
          { internalType: 'address', name: 'underlyingAsset', type: 'address' },
          { internalType: 'uint256', name: 'scaledATokenBalance', type: 'uint256' },
          { internalType: 'uint256', name: 'stableBorrowRate', type: 'uint256' },
          { internalType: 'uint256', name: 'scaledVariableDebt', type: 'uint256' },
          { internalType: 'uint256', name: 'principalStableDebt', type: 'uint256' },
          { internalType: 'uint256', name: 'stableBorrowLastUpdateTimestamp', type: 'uint40' },
          { internalType: 'bool', name: 'usageAsCollateralEnabledOnUser', type: 'bool' }
        ],
        internalType: 'struct UserReserveData[]',
        name: '',
        type: 'tuple[]'
      },
      { internalType: 'uint256', name: 'totalCollateralBase', type: 'uint256' },
      { internalType: 'uint256', name: 'totalDebtBase', type: 'uint256' },
      { internalType: 'uint256', name: 'availableBorrowsBase', type: 'uint256' },
      { internalType: 'uint256', name: 'currentLiquidationThreshold', type: 'uint256' },
      { internalType: 'uint256', name: 'ltv', type: 'uint256' },
      { internalType: 'uint256', name: 'healthFactor', type: 'uint256' }
    ],
    stateMutability: 'view',
    type: 'function'
  }
]

// Map of supported chains
const AAVE_CONFIG: Record<number, {
  chain: Chain
  poolAddressesProvider: Address
  uiPoolDataProvider: Address
}> = {
  [arbitrum.id]: {
    chain: arbitrum,
    poolAddressesProvider: '0x8162f4E0cA53BcF4788efF3FbD29c4c2635927E2',
    uiPoolDataProvider: '0x1211851c2E70FaCf4fF63bEe11EfEA6173750F51'
  },
  // Add more if needed
  // [mainnet.id]: {...},
  // [base.id]: {...},
}

export function useAaveLtv(address: Ref<Address | undefined>) {
  const chainId = useChainId() // ✅ this is already a Ref<number>


  const ltv = ref<number | null>(null)
  const healthFactor = ref<number | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const fetchLtv = async () => {
    const addr = address.value
    const id = chainId.value

    if (!addr || !id || !AAVE_CONFIG[id]) return

    const { chain, uiPoolDataProvider, poolAddressesProvider } = AAVE_CONFIG[id]

    const publicClient = createPublicClient({
      chain,
      transport: http()
    })

    loading.value = true
    error.value = null

    try {
      const result = await publicClient.readContract({
        address: uiPoolDataProvider,
        abi: UiPoolDataProviderAbi,
        functionName: 'getUserReservesData',
        args: [poolAddressesProvider, addr]
      }) as [
        any[], // user reserves
        bigint, // totalCollateralBase
        bigint, // totalDebtBase
        bigint, // availableBorrowsBase
        bigint, // currentLiquidationThreshold
        bigint, // ltv
        bigint  // healthFactor
      ]

      ltv.value = Number(result[5]) / 10000
      healthFactor.value = Number(result[6]) / 1e18
    } catch (err) {
      error.value = err as Error
    } finally {
      loading.value = false
    }
  }

  // Refetch when address or chain changes
  watch([address, chainId], () => {
    if (address.value && chainId.value) fetchLtv()
  })

  return {
    ltv,
    healthFactor,
    loading,
    error,
    fetchLtv
  }
}

export type UseAaveLtvReturn = ReturnType<typeof useAaveLtv>
