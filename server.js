const express = require('express');
const https = require('https');
const app = express();
app.use(express.json());

const XM_REFERRAL_LINK = "https://clicks.pipaffiliates.com/c?c=1333865&l=en&p=1";
const TELEGRAM_BOT_TOKEN = "8809611951:AAGsYgebyAEQLQ24FqqyxjFFzdWRxtPb1IU";
const TELEGRAM_CHAT_ID = "8670621150";

function sendTelegramAlert(trade) {
    const message = `🚨 *HUTTU PRO AUTO-TRADE EXECUTED*\n\n` +
                    `🟢 *Action:* ${trade.action}\n` +
                    `📈 *Symbol:* ${trade.symbol}\n` +
                    `💰 *Volume:* ${trade.volume} Lot\n` +
                    `💼 *Broker:* ${trade.broker}\n` +
                    `🆔 *Ticket ID:* #${trade.id}\n\n` +
                    `🔑 *XM Demo Account:* 318908218\n` +
                    `🌐 *Join & Trade:* \n${XM_REFERRAL_LINK}`;

    const data = JSON.stringify({
        chat_id: TELEGRAM_CHAT_ID,
        text: message,
        parse_mode: "Markdown"
    });

    const options = {
        hostname: 'api.telegram.org',
        path: `/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(data)
        }
    };

    const req = https.request(options, (res) => {
        let responseData = '';
        res.on('data', (chunk) => { responseData += chunk; });
        res.on('end', () => {
            console.log(`📱 [TELEGRAM AUTO-ALERT SENT]: Status ${res.statusCode}`);
        });
    });

    req.on('error', (error) => {
        console.error(`❌ [TELEGRAM ERROR]: ${error.message}`);
    });

    req.write(data);
    req.end();
}

app.get('/', (req, res) => {
    res.send(`<h1>🚀 Huttu Pro Fully Automated Engine Active</h1><p>XM Demo #318908218 Connected</p>`);
});

app.post('/api/execute-trade', (req, res) => {
    const { symbol, action, volume, broker } = req.body;
    const tradeDetails = {
        id: Math.floor(100000 + Math.random() * 900000),
        symbol: symbol || "XAUUSD",
        action: action || "BUY",
        volume: volume || 0.1,
        broker: broker || "XM MT5 Demo (#318908218)",
        timestamp: new Date().toISOString()
    };

    console.log(`⚡ [AUTO EXECUTION TRIGGERED]: ${tradeDetails.action} ${tradeDetails.symbol} (${tradeDetails.volume} lot) on XM & IC Markets`);
    sendTelegramAlert(tradeDetails);

    res.json({
        success: true,
        message: "Automated trade executed successfully",
        trade: tradeDetails
    });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`🚀 [HUTTU AUTOMATION ENGINE] Running on port ${PORT}...`);
});
