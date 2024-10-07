import logging
from playwright.sync_api import sync_playwright


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Report:
    def __init__(self):
        self.results = []

    def add_result(self, test_name, status, error=None):
        self.results.append({
            'name': test_name,
            'status': status,
            'error': error
        })

    def generate_html_report(self):
        report_file = "test_report.html"
        with open(report_file, "w") as f:
            f.write("<html><head><title>Test Report</title></head><body>")
            f.write("<h1>Test Report</h1>")
            for result in self.results:
                f.write(f"<p>Test: {result['name']}, Status: {result['status']}</p>")
                if result['error']:
                    f.write(f"<p>Error: {result['error']}</p>")
            f.write("</body></html>")
        logger.info(f"Report generated: {report_file}")

def run_test(report):
    test_name = "Accessing The Internet Page"
    logger.info(f"Running {test_name}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:

            page.goto("https://the-internet.herokuapp.com/")
            assert page.title() == "The Internet"
            report.add_result(test_name, "PASS")
            logger.info(f"{test_name} completed successfully.")
            test_link = "Elemental Selenium"
            page.click("text='Elemental Selenium'")  
            assert page.title() == "Elemental Selenium"
            report.add_result("Elemental Selenium Link Test", "PASS")
            logger.info("Elemental Selenium link test completed successfully.")
            page.go_back()

        except Exception as e:
            report.add_result(test_name, "FAIL", str(e))
            logger.error(f"{test_name} failed: {str(e)}")
        finally:
            page.close()
        browser.close()

if __name__ == "__main__":
    report = Report()
    run_test(report)
    report.generate_html_report()
