import flet as ft
import os

def main(page: ft.Page):
    page.title = "GAB-X Sovereign"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("GAB-X SOVEREIGN", size=45, weight="bold", color="blue"),
                ft.Text("Tizim Online / Faol", size=20, color="green"),
                ft.Divider(color="grey"),
                ft.ElevatedButton("Dashboardga kirish", icon=ft.icons.LOGIN),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center
        )
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")