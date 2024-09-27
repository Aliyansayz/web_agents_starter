import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import lxml , os
import html5lib
from playwright.async_api import async_playwright
from job_dashboard import generate_html


# Scrape job data from a specific keyword
async def scrape_keyword(keyword, pages_num = 1):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False, channel='chrome')
        page = await browser.new_page()

        job_id = 0
        job_info = {}
        # Generate URL for the keyword
        for i in range(pages_num):
            curr_page = i + 1
            if curr_page > 1: target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}&page={curr_page}"
            else: target_url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
            pass


        # url = f"https://www.upwork.com/nx/search/jobs/?q={keyword}"
        # url_page_2_onward = f"https://www.upwork.com/nx/search/jobs/?q={keyword}&page={2}"

            await page.goto(target_url)
            await page.mouse.wheel(0, 25000)  # Scroll down the page to load more jobs
            await page.screenshot(path=f"{keyword}_jobs_page_{curr_page}.png")  # Save a screenshot for each keyword
            response = await page.content()

            # Parse the page content
            soup = BeautifulSoup(response, 'html.parser')
            all_article_tag = soup.find_all('article', class_='job-tile')

            title_list, type_list, value_list, description_list, url_list = [], [], [], [], []
            for j, tag in enumerate(all_article_tag):
                job_details = tag.select_one('div[data-test="JobTileDetails"]:nth-child(2) div[data-test="UpCLineClamp JobDescription"] p').text
                job_link_title = tag.select_one('div:nth-child(1) > div:nth-child(1) > div:nth-child(2) a')
                job_type = tag.select_one('div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="job-type-label"]>strong').text
                job_value = tag.select('div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="is-fixed-price"] strong')
                job_url = job_link_title.get('href')
                job_url = f"https://www.upwork.com/+{job_url}"
                # Process job value
                if isinstance(job_value, list):
                    job_value_str = "".join([str(element.text) for element in job_value])
                else:
                    job_value_str = job_value.text

                # Print the job details
                title = job_link_title.text
                await asyncio.sleep(1)

                # title_list.append(), value_list.append(job_value+ " ",str(job_type) ), description_list.append(job_details), url_list.append(job_url)
                job_info[job_id] = {}
                job_info[job_id]["title"] = title
                job_info[job_id]["type"]  = job_type
                job_info[job_id]["value"] = job_value_str
                job_info[job_id]["description"] = job_details
                job_info[job_id]["proposal"] = ""
                job_info[job_id]["url"] = f"https://www.upwork.com/"+f"{job_url}"
                job_id += 1

            print(job_info)
            html_content = generate_html(job_info, keyword)

            folder_path = "reports"
            filename = f"Job_Mining_{keyword}.html"

            if not os.path.exists(folder_path): os.makedirs(folder_path)
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "w") as file:
                file.write(html_content)
            await asyncio.sleep(35)

            await page.wait_for_timeout(2000)
            await page.close()
            await asyncio.sleep(6)



        await browser.close()



# Main function to run scraping for multiple keywords serially with delay
async def get_jobs_upwork(keywords, pages_num=1):
    for keyword in keywords:
        await scrape_keyword(keyword, pages_num)
        print(f"Finished scraping for keyword: {keyword}. Waiting for 30 seconds before the next keyword...")
        await asyncio.sleep(30)  # Wait for 30 seconds before the next request

# List of keywords to search for
keywords = ["reactjs", "python", "python-visualization", "python-database", "django"]

# Run the scraping process
asyncio.run(get_jobs_upwork(keywords, 1))


# Main function to run scraping for multiple keywords in parallel
# async def get_jobs_upwork(keywords):
#     tasks = [scrape_keyword(keyword) for keyword in keywords]  # Create a list of tasks
#     await asyncio.gather(*tasks)  # Run all tasks concurrently
#
# # List of keywords to search for
# keywords = ["reactjs", "python", "python-visualization", "python-database", "django"]
#
# # Run the scraping process
# asyncio.run(get_jobs_upwork(keywords))

"""

{1 : { "title": "",  "type": "", "description": "",  }

"""
