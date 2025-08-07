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

    <!-- PortfolioBalance.vue (template section) -->
    <table v-if="converted.length" class="min-w-full divide-y divide-gray-200 text-sm">
      <thead class="bg-gray-50 font-medium">
        <tr>
          <th class="px-4 py-2 text-left">Token</th>
          <th class="px-4 py-2 text-right">Balance</th>
          <th class="px-4 py-2 text-right">USD&nbsp;Value</th>
        </tr>
      </thead>

      <tbody class="divide-y divide-gray-100">
        <tr v-for="token in converted" :key="token.symbol">
          <td class="px-4 py-2">{{ token.symbol }}</td>
          <td class="px-4 py-2 text-right">{{ token.balance }}</td>
          <!-- Use nullish-coalescing to guard against null -->
          <td class="px-4 py-2 text-right">
            {{ (token.usdValue ?? 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
          </td>
        </tr>
      </tbody>
    </table>


    <div v-if="loading">Loading...</div>
    <div v-if="error">{{ error }}</div>
  </div>
</section>
</template>
