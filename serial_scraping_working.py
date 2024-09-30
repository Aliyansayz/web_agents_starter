import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import lxml , os
import html5lib
from playwright.async_api import async_playwright
from job_dashboard import generate_html





keywords = ["reactjs", "python", "python-visualization", "python-database", "django"]

# Run the scraping process
asyncio.run(scrape_keyword(keyword=keywords, multi_keyword=True))




def scrape_upwork_html(record_info, record_id, response):
    # Parse the page content
    soup = BeautifulSoup(response, 'html.parser')
    all_article_tag = soup.find_all('article', class_='job-tile')

    for j, tag in enumerate(all_article_tag):
        job_details = tag.select_one(
            'div[data-test="JobTileDetails"]:nth-child(2) div[data-test="UpCLineClamp JobDescription"] p').text
        job_link_title = tag.select_one('div:nth-child(1) > div:nth-child(1) > div:nth-child(2) a')
        job_type = tag.select_one(
            'div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="job-type-label"]>strong').text
        job_value = tag.select('div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="is-fixed-price"] strong')
        job_url = job_link_title.get('href')
        job_url = f"https://www.upwork.com/"+f"{job_url}"
        # Process job value
        if isinstance(job_value, list):
            job_value_str = "".join([str(element.text) for element in job_value])
        else:
            job_value_str = job_value.text

        # Print the job details
        title = job_link_title.text


        record_info[record_id] = {}
        record_info[record_id]["title"] = title
        record_info[record_id]["type"] = job_type
        record_info[record_id]["value"] = job_value_str
        record_info[record_id]["description"] = job_details
        record_info[record_id]["proposal"] = ""
        record_info[record_id]["url"]  = f"https://www.upwork.com/" + f"{job_url}"
        record_info[record_id]["meta"] = f" 'record_id': {record_id}, 'title': {title}, 'job_type': {job_type}"
        record_id += 1
    pass
    return record_info

def saving_html(record_info, keyword):
    html_content = generate_html(record_info, keyword)

    folder_path = "reports"
    filename = f"Job_Mining_{keyword}.html"

    if not os.path.exists(folder_path): os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)

    # Start counter for potential duplicate file names
    counter = 1
    file_root, file_extension = os.path.splitext(file_path)

    # While loop to check if file exists, and increment counter if it does
    while os.path.exists(file_path):
        file_path = f"{file_root}_{counter}{file_extension}"
        counter += 1

    with open(file_path, "w") as file:
        file.write(html_content)

# Scrape job data from a specific keyword
async def scrape_keyword(keyword, multi_keyword=False):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False, channel='chrome')
        page = await browser.new_page()

        record_id = 0
        record_info = {}
        if multi_keyword and isinstance(keyword, list):
            page1 = await browser.new_page()
            page2 = await browser.new_page()
            page3 = await browser.new_page()
            page4 = await browser.new_page()
            page5 = await browser.new_page()
            page_instance = [page1, page2, page3, page4, page5]
            for i, word in enumerate(keyword):
                target_url = f"https://www.upwork.com/nx/search/jobs/?q={word}"
                page = page_instance[i]
                # page = await browser.new_page()

                await page.goto(target_url)
                await page.mouse.wheel(0, 25000)
                await page.screenshot(path=f"{word}_jobs_page.png")
                response = await page.content()
                record_info = scrape_upwork_html(record_info, record_id, response)
                saving_html(record_info, word)

                # await page.wait_for_timeout(2000)

            await browser.close()
            pass


        # Generate URL for the keyword

        # for i in range(pages_num):
        #     curr_page = i + 1
        #     if curr_page > 1: target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}&page={curr_page}"
        #     else: target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
        #     pass


        # url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
        # url_page_2_onward = f"https://www.upwork.com/nx/search/jobs/?q={keyword}&page={2}"
        else:
            target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
            await page.goto(target_url)
            await page.mouse.wheel(0, 25000)  # Scroll down the page to load more jobs
            await page.screenshot(path=f"{keyword}_jobs_page.png")  # Save a screenshot for each keyword
            response = await page.content()


            await asyncio.sleep(35)

            record_info = scrape_upwork_html(record_info, record_id, response)
            saving_html(record_info, keyword)

            await page.wait_for_timeout(2000)
            await page.close()
            await asyncio.sleep(6)



        await browser.close()

