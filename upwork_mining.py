from bs4 import BeautifulSoup
import pandas as pd
import lxml
import html5lib
import asyncio
from playwright.async_api import async_playwright


async def get_jobs_upwork( ):
    # with async_playwright() as playwright:
        playwright = await async_playwright().start()
        # browser = await playwright.chromium.launch(headless=False)
        browser = await  playwright.chromium.launch(headless=False ,channel='chrome' )
        # loginForm > div > div:nth-child(1) > div > label > input
        # loginForm > div > div:nth-child(2) > div > label > input

        page = await browser.new_page()
        # for i in range(1,568):
        # await page.goto("https://www.instagram.com/")
        await page.goto("https://www.upwork.com/nx/search/jobs/?q=reactjs")
        # await page.goto("https://www.upwork.com/nx/search/jobs/?q={string_input}")
        # page = await browser.new_page()
        # page.goto()


        await page.mouse.wheel(0, 25000)
        await page.screenshot(path=f"upwork_mining.png")
        response = await page.content()

        soup = BeautifulSoup(response, 'html.parser')
        print(soup)
        title = soup.title.text
        print(title)
        # await page.wait_for_timeout(2000)

asyncio.run(get_jobs_upwork())

#
# page0 = browser.new_page()
# page0.goto(link0)
#
# page1 = browser.new_page()
# page1.goto(link1)
#
# page2 = browser.new_page()
# page2.goto(link2)
#
# page3 = browser.new_page()
# page3.goto(link3)
#
# response0 = page0.content()
# response1 = page1.content()
# response2 = page2.content()
# response3 = page3.content()
