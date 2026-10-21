import os
import time

import pytest
from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

load_dotenv()
USERNAME = os.getenv("B2B_USERNAME")
PASSWORD = os.getenv("B2B_PASSWORD")

def highlight(locator):
    locator.evaluate("""
        element => {
            element.style.outline = "3px solid red";
            element.style.outlineOffset = "2px";
        }
    """)

def test_button_click(page):
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        page.goto("https://b2bconnect-staging.mercedes-benz.com/de")
        page.wait_for_timeout(8000)
        accept_all_button = page.locator("//button[contains(@id,'accept-all')]")
        if accept_all_button.count() > 0:
                accept_all_button.click()
                expect(accept_all_button).to_be_hidden(timeout=10000)
        login_button = page.locator("button[id*='header-login-login']")
        page.screenshot(path=str(screenshot_dir / "01_homepage.png"))
        expect(login_button).to_be_visible()
        login_button.click()
        username = page.locator("input[id='userid']")
        expect(username).to_be_visible(timeout=10000)
        page.screenshot(path=str(screenshot_dir / "02_username_page.png"))
        username.fill(USERNAME)
        username_next = page.locator("button[id='next-btn']")
        username_next.click()
        password = page.locator("input[id='password']")
        expect(password).to_be_visible(timeout=10000)
        page.screenshot(path=str(screenshot_dir / "03_password_page.png"))
        password.fill(PASSWORD)
        login_submit = page.locator("button[id='loginSubmitButton']")
        login_submit.click()
        homepage_logo = page.locator('a[aria-label="Back To Home"]')
        expect(homepage_logo).to_be_visible(timeout=20000)
        page.screenshot(path=str(screenshot_dir / "04_after_login.png"))