
# Aether Rebalance SC

Automated portfolio rebalancing tool using [Moccasin](https://github.com/Cyfrin/moccasin) and Aave V3 on Arbitrum. This project simulates token deposit, lending, and rebalancing strategies on a forked mainnet network. This repo is modified version of Cyfrin Updraft's Algorithmic Trading (https://github.com/Cyfrin/mox-algorithmic-trading-cu)

---

## 📌 Features

- 🧠 Simulates deposit and withdrawal of **USDC** and **WETH**
- 💸 Automatically supplies assets to **Aave V3**
- 📊 Rebalances portfolio to match target allocations (e.g. 50/50 split)
- ⚙️ Forks live Arbitrum mainnet via Infura for realistic testing

---

## 📁 Project Structure

```bash
.
├── abis/                      # ABI JSON files for contract interaction
├── script/
│   ├── _setup_script.py       # Sets up environment, token balances
│   ├── deposit.py             # Handles Aave supply interactions
│   ├── rebalance.py           # Rebalance logic and price reading
├── .venv/                     # Python virtual environment
├── moccasin.toml              # Moccasin config file
└── README.md                  # Project documentation
````

---

## 🧪 Example Workflow

This project does the following:

1. Fork Arbitrum Mainnet and connect using Infura
2. Set up test wallet with ETH, USDC, and WETH balances
3. Supply assets to Aave V3 lending pool
4. Fetch live prices and calculate current allocations
5. Rebalance portfolio according to a target ratio

---

## 🧠 Getting Started

### 1. Clone & Setup

```bash
git clone https://github.com/mbahmujono/aether_rebalance_sc.git
cd aether_rebalance_sc
uv venv
uv tool install moccasin
source .venv/bin/activate
uv add moccasin
uv sync
mox run deposit_and_rebalance.py
```

### 2. Configure Environment

Ensure you have a working `moccasin.toml` with:

```toml
[default]
rpc_url = "https://arbitrum-mainnet.infura.io/v3/YOUR_INFURA_KEY"
network = "arbitrum-fork"
wallet = "your_wallet"
```

### 3. Run Simulation

```bash
mox run script/_setup_script.py --network arbitrum-fork
mox run script/deposit.py
mox run script/rebalance.py
```

---

## ⚠️ Troubleshooting

* **`BoaError: Unknown contract`**
  Make sure you are impersonating a known whale address with token balances on the fork.

* **Token Transfer Fails**
  Ensure your ABI files are accurate and that the contract supports the function being called (e.g. `sendValue` vs `transfer`).

---

## 📈 Example Output

```bash
Wallet after deposit USDC balance: 0.00 USDC
Wallet after deposit WETH balance: 0.00 WETH
Current aUSDC value: $5000.00
Current aWETH value: $5000.00
Current percent allocation of aUSDC: 50.00%
Current percent allocation of aWETH: 50.00%
```

---

## 🔗 Credits

* Powered by [Moccasin by Cyfrin](https://github.com/Cyfrin/moccasin)
* Aave V3 lending protocol on Arbitrum
* Titanoboa for simulated Ethereum execution

---

## 📄 License

MIT License

---

Let me know if you'd like it tailored for public users, educational walkthroughs, or internal fund automation!
```
