<template>
  <div class="pages">
    <img src="/reown.svg" alt="Reown" width="150" height="150" />
    <h1>Aether Capital Rebalance Portfolio</h1>

    <appkit-button />
    <ActionButtonList />
    <UpdateBalance />
    <InfoList />
    <TesKomponen />

    <div class="advice">
      <p>
        This project only works with Diaz and Mirza wallets. Don't use other wallets.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createAppKit } from '@reown/appkit/vue'
import { wagmiAdapter, networks, projectId } from './config/index'

import ActionButtonList from './components/ActionButton.vue'
import InfoList from './components/InfoList.vue'
import UpdateBalance from './components/UpdateBalance.vue'
import TesKomponen from './components/TesKomponen.vue'

// Initialize Reown AppKit
createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId,
  themeMode: 'light',
  features: {
    connectMethodsOrder: ['email', 'social', 'wallet'],
    analytics: true
  },
  metadata: {
    name: 'Aether Rebalance',
    description: 'Aether Capital Rebalance Portfolio',
    url: window.location.origin,
    icons: ['https://your-icon-url']
  },
  themeVariables: {
    '--w3m-accent': '#000000'
  }
})
</script>
