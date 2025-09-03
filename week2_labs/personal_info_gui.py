# personal_info_gui.py
# CCCS 106 - Week 2 Lab Exercise
# Enhanced Personal Information with GUI

import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Personal Information Manager"
    page.window.width = 600
    page.window.height = 700
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    title = ft.Text("Personal Information Manager", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.INDIGO_700)

    # Inputs
    first_name = ft.TextField(label="First Name", width=280)
    last_name = ft.TextField(label="Last Name", width=280)
    age = ft.TextField(label="Age", width=100, keyboard_type=ft.KeyboardType.NUMBER)
    student_id = ft.TextField(label="Student ID", width=200)

    program_dropdown = ft.Dropdown(
        label="Academic Program", width=300,
        options=[
            ft.dropdown.Option("BSCS"), ft.dropdown.Option("BSIT"),
            ft.dropdown.Option("BSCpE"), ft.dropdown.Option("BSIS")
        ]
    )

    year_level = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="1st", label="1st Year"),
        ft.Radio(value="2nd", label="2nd Year"),
        ft.Radio(value="3rd", label="3rd Year"),
        ft.Radio(value="4th", label="4th Year"),
    ]))

    favorite_color = ft.Dropdown(
        label="Favorite Color", width=200,
        options=[ft.dropdown.Option(c) for c in ["Red","Blue","Green","Yellow","Purple","Orange","Pink","Black","White","Gray"]]
    )

    hobbies = ft.TextField(label="Hobbies/Interests", width=400, multiline=True)

    output_container = ft.Container(
        content=ft.Text("Fill out the form and click 'Generate Profile' to see your information."),
        bgcolor=ft.Colors.GREY_100, padding=15, border_radius=10, width=550
    )

    # Functions
    def generate_profile(e):
        try:
            if not all([first_name.value, last_name.value, age.value]):
                show_error("Please fill in all required fields (Name and Age)!")
                return

            current_year = datetime.now().year
            birth_year = current_year - int(age.value)
            grad_year = current_year + (4 - int(year_level.value[0]) if year_level.value else 4)

            profile = ft.Column([
                ft.Text("🎓 STUDENT PROFILE", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_700),
                ft.Divider(),
                ft.Text(f"👤 Full Name: {first_name.value} {last_name.value}", size=16),
                ft.Text(f"🆔 Student ID: {student_id.value or 'Not provided'}", size=16),
                ft.Text(f"🎂 Age: {age.value}", size=16),
                ft.Text(f"📅 Birth Year: {birth_year}", size=16),
                ft.Text(f"📚 Program: {program_dropdown.value or 'Not selected'}", size=16),
                ft.Text(f"📊 Year Level: {year_level.value or 'Not selected'}", size=16),
                ft.Text(f"🎨 Favorite Color: {favorite_color.value or 'Not selected'}", size=16),
                ft.Text(f"🎯 Hobbies: {hobbies.value or 'Not provided'}", size=16),
                ft.Divider(),
                ft.Text(f"🎓 Expected Graduation: {grad_year}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"📝 Generated on {datetime.now().strftime('%B %d, %Y %I:%M %p')}", size=12, color=ft.Colors.GREY_600),
            ])

            output_container.content = profile
            page.update()
        except ValueError:
            show_error("Please enter a valid age (number only)!")

    def clear_form(e):
        first_name.value = last_name.value = age.value = student_id.value = hobbies.value = ""
        program_dropdown.value = year_level.value = favorite_color.value = None
        output_container.content = ft.Text("Form cleared. Fill out the information again.")
        page.update()

    def show_error(message):
        error_dialog = ft.AlertDialog(title=ft.Text("Input Error"), content=ft.Text(message),
                                      actions=[ft.TextButton("OK", on_click=lambda e: close_error(error_dialog))])
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()

    def close_error(dialog):
        dialog.open = False
        page.update()

    # Buttons
    gen_btn = ft.ElevatedButton("Generate Profile", on_click=generate_profile, bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE, width=150)
    clr_btn = ft.ElevatedButton("Clear Form", on_click=clear_form, bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE, width=150)

    # Layout
    page.add(ft.Column([
        title, ft.Divider(),
        ft.Row([first_name, last_name], spacing=20),
        ft.Row([age, student_id], spacing=20),
        program_dropdown, ft.Text("Year Level:"), year_level,
        favorite_color, hobbies,
        ft.Row([gen_btn, clr_btn], spacing=20),
        ft.Divider(),
        ft.Text("Generated Profile:", size=18, weight=ft.FontWeight.BOLD),
        output_container,
    ], spacing=10))

if __name__ == "__main__":
    ft.app(target=main)
