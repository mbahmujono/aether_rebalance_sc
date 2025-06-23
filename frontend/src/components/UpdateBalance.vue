<template>
  <section>
    <h2>Account Info</h2>
    <pre>
Address: {{ address }}
Connected: {{ isConnected }}
Status: {{ status }}
    </pre>

    <h2>Balance</h2>
    <div v-if="isConnected">
      <p>Native Balance: {{ balanceDisplay }}</p>
      <button @click="refetch">Refresh</button>
    </div>
    <div v-else>
      <p>Connect to view balance</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppKitAccount } from '@reown/appkit/vue'
import { useBalance } from '@wagmi/vue'
import type { Address } from 'viem'

// Expose these to the template automatically
const { address, isConnected, status } = useAppKitAccount()
console.log('Account Address:', address, 'Connected:', isConnected, 'Status:', status)

const { data, refetch } = useBalance({
  address: address as Address | undefined,
  watch: true
})

const balanceDisplay = computed(() =>
  data.value ? `${data.value.formatted} ${data.value.symbol}` : 'Loading…'
)
</script>
