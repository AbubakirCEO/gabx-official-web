import flet as ft
import sqlite3
import bcrypt
import os
import asyncio
import uuid
from datetime import datetime

# --- 1. TIZIM SOZLAMALARI ---
class FounderProtocol:
    FULL_NAME = "Abubakir Abdug‘aniyev Juraboyev Qobiljon o'g'li"
    VERSION = "GAB-X SOVEREIGN V21.WEB"
    DB_NAME = "gabx_enterprise_core.db"

# --- 2. MA'LUMOTLAR BAZASI YADROSI ---
class GabXEngine:
    def __init__(self):
        with sqlite3.connect(FounderProtocol.DB_NAME) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users 
                (id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT, created_at TIMESTAMP)''')

    async def execute(self, sql, params=(), commit=False):
        def run():
            with sqlite3.connect(FounderProtocol.DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.execute(sql, params)
                if commit: conn.commit(); return True
                return [dict(r) for r in cur.fetchall()]
        return await asyncio.to_thread(run)

# --- 3. WEB INTERFEYS ---
class GabXWebApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = GabXEngine()
        self.page.title = f"GAB-X | Founder: {FounderProtocol.FULL_NAME}"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#050505" # Premium qora
        self.page.padding = 40
        self.show_home()

    def show_home(self):
        self.page.clean()
        self.page.add(
            ft.Container(
                expand=True, alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Text("GAB-X", size=60, weight="bold", color="gold"),
                    ft.Text("SOVEREIGN ENTERPRISE OS", size=14, color="white54", letter_spacing=2),
                    ft.Divider(height=40, color="transparent"),
                    ft.Text(f"FOUNDER: {FounderProtocol.FULL_NAME}", size=16, italic=True),
                    ft.Divider(height=40, color="transparent"),
                    ft.ElevatedButton(
                        "TIZIMGA KIRISH", 
                        on_click=lambda _: self.show_auth(),
                        bgcolor="gold", color="black", width=300, height=50
                    )
                ], horizontal_alignment="center")
            )
        )

    def show_auth(self):
        self.page.clean()
        u_field = ft.TextField(label="Username", width=350, border_color="gold")
        p_field = ft.TextField(label="Password", password=True, width=350, border_color="gold")
        msg = ft.Text()

        async def handle_auth(e):
            is_reg = (e.control.text == "RO'YXATDAN O'TISH")
            if not u_field.value or not p_field.value:
                msg.value = "Ma'lumotlarni to'ldiring!"; msg.color="red"
            elif is_reg:
                hashed = bcrypt.hashpw(p_field.value.encode(), bcrypt.gensalt()).decode()
                try:
                    await self.engine.execute("INSERT INTO users VALUES (?,?,?,?)", 
                        (str(uuid.uuid4()), u_field.value, hashed, datetime.now()), True)
                    msg.value = "Muvaffaqiyatli! Endi LOGIN ni bosing."; msg.color="green"
                except: msg.value = "Bu login band!"; msg.color="red"
            else:
                res = await self.engine.execute("SELECT * FROM users WHERE username=?", (u_field.value,))
                if res and bcrypt.checkpw(p_field.value.encode(), res[0]['password'].encode()):
                    self.show_dashboard(u_field.value)
                else: msg.value = "Login yoki parol xato!"; msg.color="red"
            self.page.update()

        self.page.add(
            ft.Container(expand=True, alignment=ft.alignment.center, content=ft.Column([
                ft.Text("AUTHENTICATION", size=24, weight="bold", color="gold"),
                u_field, p_field,
                ft.ElevatedButton("LOGIN", on_click=handle_auth, width=350, bgcolor="gold", color="black"),
                ft.TextButton("RO'YXATDAN O'TISH", on_click=handle_auth),
                msg
            ], horizontal_alignment="center"))
        )

    def show_dashboard(self, user):
        self.page.clean()
        self.page.add(
            ft.AppBar(title=ft.Text(f"GAB-X | {user}"), bgcolor="#111111"),
            ft.Column([
                ft.Container(padding=20, content=ft.Column([
                    ft.Text("WELCOME TO THE SOVEREIGN CORE", size=28, weight="bold", color="gold"),
                    ft.Text(f"Tizim muvaffaqiyatli ishga tushirildi. Hozirda barcha modullar barqaror ishlamoqda.", size=16),
                    ft.Divider(height=30),
                    ft.Row([
                        ft.Card(content=ft.Container(padding=20, content=ft.Text("STATUS: ONLINE", color="green", weight="bold"))),
                        ft.Card(content=ft.Container(padding=20, content=ft.Text(f"VER: 21.0", color="gold")))
                    ])
                ]))
            ])
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=GabXWebApp, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
