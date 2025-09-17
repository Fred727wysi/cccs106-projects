import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    # Configure the page
    page.window_center = True
    page.window_frameless = True
    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_height = 350
    page.window_width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT
    
    # Create UI controls
    login_title = ft.Text(
        "User Login",
        text_align=ft.TextAlign.CENTER,
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial"
    )
    
    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        disabled=False,
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
    )
    
    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        disabled=False,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.PASSWORD,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
    )
    
    async def login_click(e):
        # Define dialogs
        success_dialog = ft.AlertDialog(
            title=ft.Text("Login Successful"),
            content=ft.Text(
                f"Welcome, {username_field.value}!",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda _: page.close(success_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
        )
        
        failure_dialog = ft.AlertDialog(
            title=ft.Text("Login Failed"),
            content=ft.Text(
                "Invalid username or password",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda _: page.close(failure_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            icon=ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED)
        )
        
        invalid_input_dialog = ft.AlertDialog(
            title=ft.Text("Input Error"),
            content=ft.Text(
                "Please enter username and password",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda _: page.close(invalid_input_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            icon=ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE)
        )
        
        database_error_dialog = ft.AlertDialog(
            title=ft.Text("Database Error"),
            content=ft.Text(
                "An error occurred while connecting to the database",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda _: page.close(database_error_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Validation and database logic
        if not username_field.value or not password_field.value:
            page.open(invalid_input_dialog)
            return
        
        try:
            # Establish database connection
            connection = connect_db()
            cursor = connection.cursor()
            
            # Execute parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username_field.value, password_field.value))
            
            # Fetch result
            result = cursor.fetchone()
            
            # Close database connection
            cursor.close()
            connection.close()
            
            # Check if user was found
            if result:
                page.open(success_dialog)
            else:
                page.open(failure_dialog)
            
            page.update()
            
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            page.open(database_error_dialog)
            page.update()
    
    # Create login button
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=login_click,
        width=100,
        icon=ft.Icons.LOGIN
    )
    
    # Add controls to the page
    page.add(
        login_title,
        ft.Container(
            content=ft.Column(
                [username_field, password_field],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center
        ),
        ft.Container(
            content=login_button,
            alignment=ft.alignment.top_right,
            margin=ft.margin.only(top=0, right=20, bottom=40, left=0)
        )
    )

# Start the Flet app
ft.app(target=main)