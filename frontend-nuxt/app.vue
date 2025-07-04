<template>
  <div class="pages" style="background-color: #000; color: #fff; padding: 20px; text-align: center;">
    <h1 style="color: #fff; font-size: 2em; margin-bottom: 20px;">Aether Capital Rebalance Portfolio</h1>
    <img src="/reown.svg" alt="Reown" width="150" height="150" />
    <h1>Aether Capital Rebalance Portfolio</h1>
    <div class="advice">
      <p>
        This project only works with Diaz and Mirza wallets. Don't use other wallets.
      </p>
    </div>

    <appkit-button /> 
    <!-- this is the button that opens the wallet connection modal, kebab cased because of global component registration -->
    <ActionButtonList />
    <UpdateBalance />
    <PortfolioBalance />
    <InfoList />


  </div>
</template>

<script setup lang="ts">
import { createAppKit, useAppKit } from '@reown/appkit/vue'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import ActionButtonList from './components/ActionButton.vue'
import InfoList from './components/InfoList.vue'
import UpdateBalance from './components/UpdateBalance.vue'
import { arbitrum, mainnet } from '@reown/appkit/networks'
import PortfolioBalance from './components/PortfolioBalance.vue'


// 1. Get projectId from https://cloud.reown.com
const projectId = import.meta.env.VITE_PROJECT_ID

// 2. Create a metadata object - optional
const metadata = {
  name: 'frontend web3',
  description: 'Web3 frontend for Aether Capital Rebalance Portfolio',
  url: 'http://127.0.0.1:5173/', // origin must match your domain & subdomain
  icons: ['https://assets.reown.com/reown-profile-pic.png'],
  title: 'Aether Capital Rebalance Portfolio'
}
const networks = [mainnet, arbitrum]
// 3. Create Wagmi Adapter
const wagmiAdapter = new WagmiAdapter({
  ssr: true,
  projectId,
  networks
})

// 4. Create modal
createAppKit({
  adapters: [wagmiAdapter],
  networks: [mainnet, arbitrum],
  metadata,
  projectId,
  features: {
    analytics: true // Optional - defaults to your Cloud configuration
  }
})

// 5. Use modal composable
const modal = useAppKit()
</script>
