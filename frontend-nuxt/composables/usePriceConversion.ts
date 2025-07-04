import { ref } from 'vue'
import axios from 'axios'
import { useSymbolToIdMap } from './useSymbolToIdMap'

type Token = {
  symbol: string
  balance: number
}

type ConvertedToken = Token & {
  usdValue: number | null
}

export function usePriceConversion() {
  const convertedTokens = ref<ConvertedToken[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const convertAll = async (tokens: Token[]) => {
    isLoading.value = true
    error.value = null

    const results: ConvertedToken[] = []
    const { fetchSymbolIdMap, getId } = useSymbolToIdMap()
    await fetchSymbolIdMap() // Ensure we have the symbol-ID map ready

    for (const token of tokens) {
      try {
        const tokenId = getId(token.symbol)
        const { data } = await axios.get('https://pro-api.coinmarketcap.com/v2/tools/price-conversion', {
          headers: {
            'X-CMC_PRO_API_KEY': import.meta.env.VITE_CMC_API_KEY,
            'Accept': 'application/json'
          },
          params: {
            tokenId,
            amount: token.balance,
            convert: 'USD'
          }
        })

        const quote = data.data.quote
        results.push({
          symbol: token.symbol,
          balance: token.balance,
          usdValue: quote.USD?.price ?? null
        })

      } catch (err: any) {
        console.error(`Failed to convert ${token.symbol}`, err)
        results.push({
          symbol: token.symbol,
          balance: token.balance,
          usdValue: null
        })
      }
    }

    convertedTokens.value = results
    isLoading.value = false
  }

  return {
    convertedTokens,
    convertAll,
    isLoading,
    error
  }
}
