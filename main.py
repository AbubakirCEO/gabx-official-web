import flet as ft
import os

def main(page: ft.Page):
    page.title = "GAB-X Sovereign Ecosystem"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800

    # --- RANG VA USLUB ---
    BG_COLOR = "#0f172a"
    ACCENT_COLOR = ft.colors.BLUE_600

    # --- NAVIGATSIYA FUNKSIYASI ---
    def change_tab(e):
        idx = e.control.selected_index
        tab_home.visible = (idx == 0)
        tab_smm.visible = (idx == 1)
        tab_math.visible = (idx == 2)
        tab_kiber.visible = (idx == 3)
        tab_elon.visible = (idx == 4)
        page.update()

    # --- 1. HOME TAB (BOSH SHAHAR) ---
    tab_home = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("GAB-X SOVEREIGN", size=50, weight="bold", color=ACCENT_COLOR),
                ft.Text("Global Optimization & Business Ecosystem", size=20, italic=True),
                ft.Divider(height=50, color=ft.colors.GREY_800),
                ft.Row([
                    ft.Container(content=ft.Text("CPU: 12%"), bgcolor=ft.colors.GREEN_900, padding=10, border_radius=10),
                    ft.Container(content=ft.Text("Server: Uzbekistan/Namangan"), bgcolor=ft.colors.BLUE_900, padding=10, border_radius=10),
                ])
            ]), padding=50
        )
    ], visible=True, expand=True)

    # --- 2. SMM TAB (ARZON SUPER NAKRUTKA) ---
    tab_smm = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("SMM Management Center", size=30, weight="bold"),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Platforma")),
                        ft.DataColumn(ft.Text("Xizmat")),
                        ft.DataColumn(ft.Text("Narx")),
                    ],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text("Telegram")), ft.DataCell(ft.Text("Kanal Obunachi")), ft.DataCell(ft.Text("7,500 so'm"))]),
                        ft.DataRow(cells=[ft.DataCell(ft.Text("Instagram")), ft.DataCell(ft.Text("Real Followers")), ft.DataCell(ft.Text("12,000 so'm"))]),
                        ft.DataRow(cells=[ft.DataCell(ft.Text("YouTube")), ft.DataCell(ft.Text("Watch Hours")), ft.DataCell(ft.Text("45,000 so'm"))]),
                    ]
                ),
                ft.ElevatedButton("Yangi Buyurtma", icon=ft.icons.ADD_SHOPPING_CART)
            ]), padding=50
        )
    ], visible=False, expand=True)

    # --- 3. MATH LAB (P vs NP) ---
    tab_math = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("Complexity Theory Lab", size=30, weight="bold", color="purple"),
                ft.Text("Abdug'aniyev Theorem: P ≈ NP Analysis", size=18),
                ft.Container(
                    bgcolor=ft.colors.BLACK, padding=20, border_radius=10,
                    content=ft.Text("L = { <M, w, 1^t> | M(w) halts in t steps }\nStatus: Optimizing search space...", font_family="monospace")
                ),
                ft.ProgressBar(value=0.85, color="purple", width=400),
            ]), padding=50
        )
    ], visible=False, expand=True)

    # --- 4. KIBER SPORT (GAME CLUB MANAGER) ---
    tab_kiber = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("KiberSport 65 PC Center", size=30, weight="bold", color="red"),
                ft.Row([
                    ft.Card(content=ft.Container(content=ft.Text("PC 1-20: BAND"), padding=20, bgcolor="red")),
                    ft.Card(content=ft.Container(content=ft.Text("PC 21-65: BO'SH"), padding=20, bgcolor="green")),
                ]),
                ft.Text("CS 1.6 & PUBG Turnirlari faol", size=16)
            ]), padding=50
        )
    ], visible=False, expand=True)

    # --- 5. ELON MUSK (SPACE NEWS) ---
    tab_elon = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("SpaceX & Mars Exploration", size=30, weight="bold", color="orange"),
                ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/e/ee/Starship_flight_4_launch.jpg", width=400, border_radius=15),
                ft.Text("Elon Musk: 'Mars is the key to humanity's future'", italic=True)
            ]), padding=50
        )
    ], visible=False, expand=True)

    # --- SIDEBAR NAV ---
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min
