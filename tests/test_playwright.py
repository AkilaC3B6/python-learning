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
        language_dropdown = page.locator("(//span[contains(@class,'header__langs__dropdown-icon')])[2]")
        expect(language_dropdown).to_be_visible()
        language_dropdown.click()
        english_language = page.locator("a[id*='languages-en']")
        expect(english_language).to_be_visible()
        english_language.click()
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
        expect(page).to_have_title('Home | B2B Connect 🔗 | Mercedes-Benz');
        page.screenshot(path=str(screenshot_dir / "04_after_login.png"))
        features = page.locator("//span[contains(@class,'modal__header_close-button')]")
        expect(features).to_be_visible(timeout=30000)
        features.click()
        language_dropdown = page.locator("(//span[contains(@class,'header__langs__dropdown-icon')])[2]")
        expect(language_dropdown).to_be_visible()
        language_dropdown.click()
        english_language = page.locator("a[id*='languages-en']")
        expect(english_language).to_be_visible()
        english_language.click()
        page.wait_for_load_state("domcontentloaded")
        VIN = page.locator("div[data-qa='vehicle-list-item']").filter(has_text="WDB2304581F151448")
        VIN.locator("a[id*='vehicle-list-open']").click()
        print_vehicle = page.locator("//div[contains(@class,'vehicle-information__details ')]//a[contains(@id,'vehicle-vehicle-print-print')]")
        expect(print_vehicle).to_be_visible(timeout=10000)
        page.screenshot(path=str(screenshot_dir / "05_vehicle_overview_page.png"))
        details = page.locator("(//div[contains(@class,'vehicle-information')]//div[contains(@data-id,'activeTab')])[1]//td[contains(@class,'label')]")
        rowValue = None
        for index in range (details.count()):
                if details.nth(index).filter(has_text="Delivery Date").count() > 0:
                        rowValue = index;
                print(f"Delivery Date is in {rowValue}")
                break
        delivery_date = page.locator(f"((//div[contains(@class,'vehicle-information')]//div[contains(@data-id,'activeTab')])[1]//td[contains(@class,'value')])[{rowValue}]")
        value=delivery_date.text_content()
        print(value)
        print(delivery_date.inner_text().strip())
        with page.expect_popup() as newPageInfo:
                newsletter = page.locator("//button[contains(@id,'footer-newsletter-subscribe-go-to-url')]//parent::a")
                expected_url = newsletter.get_attribute("href")
                print("Expected URL:", expected_url)
                newsletter.click()
                child_page = newPageInfo.value
                child_page.wait_for_load_state("load")
                print(child_page.title())
                page.screenshot(path=str(screenshot_dir / "06_newsletter_page.png"))
                actual_url = child_page.url
                print("Actual URL:", actual_url)
                assert actual_url == expected_url, f"URL mismatch! Expected : {expected_url}, Actual : {actual_url}"

def test_dialog(page):
        screenshot_dir = Path("dialogTest")
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
        expect(page).to_have_title('Home | B2B Connect 🔗 | Mercedes-Benz');
        page.screenshot(path=str(screenshot_dir / "04_after_login.png"))
        features = page.locator("//span[contains(@class,'modal__header_close-button')]")
        expect(features).to_be_visible(timeout=30000)
        features.click()
        language_dropdown = page.locator("(//span[contains(@class,'header__langs__dropdown-icon')])[2]")
        expect(language_dropdown).to_be_visible()
        language_dropdown.click()
        english_language = page.locator("a[id*='languages-en']")
        expect(english_language).to_be_visible()
        english_language.click()
        page.wait_for_load_state("domcontentloaded")
        basket = page.locator("//button[contains(@data-qa,'go-to-basket-button')]")
        expect(basket).to_be_visible(timeout=30000)
        value_before = basket.all_text_contents()
        print(value_before)
        basket.click()
        page.screenshot(path=str(screenshot_dir / "05_basket_page.png"))
        parts_tab = page.locator("(//div[contains(@class,'shopping-basket')]//div[contains(@id,'parts-basket-tab-click')])[1]")
        expect(parts_tab).to_be_visible(timeout=30000)
        parts_tab.click()
        page.screenshot(path=str(screenshot_dir / "06_part.png"))
        add_note = page.locator("a[data-qa*='part-note-add-button']")
        add_note.click()
        note_field = page.locator("textarea[name='part-note']").fill("For Testing Purpose")
        time.sleep(5)
        page.screenshot(path=str(screenshot_dir / "07_notearea.png"))
        checkout = page.locator("button[id*='shopping-basket-webparts-submit']")
        #alert
        page.on("dialog",lambda dialog:dialog.accept())
        checkout.click()
        time.sleep(5)
        page.screenshot(path=str(screenshot_dir / "08_dialogBox.png"))