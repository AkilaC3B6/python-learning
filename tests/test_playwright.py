import os
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
        language_dropdown = page.locator("//span[contains(@class,'header__langs__dropdown-icon') and contains(@class,'azure')]")
        expect(language_dropdown).to_be_visible()
        language_dropdown.click()
        english_language = page.locator("a[id*='languages-en']")
        expect(english_language).to_be_visible()
        english_language.click()
        expect(language_dropdown).to_be_hidden()
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