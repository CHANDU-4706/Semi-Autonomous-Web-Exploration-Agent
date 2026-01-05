
from playwright.sync_api import sync_playwright

class BrowserController:
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        """Starts the browser session."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        # Set a reasonable timeout
        self.page.set_default_timeout(10000)

    def navigate(self, url):
        """Navigates to the specified URL."""
        if not self.page:
            raise Exception("Browser not started. Call start() first.")
        print(f"[Browser] Navigating to {url}...")
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def get_page(self):
        """Returns the current page object."""
        return self.page

    def close(self):
        """Closes the browser session."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
