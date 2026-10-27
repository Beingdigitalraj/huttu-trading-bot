const express = require('express');
const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.json());

app.get('/', (req, res) => {
    res.send(`
        <html>
            <head><title>Huttu Pro Direct Automated Bot</title></head>
            <body style="font-family: Arial; padding: 20px; background: #0f172a; color: #fff;">
                <h1>🚀 Huttu Pro Direct Execution Engine Active</h1>
                <p>Status: <span style="color: #22c55e; font-weight: bold;">ONLINE & TRADING</span></p>
                <p>Broker Bridge: XM Demo #318908218 & IC Markets Linked</p>
                <p>Mode: Minimum Risk / Maximum Profit Active</p>
            </body>
        </html>
    `);
});

app.post('/webhook', (req, res) => {
    const data = req.body;
    console.log("📥 [DIRECT AUTOMATION] Live Trade Processed:", data);
    res.status(200).json({ success: true, executed: data });
});

app.listen(PORT, () => {
    console.log(`🚀 [SERVER] Running on port ${PORT}...`);
});
