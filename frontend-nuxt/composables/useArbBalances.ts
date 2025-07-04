import { ref, watchEffect } from 'vue'
import type { Address } from 'viem'
import { ethers } from 'ethers'
import type { Ref } from 'vue'

// Minimal ERC‑20 ABI
const erc20Abi = [
  'function balanceOf(address) view returns (uint256)',
  'function decimals() view returns (uint8)',
  'function symbol() view returns (string)'
]

// List token contracts you want to track
const TOKEN_LIST = [
  { address: '0xaf88d065e77c8cc2239327c5edb3a432268e5831', symbolOverride: 'USDC' },
  { address: '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1', symbolOverride: 'WETH' },
  { address: "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f", symbolOverride: 'WBTC' },
  { address: "0x1cff25B095cf6595afAbe35Dd7e5348666e57C11", symbolOverride: 'ETH' },
  // Add more token addresses here
]

interface TokenInfo {
  symbol: string
  balance: number
  usdValue?: number
}

export function useTokenBalances(
  userAddress: Ref<Address | undefined>,
  chainId: Ref<number | string | undefined>,
  infuraProjectId: string
) {
  const nativeBalance = ref<number | null>(null)
  const tokens = ref<TokenInfo[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  watchEffect(async () => {
    const addr = userAddress.value
    const id = chainId.value
    console.log(`Fetching balances for ${addr} on chain ${id}`)
    if (!addr || id !== 42161) return  // only Arbitrum in this example

    loading.value = true
    error.value = null

    try {
      const provider = new ethers.JsonRpcProvider(
        `https://arbitrum-mainnet.infura.io/v3/${infuraProjectId}`
      )
      const results: TokenInfo[] = []
      // Native balance
      const raw = await provider.getBalance(addr)
      nativeBalance.value = parseFloat(ethers.formatEther(raw))
      console.log(`Native balance for ${addr}: ${nativeBalance.value} ETH`)

      results.push({
        symbol: 'ETH', // or change if on other chains (e.g., 'MATIC')
        balance: nativeBalance.value || 0,
        // usdValue will be filled in later
      })
      // Fetch each token
      for (const token of TOKEN_LIST) {
        const contract = new ethers.Contract(token.address, erc20Abi, provider)
        const [balRaw, dec, sym] = await Promise.all([
          contract.balanceOf(addr),
          contract.decimals(),
          contract.symbol()
        ])
        const balanceRaw = ethers.formatUnits(balRaw, dec)
        const balance = parseFloat(balanceRaw)
        console.log(`Balance for ${sym} (${token.address}): ${balance}`)
        results.push({
          symbol: sym || token.symbolOverride || 'Unknown',
          balance,
          // usdValue: fetch via external API if you want
        })
      }
      tokens.value = results
    } catch (e: any) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  })

  return { nativeBalance, tokens, loading, error }
}
