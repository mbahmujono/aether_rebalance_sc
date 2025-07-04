export default defineEventHandler(async (event) => {
  const { symbol, amount, convert } = getQuery(event)

  const res = await $fetch('https://pro-api.coinmarketcap.com/v2/tools/price-conversion', {
    headers: {
      'X-CMC_PRO_API_KEY': process.env.CMC_API_KEY!,
      'Accept': 'application/json'
    },
    params: {
      symbol,
      amount,
      convert
    }
  })

  return res
})
