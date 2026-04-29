const express = require('express');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;
const DB_FILE = './orders.json';

const getOrders = () => {
    if (!fs.existsSync(DB_FILE)) return [];
    try {
        return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
    } catch (e) { return []; }
};

const saveOrder = (order) => {
    const orders = getOrders();
    orders.push(order);
    fs.writeFileSync(DB_FILE, JSON.stringify(orders, null, 2));
};

// Главная страница
app.get('/', (req, res) => {
    res.send('<h1>Samburger API v2.0 Live</h1>');
});

// Создание заказа с выдачей ID
app.post('/create-payment', (req, res) => {
    const { amount, customerName, phone, items } = req.body;
    
    // Генерируем короткий ID для удобства (например, последние 4 цифры времени)
    const shortId = Math.floor(1000 + Math.random() * 9000);
    const orderId = `SB-${shortId}`;

    const newOrder = {
        order_id: orderId,
        name: customerName,
        phone: phone,
        amount: amount,
        items: items || [],
        status: 'Новый',
        date: new Date().toLocaleString("ru-RU")
    };

    saveOrder(newOrder);
    console.log(`✅ Новый заказ: ${orderId}`);
    
    // Возвращаем ID фронтенду
    res.json({ success: true, order_id: orderId });
});

// Список для персонала
app.get('/admin/orders', (req, res) => {
    res.json(getOrders());
});

app.listen(PORT, () => {
    console.log(`🚀 Сервер на порту ${PORT}`);
});
