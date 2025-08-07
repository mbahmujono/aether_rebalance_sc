import { ref } from 'vue'
import axios from 'axios'

type Token = { symbol: string; balance: number }
type ConvertedToken = Token & { usdValue: number | null }

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://127.0.0.1:5000'

export function usePriceConversion() {
  const convertedTokens = ref<ConvertedToken[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const convertAll = async (tokens: Token[]) => {
    isLoading.value = true
    error.value = null
    try {
      const { data } = await axios.post(`${API_BASE}/api/price-conversion`, { tokens })
      convertedTokens.value = data.data as ConvertedToken[]
    } catch (e) {
      console.error(e)
      error.value = 'Price conversion failed'
    } finally {
      isLoading.value = false
    }
  }

  return { convertedTokens, convertAll, isLoading, error }
}
