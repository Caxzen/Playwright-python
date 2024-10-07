import logging
from playwright.sync_api import sync_playwright
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


RETRY_LIMIT = 3
SCREENSHOT_DIR = "screenshots"


os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_screenshot(page, attempt):
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_attempt_{attempt}.png")
    page.screenshot(path=screenshot_path)
    logger.info(f"Screenshot captured: {screenshot_path}")

def run_test_with_retries(page, url):
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            run_test(page, url)
            break
        except Exception as e:
            logger.error("Test failed on attempt {}: {}".format(attempt, e))
            capture_screenshot(page, attempt)
            if attempt == RETRY_LIMIT:
                logger.error("Test failed after {} attempts".format(RETRY_LIMIT))

def run_test(page, url):
    logger.info(f"Navigating to {url}")
    page.goto(url)

    logger.info("Navigating to Form Authentication")
    page.click('text=Form Authentication')

    logger.info("Filling out the login form")
    page.fill('#username', 'tomsmith')
    page.fill('#password', 'SuperSecretPassword!')
    page.click('button[type="submit"]')

 
    try:
        page.wait_for_selector('.flash.success', timeout=5000)
        logger.info("Logged in successfully!")
    except Exception as e:
        logger.error("Failed to find the success message. Exception: {}".format(e))
        raise RuntimeError("Login was not successful.")


    success_message = page.inner_text('div#flash')
    logger.info(f"Success message: {success_message}")  


    if "You logged into a super secret area" not in success_message:
        logger.error("Unexpected success message content.")
        raise RuntimeError(f"Unexpected success message: {success_message}")

    logger.info("Test successfully completed!")

if __name__ == "__main__":
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        run_test_with_retries(page, "http://the-internet.herokuapp.com")
        browser.close()
