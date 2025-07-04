<script setup lang="ts">
import { reactive, toRefs } from 'vue'
import { useAppKitAccount, useAppKitNetwork } from '@reown/appkit/vue'
import { useTokenBalances } from '../composables/useArbBalances'
import { usePriceConversion } from '../composables/usePriceConversion'
import type { Address } from 'viem'

const account = useAppKitAccount()
const network = useAppKitNetwork()
const { address, isConnected } = toRefs(account.value)
const { chainId } = toRefs(network.value)
console.log('Account address:', address)
console.log('Network:', chainId)

const infuraId = import.meta.env.VITE_INFURA_ID
const { tokens } = useTokenBalances(address, chainId, infuraId)

const { convertedTokens: converted, convertAll, isLoading: loading, error } = usePriceConversion()

const fetchConversions = () => {
  convertAll(tokens.value)
}

</script>

<template>
<section>
  <div v-if="isConnected">
    <h3>Native Balance: {{ tokens[0].balance }} ETH</h3>
    <div v-if="loading">Loading token balances…</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <ul v-else>
      <li v-for="t in tokens" :key="t.symbol">
        {{ t.symbol }}: {{ t.balance }}
      </li>
    </ul>
  </div>
</section>
<section>
  <div>
    <button @click="fetchConversions">Convert to USD</button>

    <ul v-if="converted.length">
      <li v-for="token in converted" :key="token.symbol">
        {{ token.symbol }}: {{ token.balance }} → USD {{ token.usdValue }}
      </li>
    </ul>

    <div v-if="loading">Loading...</div>
    <div v-if="error">{{ error }}</div>
  </div>
</section>
</template>
