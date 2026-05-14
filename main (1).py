import flet as ft
import sqlite3
import bcrypt
import jwt
import asyncio
import uuid
import os
from datetime import datetime

# --- 1. ASOSCHI VA TIZIM PROTOKOLLARI ---
class FounderProtocol:
    FULL_NAME = "Abubakir Abdug‘aniyev Juraboyev Qobiljon o'g'li"
    BIRTHDAY = "20-September"
    VERSION = "GAB-X SOVEREIGN V21.WEB"
    SECRET_KEY = os.getenv("GABX_SECRET", "GABX_TITAN_ULTRA_MASTER_2026")
    DB_NAME = "gabx_enterprise_core.db"
    AGE_RESTRICTED = False

# --- 2. ASYNCHRONOUS DATA ARCHITECTURE ---
class GabXEngine:
    def __init__(self):
        self._initialize_vault()

    def _initialize_vault(self):
        with sqlite3.connect(FounderProtocol.DB_NAME) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY, username TEXT UNIQUE, 
                password TEXT, role TEXT, created_at TIMESTAMP)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, action TEXT)''')

    async def execute(self, sql, params=(), commit=False):
        return await asyncio.to_thread(self._sync_execute, sql, params, commit)

    def _sync_execute(self, sql, params, commit):
        with sqlite3.connect(FounderProtocol.DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(sql, params)
            if commit: conn.commit(); return True
            return [dict(r) for r in cursor.fetchall()]

# --- 3. THE UNIFIED WEB INTERFACE ---
class GabXWebApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = GabXEngine()
        self.current_session = None
        self._configure_web_environment()

    def _configure_web_environment(self):
        self.page.title = f"GAB-X | Founder: {FounderProtocol.FULL_NAME}"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#050505"
        self.page.padding = 0
        self.show_opening_ceremony()

    def show_opening_ceremony(self):
        self.page.clean()
        is_bday = (datetime.now().strftime("%d-%B") == FounderProtocol.BIRTHDAY)
        
        ceremony = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column([
                # TUZATILGAN QATOR: SHIELD_SHARP o'rniga SECURITY ishlatildi
                ft.Icon(name=ft.icons.SECURITY, color="gold", size=60),
                ft.Text("INITIALIZING GAB-X CORE", size=12, color="gold", weight="bold", opacity=0.7),
                ft.Text(FounderProtocol.FULL_NAME, size=32, weight="bold", text_align="center"),
                ft.Text("SYSTEM OWNER / FOUNDER", color="white54", size=14, italic=True),
                ft.Divider(height=40, color="transparent"),
                ft.ElevatedButton(
                    "TIZIMNI ISHGA TUSHIRISH", 
                    on_click=lambda _: self.show_auth_portal(),
                    bgcolor="gold", color="black", width=300, height=55
                )
            ], horizontal_alignment="center", alignment="center")
        )
        self.page.add(ceremony)

    def show_auth_portal(self):
        self.page.clean()
        u_in = ft.TextField(label="Username", width=350, border_color="gold")
        p_in = ft.TextField(label="Password", password=True, width=350)
        msg = ft.Text()

        async def auth_action(e):
            is_new = (e.control.text == "PROFIL YARATISH")
            if is_new:
                hashed = bcrypt.hashpw(p_in.value.encode(), bcrypt.gensalt()).decode()
                try:
                    await self.engine.execute(
                        "INSERT INTO users (id, username, password, role, created_at) VALUES (?,?,?,?,?)",
                        (str(uuid.uuid4()), u_in.value, hashed, "USER", datetime.now()), commit=True)
                    msg.value = "Profil yaratildi! Endi kiring."; msg.color="green"
                except: msg.value = "Bu login band!"; msg.color="red"
            else:
                res = await self.engine.execute("SELECT * FROM users WHERE username=?", (u_in.value,))
                if res and bcrypt.checkpw(p_in.value.encode(), res[0]['password'].encode()):
                    self.current_session = {"id": res[0]['id'], "name": u_in.value}
                    self.show_main_dashboard()
                else: msg.value = "Login yoki parol xato!"; msg.color="red"
            self.page.update()

        self.page.add(
            ft.Container(
                expand=True, alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Text("GAB-X SECURE ACCESS", size=24, weight="bold"),
                    u_in, p_in,
                    ft.ElevatedButton("TIZIMGA KIRISH", on_click=auth_action, width=350, bgcolor="gold", color="black"),
                    ft.TextButton("PROFIL YARATISH", on_click=auth_action),
                    msg
                ], horizontal_alignment="center", alignment="center")
            )
        )

    def show_main_dashboard(self):
        self.page.clean()
        self.page.add(
            ft.AppBar(
                title=ft.Text(f"GAB-X OS | User: {self.current_session['name']}"),
                bgcolor="#111111",
                actions=[ft.IconButton(ft.icons.LOGOUT, on_click=lambda _: self.show_auth_portal())]
            ),
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Row([
                        ft.Card(expand=True, content=ft.Container(padding=20, content=ft.Column([
                            ft.Text("TIZIM STATUSI", size=12, color="white54"),
                            ft.Text("ONLINE", size=28, weight="bold", color="green")
                        ]))),
                        ft.Card(expand=True, content=ft.Container(padding=20, content=ft.Column([
                            ft.Text("FOUNDER"),
                            ft.Text(f"{FounderProtocol.FULL_NAME[:15]}...", size=18, color="gold", weight="bold")
                        ])))
                    ]),
                    ft.Text("GLOBAL NETWORK", size=18, weight="bold"),
                    ft.ListView(expand=True, controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PUBLIC),
                            title=ft.Text(f"Sovereign Node #{i}"),
                            subtitle=ft.Text("Tizim muvaffaqiyatli ishga tushdi.")
                        ) for i in range(3)
                    ])
                ])
            )
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=GabXWebApp, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
