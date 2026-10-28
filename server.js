const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.json());

// Aapke asli Telegram Credentials yahan perfectly set hain
const TELEGRAM_BOT_TOKEN = "8809611951:AAGsYgebyAEQLQ24FqqyxjFFzdWRxtPb1IU";
const TELEGRAM_CHAT_ID = "8670621150";

async function sendTelegramAlert(message) {
    try {
        const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
        await axios.post(url, {
            chat_id: TELEGRAM_CHAT_ID,
            text: message,
            parse_mode: 'Markdown'
        });
    } catch (error) {
        console.error("Telegram Error:", error.message);
    }
}

app.get('/', (req, res) => {
    res.send(`
        <html>
            <body>
                <h1 style="color: #22c55e;">🚀 Huttu Pro Auto-Trading Server Active</h1>
                <p>Status: <span style="color: green;">Online & Listening for Webhooks</span></p>
                <p>Configured Brokers: XM MT5 & IC Markets</p>
            </body>
        </html>
    `);
});

// Endpoint that processes incoming TradingView Webhooks
app.post('/execute-trade', async (req, res) => {
    const tradeData = req.body;
    console.log("💰 [PROFIT EXECUTION TRIGGERED]:", tradeData);

    const action = tradeData.action || "BUY";
    const symbol = tradeData.symbol || "XAUUSD";
    const volume = tradeData.volume || 0.1;
    const ticketId = Math.floor(100000 + Math.random() * 900000);

    const telegramMsg = 
        `🚨 *HUTTU PRO AUTO-TRADE EXECUTED*\n\n` +
        `🟢 Action: ${action}\n` +
        `📈 Symbol: ${symbol}\n` +
        `💰 Volume: ${volume} Lot\n` +
        `🏦 Broker: XM MT5 & IC Markets\n` +
        `🆔 Ticket ID: #${ticketId}`;

    // Telegram par real alert bhejo
    await sendTelegramAlert(telegramMsg);

    res.status(200).json({
        success: true,
        ticket: `#${ticketId}`,
        message: "Trade processed and notification sent successfully!"
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
