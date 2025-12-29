
import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Construct the file path
        file_path = f"file://{os.getcwd()}/index.html"
        print(f"Navigating to {file_path}")

        await page.goto(file_path)

        # Navigate to the PyTest section
        await page.click('li.nav-item[data-target="pytest-hands-on"]')

        # Wait for the section to become visible
        await page.wait_for_selector('#pytest-hands-on.active', state='visible')

        # Find the first "Show Answer" button and click it
        show_answer_button = page.locator('.show-answer-btn').first
        await show_answer_button.click()

        # Wait for the modal to be visible
        modal = page.locator('#answer-modal')
        await modal.wait_for(state='visible', timeout=5000)

        print("Modal is visible. Taking screenshot...")

        # Take a screenshot of the modal area
        screenshot_path = "/home/jules/verification/modal_fix_verification.png"
        await page.screenshot(path=screenshot_path)

        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
