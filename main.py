from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from starlette.middleware.base import BaseHTTPMiddleware

import home_page
import theme

passwords = {"admin": "admin", "user": "user"}

unrestricted_page_routes = {"/login"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if (
                not request.url.path.startswith("/_nicegui")
                and request.url.path not in unrestricted_page_routes
            ):
                return RedirectResponse(f"/login?redirect_to={request.url.path}")
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page("/")
def main_page() -> None:
    with theme.frame("Homepage"):

        def logout() -> None:
            app.storage.user.clear()
            ui.navigate.to("/login")

        with ui.column().classes("absolute-center items-center"):
            ui.label(f"Hello {app.storage.user["username"]}!").classes("text-2x1")
            ui.button(on_click=logout, icon="logout").props("outline round")


@ui.page("/subpage")
def test_page() -> None:
    with theme.frame("Subpage"):
        ui.label("Hello from subpage!")


@ui.page("/login")
def login(redirect_to: str = "/") -> Optional[RedirectResponse]:
    with theme.frame("Login"):

        def try_login() -> None:
            if passwords.get(username.value) == password.value:
                app.storage.user.update(
                    {"username": username.value, "authenticated": True}
                )
                ui.navigate.to(redirect_to)
            else:
                ui.notify("Wrong username or password", color="negative")

        if app.storage.user.get("authenticated", False):
            return RedirectResponse("/")

        username = ui.input("Username").on("keydown.enter", try_login)
        password = ui.input("Password", password=True, password_toggle_button=True).on(
            "keydown.enter", try_login
        )
        ui.button("Log in", on_click=try_login).props("outline round")

        return None


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(storage_secret="wtf is this")
