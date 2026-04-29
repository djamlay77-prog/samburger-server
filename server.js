const express = require('express');
const cors = require('cors');
const fs = require('fs');
const YooKassa = require('yookassa'); // Используем установленный пакет

const app = express();
app.use(cors());
app.use(express.json());

// Пока ключей нет, оставляем тестовые заглушки
const checkout = new YooKassa({
    shopId: '123456', 
    secretKey: 'test_xxxxxxxxxxxxxxxxxxxxxxxx'
});

const DB_FILE = './orders.json';

// Чтение базы
const getOrders = () => {
    if (!fs.existsSync(DB_FILE)) return [];
    try {
        return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
    } catch (e) { return []; }
};

// Сохранение в базу
const saveOrder = (order) => {
    const orders = getOrders();
    orders.push(order);
    fs.writeFileSync(DB_FILE, JSON.stringify(orders, null, 2));
};

// Маршрут для создания заказа
app.post('/create-payment', (req, res) => {
    const { amount, customerName, phone } = req.body;
    const orderId = "SB-" + Date.now();

    const newOrder = {
        order_id: orderId,
        name: customerName,
        phone: phone || 'Не указан',
        amount: amount,
        status: 'Ожидает оплаты',
        date: new Date()
    };

    saveOrder(newOrder);
    console.log(`✅ Заказ сохранен: ${orderId}`);
    res.json({ success: true, order_id: orderId });
});

// Маршрут для админки
app.get('/admin/orders', (req, res) => {
    res.json(getOrders());
});

app.listen(3000, () => {
    console.log('🚀 СЕРВЕР ЗАПУЩЕН!');
    console.log('🔗 Админка будет брать данные отсюда: http://localhost:3000/admin/orders');
});