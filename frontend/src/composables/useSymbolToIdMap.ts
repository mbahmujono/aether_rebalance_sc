import { ref } from 'vue'
import axios from 'axios'

const API_KEY = import.meta.env.VITE_CMC_API_KEY

type SymbolIdMap = Record<string, number>

export function useSymbolToIdMap() {
  const symbolIdMap = ref<SymbolIdMap>({})
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchSymbolIdMap = async () => {
    isLoading.value = true
    error.value = null

    try {
      const { data } = await axios.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/map', {
        headers: {
          'X-CMC_PRO_API_KEY': API_KEY,
          'Accept': 'application/json'
        }
      })

      const mapping: SymbolIdMap = {}
      for (const item of data.data) {
        if (!mapping[item.symbol]) {
          mapping[item.symbol] = item.id // only map first match
        }
      }

      symbolIdMap.value = mapping

    } catch (err: any) {
      error.value = err.response?.data?.status?.error_message || 'Failed to fetch symbol-ID map'
    } finally {
      isLoading.value = false
    }
  }

  const getId = (symbol: string): number | undefined => {
    return symbolIdMap.value[symbol.toUpperCase()]
  }

  return {
    symbolIdMap,
    getId,
    fetchSymbolIdMap,
    isLoading,
    error
  }
}
