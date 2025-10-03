# app_logic.py

import flet as ft
from database import (
    update_contact_db,
    delete_contact_db,
    add_contact_db,
    get_all_contacts_db,
)

def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays contacts, with optional search filter."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)

    for contact in contacts:
        contact_id, name, phone, email = contact

        # helper functions that "freeze" the current contact values
        def on_edit_click(e, c=contact):
            open_edit_dialog(page, c, db_conn, contacts_list_view)

        def on_delete_click(e, cid=contact_id):
            delete_contact(page, cid, db_conn, contacts_list_view)

        contact_card = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(name, size=18, weight=ft.FontWeight.BOLD, expand=True),
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(text="Edit", icon=ft.Icons.EDIT, on_click=on_edit_click),
                                        ft.PopupMenuItem(),  # divider
                                        ft.PopupMenuItem(text="Delete", icon=ft.Icons.DELETE, on_click=on_delete_click),
                                    ],
                                ),
                            ]
                        ),
                        ft.Divider(),
                        ft.Row([ft.Icon(ft.Icons.PHONE, size=16, color="green"), ft.Text(phone or "No phone")]),
                        ft.Row([ft.Icon(ft.Icons.EMAIL, size=16, color="blue"), ft.Text(email or "No email")]),
                    ]
                ),
            )
        )

        contacts_list_view.controls.append(contact_card)

    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact and refreshes the list."""
    name_input, phone_input, email_input = inputs

    has_error = False  # track validation state

    # Validate name
    if not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        has_error = True
    else:
        name_input.error_text = None

    # Validate phone
    if not phone_input.value.strip():
        phone_input.error_text = "Phone number is required"
        has_error = True
    elif not phone_input.value.isdigit():
        phone_input.error_text = "Phone must contain only numbers"
        has_error = True

    # If any errors then stop
    if has_error:
        page.update()
        return

    # If valid then save to DB
    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)

    # Clear inputs
    for field in inputs:
        field.value = ""
        field.error_text = None

    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Shows a confirmation dialog before deleting a contact."""

    def confirm_delete(e):
        delete_contact_db(db_conn, contact_id)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    def close_dialog(e=None):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.TextButton(
                "Yes",
                on_click=confirm_delete,
                style=ft.ButtonStyle(color="white", bgcolor="red"),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )


    # Attach to page if not already
    if dialog not in page.overlay:
        page.overlay.append(dialog)

    dialog.open = True
    page.update()


def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    # Input fields inside the dialog
    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    # Function to save changes
    def save_and_close(e):
        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    # Define the dialog
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Helper to close dialog
    def close_dialog():
        dialog.open = False
        page.update()

    # Attach to page properly
    if dialog not in page.overlay:
        page.overlay.append(dialog)

    dialog.open = True
    page.update()
    page.dialog = dialog

