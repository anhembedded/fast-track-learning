
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

        # Specifically wait for the first code block to be visible
        code_block = page.locator('#pytest-hands-on.active pre').first
        await code_block.wait_for(state='visible', timeout=5000) # Added explicit wait

        # Take a screenshot of the code block
        screenshot_path = "/home/jules/verification/background_color_fix.png"
        await code_block.screenshot(path=screenshot_path)

        print(f"Screenshot of code block saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
