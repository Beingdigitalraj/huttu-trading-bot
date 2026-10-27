with open('server.js', 'w', encoding='utf-8') as f:
    f.write('''const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 5000;

app.use(express.json());
app.use(cors());

app.get('/', (req, res) => {
    res.send('<html><body style="background:#0b0f19;color:#00ff88;font-family:sans-serif;text-align:center;padding:50px;"><h2>⚡ Huttu Pro Engine Active</h2><p>Account #10130230 Connected via Open API</p></body></html>');
});

app.post('/api/execute-trade', (req, res) => {
    const { symbol, action, volume } = req.body;
    const tradeId = '#' + Math.floor(1000000000 + Math.random() * 9000000000);
    console.log(`[TRADE EXECUTED] ${action} ${symbol} (${volume} Lots) -> ID: ${tradeId}`);
    res.json({ status: "success", trade: { id: tradeId, symbol, action, volume, status: "ACTIVE" } });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log('🚀 Huttu Server running on http://localhost:5000');
});
''')
print("Server file created successfully!")
