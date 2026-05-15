import flet as ft

def main(page: ft.Page):
    page.title = "GAB-X Sovereign"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    page.add(
        ft.Column(
            [
                ft.Text("GAB-X SOVEREIGN", size=40, weight="bold", color="blue"),
                ft.Text("Tizim muvaffaqiyatli ishga tushdi!", size=20, color="white"),
                ft.Divider(),
                ft.ElevatedButton("Dashboardga kirish", icon=ft.icons.LOGIN),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)
