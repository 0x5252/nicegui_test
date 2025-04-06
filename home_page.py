from nicegui import ui

from message import message


def content() -> None:
    message("This is the home page.").classes("font-bold")
    ui.label("use the menu on the top right to navigate.")
