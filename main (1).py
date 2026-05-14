import flet as ft
import os

# GAB-X Tizim ma'lumotlari
FOUNDER = "Abubakir Abdug‘aniyev Juraboyev Qobiljon o'g'li"
VERSION = "GAB-X V21 CORE"

async def main(page: ft.Page):
    page.title = f"GAB-X | Founder: {FOUNDER}"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Dashboard interfeysi
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(name=ft.icons.SHIELD_SHARP, color="gold", size=60),
                ft.Text(FOUNDER, size=24, weight="bold", color="gold", text_align="center"),
                ft.Text("SYSTEM OWNER / FOUNDER", size=12, color="white54", italic=True),
                ft.Text(VERSION, size=10, color="green"),
                ft.Divider(height=20, color="transparent"),
                ft.Container(
                    content=ft.Text("TIZIMGA KIRISH", color="black", weight="bold"),
                    bgcolor="gold",
                    padding=15,
                    border_radius=10
                ),
            ], horizontal_alignment="center"),
            padding=40,
            border=ft.border.all(1, "gold"),
            border_radius=20,
            bgcolor="#111111"
        )
    )

if __name__ == "__main__":
    # Server portini avtomatik aniqlash
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
