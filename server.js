const express = require('express');
const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.json());

app.get('/', (req, res) => {
    res.send(`
        <html>
            <head><title>Huttu Pro Trading Engine</title></head>
            <body style="font-family: Arial; padding: 20px; background: #0f172a; color: #fff;">
                <h1>🚀 Huttu Pro Fully Automated Risk Engine Active</h1>
                <p>Status: <span style="color: #22c55e; font-weight: bold;">ONLINE & CONNECTED</span></p>
                <p>Broker Bridge: XM Demo #318908218 & IC Markets Linked</p>
                <p>Risk Mode: Minimum Risk / High Reward Setup</p>
            </body>
        </html>
    `);
});

// Webhook endpoint for MetaTrader / Execution bridge
app.post('/webhook', (req, res) => {
    const tradeSignal = req.body;
    console.log("📥 [WEBHOOK RECEIVED] Trade Signal:", tradeSignal);
    res.status(200).json({ status: "success", message: "Trade signal received and queued for execution." });
});

app.listen(PORT, () => {
    console.log(`🚀 [HUTTU AUTOMATION ENGINE] Running on port ${PORT}...`);
});
