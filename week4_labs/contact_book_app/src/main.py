# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600

    db_conn = init_db()

    # Input fields with icons
    name_input = ft.TextField(
        label="Name",
        width=350,
        prefix_icon=ft.Icons.PERSON,
    )

    phone_input = ft.TextField(
        label="Phone",
        width=350,
        prefix_icon=ft.Icons.PHONE,
    )

    email_input = ft.TextField(
        label="Email",
        width=350,
        prefix_icon=ft.Icons.EMAIL,
        
    )

    # Contacts list
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    # Add button
    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(
            page, (name_input, phone_input, email_input), contacts_list_view, db_conn
        ),
    )

    # Search field
    search_field = ft.TextField(
        label="Search Contacts",
        width=350,
        prefix_icon=ft.Icons.SEARCH,   # 🔍 search icon
        on_change=lambda e: display_contacts(
            page, contacts_list_view, db_conn, search_field.value
        ),
    )


    # Dark mode switch
    def toggle_theme(e):
        if theme_switch.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    theme_switch = ft.Switch(label="Dark Mode", value=False, on_change=toggle_theme)

    # Page layout
    page.add(
        ft.Column(
            [
                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(),
                ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                search_field,
                theme_switch,
                ft.Container(
                    content=contacts_list_view,
                    expand=True,       # make it expand to fill space
                    height=400,     # fixed height for the list
                ),
            ],
            expand=True 
        )
    )


    # Initial display
    display_contacts(page, contacts_list_view, db_conn)


if __name__ == "__main__":
    ft.app(target=main)
