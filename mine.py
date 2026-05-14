import flet as ft
import sqlite3
import bcrypt
import os
import asyncio
import uuid
from datetime import datetime

# --- SYSTEM CONFIG ---
class FounderProtocol:
    FULL_NAME = "Abubakir Abdug‘aniyev Juraboyev Qobiljon o'g'li"
    VERSION = "GAB-X SOVEREIGN V21.WEB"
    DB_NAME = "gabx_enterprise_core.db"

# --- DATABASE ENGINE ---
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

# --- WEB UI ---
class GabXWebApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = GabXEngine()
        self.page.title = "GAB-X SOVEREIGN"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#050505"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.show_home()

    def show_home(self):
        self.page.clean()
        self.page.add(
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Text("GAB-X", size=60, weight="bold", color="gold"),
                    ft.Text("SYSTEM INITIALIZED", size=14, color="white54", letter_spacing=2),
                    ft.Divider(height=40, color="transparent"),
                    ft.Text(f"FOUNDER: {FounderProtocol.FULL_NAME}", size=16, italic=True),
                    ft.ElevatedButton(
                        "ENTER SYSTEM", 
                        on_click=lambda _: self.show_auth(),
                        bgcolor="gold", color="black", width=250, height=50
                    )
                ], horizontal_alignment="center")
            )
        )

    def show_auth(self):
        self.page.clean()
        u = ft.TextField(label="Login", width=300, border_color="gold")
        p = ft.TextField(label="Parol", password=True, width=300, border_color="gold")
        m = ft.Text()

        async def auth_logic(e):
            is_reg = (e.control.text == "REG")
            if not u.value or not p.value:
                m.value = "To'ldiring!"; m.color="red"
            elif is_reg:
                h = bcrypt.hashpw(p.value.encode(), bcrypt.gensalt()).decode()
                try:
                    await self.engine.execute("INSERT INTO users VALUES (?,?,?,?)", 
                        (str(uuid.uuid4()), u.value, h, datetime.now()), True)
                    m.value = "OK! Endi Login bosing."; m.color="green"
                except: m.value = "Bu login band!"; m.color="red"
            else:
                res = await self.engine.execute("SELECT * FROM users WHERE username=?", (u.value,))
                if res and bcrypt.checkpw(p.value.encode(), res[0]['password'].encode()):
                    self.dashboard(u.value)
                else: m.value = "Xato!"; m.color="red"
            self.page.update()

        self.page.add(
            ft.Container(alignment=ft.alignment.center, content=ft.Column([
                ft.Text("AUTH PORTAL", size=24, weight="bold", color="gold"),
                u, p,
                ft.Row([
                    ft.ElevatedButton("LOGIN", on_click=auth_logic, bgcolor="gold", color="black"),
                    ft.TextButton("REG", on_click=auth_logic)
                ], alignment="center"),
                m
            ], horizontal_alignment="center"))
        )

    def dashboard(self, user):
        self.page.clean()
        self.page.add(
            ft.Text(f"XUSH KELDINGIZ, {user}!", size=30, color="gold", weight="bold"),
            ft.Text("GAB-X SOVEREIGN ONLINE", color="green")
        )

if __name__ == "__main__":
    ft.app(target=GabXWebApp, view=ft.AppView.WEB_BROWSER, port=int(os.getenv("PORT", 8080)), host="0.0.0.0")

