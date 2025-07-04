<template>
  <section>
    <!-- 🧾 Account Info -->
    <h2>Account Info - Safe Wallet</h2>
    <pre>
Address: {{ address }}
Connected: {{ isConnected }}
Status: {{ status }}
    </pre>

    <!-- 💰 Native Balance -->
    <section>
      <h2>Balance</h2>
      <div v-if="isConnected">
        <p v-if="balanceState.loadingBalance">Loading balance...</p>
        <p v-else-if="balanceState.errorBalance">Error: {{ balanceState.errorBalance }}</p>
        <p v-else>Native Balance: {{ balanceState.nativeBalance }} {{ balanceState.symbol }}</p>
      </div>
      <div v-else>
        <p>Connect wallet to view balance</p>
      </div>
    </section>

    <!-- 📊 Aave LTV & Health -->
    <h2>Aave LTV</h2>
    <div v-if="loading">Loading Aave stats...</div>
    <div v-else-if="error">Error: {{ error.message }}</div>
    <div v-else>
      <p><strong>LTV:</strong> {{ ltv }}</p>
      <p><strong>Health Factor:</strong> {{ healthFactor }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
// ✅ Imports
import { reactive, toRefs, watchEffect, computed } from 'vue'
import { useAppKitAccount, useAppKitNetwork, useAppKitBalance } from '@reown/appkit/vue'
import type { Address } from 'viem'
import { useAaveLtv, type UseAaveLtvReturn } from '../composables/useAaveLtv'

// -- Types for balance result and local view state
interface BalanceState {
  nativeBalance: string | null
  symbol: string | null
  loadingBalance: boolean
  errorBalance: string | null
}

// ──────────────────────────────────────────────────────────────────────────────
// 🧠 1. AppKit wallet / network composables
const account = useAppKitAccount()
const { address, isConnected, status } = toRefs(account.value)

const network = useAppKitNetwork()
const { chainId } = toRefs(network.value)

// ──────────────────────────────────────────────────────────────────────────────
// 🎯 2. Address computed only after connected & chain selected
const addressWithChain = computed<Address | undefined>(() => {
  return isConnected.value && chainId.value && address.value
    ? (address.value as Address)
    : undefined
})

// ──────────────────────────────────────────────────────────────────────────────
// 💱 3. Native balance state
const balanceState = reactive<BalanceState>({
  nativeBalance: null,
  symbol: null,
  loadingBalance: false,
  errorBalance: null,
})

const { fetchBalance } = useAppKitBalance()

// Fetch native balance reactively on connection or network changes
watchEffect(async () => {
  if (isConnected.value && chainId.value && addressWithChain.value) {
    balanceState.loadingBalance = true
    balanceState.errorBalance = null

    const result = await fetchBalance()

    balanceState.loadingBalance = false
    if (result.isSuccess && result.data) {
      balanceState.nativeBalance = result.data.balance
      balanceState.symbol = result.data.symbol
    } else {
      balanceState.errorBalance = result.error
    }
  }
})

// ──────────────────────────────────────────────────────────────────────────────
// 📐 4. Aave LTV tracking
const {
  ltv,
  healthFactor,
  loading,
  error,
  fetchLtv,
}: UseAaveLtvReturn = useAaveLtv(addressWithChain)

// Trigger LTV fetch when address or chain changes
watchEffect(() => {
  if (addressWithChain.value && chainId.value) {
    fetchLtv()
  }
})
</script>

<!-- it is not scoped bruh!-->
<style>
section {
  padding: 20px;
  background-color: #9b1d1d;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
}
</style>
