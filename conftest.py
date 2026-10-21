import base64
import pytest
import pytest_html
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--start-maximized"]
        )

        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        yield page

        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            screenshot = page.screenshot(full_page=True)
            image_base64 = base64.b64encode(screenshot).decode("utf-8")

            html = (
                '<div><img src="data:image/png;base64,'
                + image_base64
                + '" style="max-width:100%;"></div>'
            )

            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.html(html))
            report.extras = extras
