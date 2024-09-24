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

        # Find the article tag with class 'job-tile'

        all_article_tag = soup.find_all('article', class_='job-tile')

        # Get all child tags inside the article
        print(len(all_article_tag))
        # print(all_article_tag)

        # specific_a_tag = all_article_tag.select_one('div:nth-child(1) > div:nth-child(1) > div:nth-child(2) a')
        # print(specific_a_tag)

        for i, tag in enumerate(all_article_tag):
            job_info = tag.select_one('div[data-test="JobTileDetails"]:nth-child(2) div[data-test="UpCLineClamp JobDescription"] p').text
            job_link_title = tag.select_one('div:nth-child(1) > div:nth-child(1) > div:nth-child(2) a')
            job_type  = tag.select_one('div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="job-type-label"]>strong').text
            # job_value = tag.find_all('div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="is-fixed-price"]>strong')
            job_value = tag.select('div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="is-fixed-price"] strong')

            if isinstance(job_value, list):
                job_value_str = ""
                for element in job_value:
                    job_value_str += str(element.text)
                job_value = job_value_str
                print(job_value_str)

            else : job_value = job_value.text

            print(job_link_title.text)
            print(job_type)
            print(job_value)
            print(job_info)
            print(job_link_title.get('href') + "\n\n")

    # print(soup)
        # title = soup.title.text
        # print(title)

        await page.wait_for_timeout(2000)

asyncio.run(get_jobs_upwork())

from playwright.sync_api import sync_playwright


def upwork_run():

    playwright =  sync_playwright().start()
    # browser = await playwright.chromium.launch(headless=False)
    browser =   playwright.chromium.launch(headless=False, channel='chrome')
    # loginForm > div > div:nth-child(1) > div > label > input
    # loginForm > div > div:nth-child(2) > div > label > input

    page = browser.new_page()
    # for i in range(1,568):
    # await page.goto("https://www.instagram.com/")
    page.goto("https://www.upwork.com/nx/search/jobs/?q=reactjs")
    pass

# upwork_run()
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
"""
select a article tag class named job-tile cursor-pointer px-md-4 air3-card air3-card-list px-4x inside 
it select a div tag with `data-test="JobTileDetails"` and then select a div class named: air3-line-clamp is-clamped
inside it there select a paragraph tag class named mb-0 text-body-sm use css selector
"""


"""

Step # 1 Getting all article tag

article.job-tile:nth-child(5)


Step # 2 Getting Job Details Tag

 `div[data-test="JobTileDetails"]:nth-child(2) div[data-test="UpCLineClamp JobDescription"] p`
 
```
<p class="mb-0 text-body-sm">Setup mocks and write the first unit test for the duplicate API calls bug that happens in our frontend repo.</p>
```



Step # 3 Saving html link for each job 

article.job-tile:nth-child(10) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)  a

Step 4 Extra Details
`pricing` : 
css selector `article.job-tile:nth-child(8) > div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="job-type-label"]>strong`
`article.job-tile:nth-child(8) > div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="job-type-label"]>strong`


`experience`:
css selector `article.job-tile:nth-child(8) > div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="experience-level"]>strong`

`duration`:  
css selector `article.job-tile:nth-child(8) > div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="duration-label"]>strong` get all strong

`article.job-tile:nth-child(8) > div:nth-child(2) > ul[data-test="JobInfo"] > li[data-test="is-fixed-price"]>strong` get all strong



```html content 
<a data-v-489be0f1="" href="/jobs/Full-stack-dashboard-and-admin-development-for-SaaS-product_~021838442850985729272/?referrer_url_path=/nx/search/jobs/" 
class="up-n-link" data-test="job-tile-title-link UpLink">
Full-stack dashboard and admin development for SaaS product</a>

```


article.job-tile:nth-child(10) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)

"""

"""
Article Tag
article.job-tile:nth-child(5)
/html/body/div[3]/div/div/div[1]/main/div/div/div/div[2]/div[2]/section/article[5]

"""

"""
Job Details Tag 
div[data-test="JobTileDetails"]


"""

"""
Job Details Tag -> air3-line-clamp-wrapper

article.job-tile:nth-child(9) > div:nth-child(2) > div:nth-child(2)

"""

"""
Job Description Paragraph Tag
#air3-line-clamp-19 > p:nth-child(1)
"""




"""OUTPUT 
React Native Developer
Hourly: $5.00 - $6.00 

Job Description:
As a React Native Developer, you will be responsible for the development and maintenance of cross-platform mobile applications for both Android and iOS. You will work closely with our product managers, designers, and backend developers to deliver a seamless user experience. The ideal candidate should have experience building mobile applications from scratch and have a strong understanding of the full mobile development life cycle.

Key Responsibilities:
Design and build cross-platform mobile applications using React Native for Android and iOS.
Collaborate with UX/UI designers to implement high-quality interfaces.
Integrate RESTful APIs and third-party libraries to enhance functionality.
Ensure the performance, quality, and responsiveness of the applications.
Debug and optimize code to ensure a smooth user experience.
Participate in code reviews and maintain high coding standards and best practices.
Work with the backend team to define API requirements and collaborate on data management.
Deploy and maintain apps in both the Google Play Store and Apple App Store.
Stay updated with the latest mobile development trends, frameworks, and tools.
Collaborate in an agile development environment, following CI/CD practices.

Required Skills & Qualifications:
Proven experience as a React Native Developer (2+ years or as required).
Strong proficiency in JavaScript, including DOM manipulation and JavaScript object model.
Experience with popular React Native workflows (such as Redux or MobX).
Familiarity with native build tools, like Xcode, Android Studio, and Gradle.
Experience with RESTful APIs and third-party libraries like Firebase, Realm, etc.
Understanding of mobile design principles and experience with building responsive UIs.
Knowledge of React.js and its core principles.
Experience with CI/CD tools for mobile applications.
Good understanding of version control systems like Git.
Knowledge of modern authorization mechanisms, such as JSON Web Token (JWT).
Familiarity with cloud message APIs and push notifications (e.g., Firebase Cloud Messaging).

Preferred Qualifications:
Experience with native mobile development (iOS/Android) is a plus.
Familiarity with TypeScript and ES6+ syntax.
Experience with testing frameworks and debugging tools.
Prior experience deploying mobile apps in app stores.
Knowledge of agile methodologies and workflow (Scrum, Kanban).

Soft Skills:
Excellent communication and collaboration skills.
Strong problem-solving and analytical skills.
Ability to work independently and manage multiple tasks efficiently.
A proactive, self-starter attitude.
/jobs/React-Native-Developer_~021838557854468693240/?referrer_url_path=/nx/search/jobs/



React Native Mobile App Developer Needed for Feature Enhancement
Hourly: $15.00 - $30.00 

We are seeking an experienced React Native developer to assist in adding new features and providing ongoing support for our existing mobile application. The ideal candidate should be proficient in React Native and have a strong understanding of mobile app development best practices. You will work closely with our team to implement new functionalities, troubleshoot issues, and ensure optimal performance. If you are passionate about mobile technology and ready to contribute to an exciting project, we would love to hear from you!
/jobs/React-Native-Mobile-App-Developer-Needed-for-Feature-Enhancement_~021838560060269557504/?referrer_url_path=/nx/search/jobs/



Backend Software Engineer Developer (Node.js)

Hourly: $15.00 - $30.00 

We are looking for an experienced Backend Software Engineer with expertise in Node.js and book metadata (specifically ONIX) to help structure our backend and develop APIs for our platform. This project will involve building a scalable backend for our Firebase-based system, setting up proper schemas to handle book data and media, and creating APIs for our React-based web app.

Key Responsibilities:
	•	Imrove the backend structure for our platform on Firebase, considering book schema and ONIX metadata standards.
	•	Develop APIs to integrate the backend with our React front-end.
	•	Ensure proper linkage between the platform’s content (text, audio, images) and its metadata (book formats, ISBN, etc.).
	•	Set up a scalable and secure backend to handle user data, books, and media files.
	•	Collaborate with our front-end developer to ensure seamless integration between the web app and backend.

Requirements:
	•	5+ years of experience in backend development with Node.js.
	•	Strong knowledge of Firebase, NoSQL databases, and serverless architecture.
	•	Expertise in book metadata standards, including ONIX.
	•	Experience designing scalable backends with APIs for front-end integration (React preferred).
	•	Knowledge of book schemas and best practices in handling book data (e.g., formats, metadata, ISBNs, and digital content).
	•	Familiarity with Google Cloud Platform (GCP) is a plus.

Deliverables:
	•	Properly structured Firebase backend for our platform, meeting all app and content requirements.
	•	Secure, efficient APIs for the front-end React web app.
	•	Documentation of the backend setup and API endpoints.

Duration:
Estimated project length is 1-2 months, with potential for ongoing work based on performance and needs.

/jobs/Backend-Software-Engineer-Developer-Node_~021838559923287783168/?referrer_url_path=/nx/search/jobs/



Senior Solidity/Smart Contract Developer & Web3/React.js Front-End Developer Needed
Hourly: $60.00 - $80.00 

We are looking for a highly skilled Senior Solidity/Smart Contract Developer combined with a Web3/React.js Front-End Developer for an innovative project. The ideal candidate will possess extensive experience in blockchain technology, smart contract development, and creating responsive front-end applications. You will collaborate closely with our team to ensure seamless integration between the smart contracts and user interface. If you are passionate about decentralized applications and thrive in a dynamic environment, we want to hear from you!
/jobs/Senior-Solidity-Smart-Contract-Developer-Web3-React-Front-End-Developer-Needed_~021838559892826518377/?referrer_url_path=/nx/search/jobs/



Full Stack Developer Needed for Startup Prototype
Hourly: $5.00 - $35.00 


We are a forward-thinking startup in the advertising production space, building a peer-to-peer platform designed to revolutionize how freelancers and clients collaborate.

Our project has already garnered significant interest from investors, and we're confident this platform will make a big impact in the industry. We're seeking a talented Full-stack Developer to lead the development of our MVP, with the potential to grow into a leadership role as the project scales.

What You’ll Do
As the Full-stack Developer, you will:

    Develop and maintain both the front-end and back-end of our platform.
    Implement key features such as user profiles, booking systems, and search filters.
    Build a dynamic pricing system that adjusts according to freelancer availability.
    Create an algorithm or filtering system that matches clients with freelancers based on their specific needs (e.g., creative vs. film-focused skills).
    Collaborate with the Product Manager to ensure an intuitive and scalable platform design.
    Potentially grow into a leadership role, helping to build and lead a tech team as the platform evolves.

Key Responsibilities

    Design and develop the platform’s front-end using modern JavaScript frameworks (React preferred).
    Build and maintain a secure back-end infrastructure (Node.js, Python, or similar).
    Develop a database system to handle user data (profiles, bookings, payments).
    Ensure the platform is mobile-responsive and user-friendly.
    Collaborate closely with the Product Manager and UI/UX designer to refine the user experience.

What We’re Looking For


    Technical Skills:
        Front-end: React, Angular, or Vue.js
        Back-end: Node.js, Python, or Ruby
        Database: Firebase, PostgreSQL, MongoDB, or similar.
        Familiarity with APIs (e.g., Stripe) and payment gateways.
    Problem-Solver: Ability to translate business requirements into technical solutions.
    Leadership Potential: Someone excited to potentially lead a development team as the project grows.
    Self-Motivated & Independent: You’ll own the product’s development, so being proactive is key.
    Strong Communication Skills: Fluent in English and able to communicate clearly.
    Experience in a Startup Environment: Comfortable in a fast-paced, dynamic startup setting.

Nice to Have

    Experience with peer-to-peer platforms, booking systems, or freelance marketplaces.
    Experience developing algorithms for search filtering and pricing optimization.
    Knowledge of accounting/bookkeeping systems for freelancers.

Why Join Us?

    Be a crucial part of building a platform that has attracted investor interest and has significant potential in the industry.
    Opportunity for growth into a leadership role as the project scales.
    Flexible working hours and remote-friendly.
    Competitive pay for project-based work, with long-term collaboration possibilities.
    Work closely with a passionate founder driving innovation in the advertising production industry.

How to Apply
Please send your resume, portfolio, and a brief cover letter outlining your experience and why you’re interested in this project to [your email address]. Be sure to highlight any relevant marketplace or platform work in your portfolio.

We look forward to hearing from you!
/jobs/Full-Stack-Developer-Needed-for-Startup-Prototype_~021838546561442085360/?referrer_url_path=/nx/search/jobs/


Est. budget:$500.00
Full Stack Nextjs & Node.js developer needed for taxi booking web app
Fixed price
Est. budget:$500.00
Project Overview
We are seeking a highly skilled and experienced developer (5+ years) to create a modern and efficient taxi booking application using Next.js for the frontend and Node.js for the backend. The platform will offer a seamless booking experience with multiple options, including Book Now, Book Later, Hourly Booking, and Parcel Delivery. This world-class application will focus on performance, scalability, and intuitive design.

Key Features & Requirements

1. User Authentication:
   - Secure user registration and login (JWT or OAuth).
   - Profile management for users.
2. Booking Options:
   - Book Now: Real-time ride booking with immediate availability.
   - Book Later: Pre-scheduling rides for a future date and time.
   - Hourly Booking: Option for users to book rides on an hourly basis.
   - Parcel Delivery: Feature to enable users to send parcels and delivery status updates.

3. Ride and Parcel Management:
   - Dynamic pricing based on distance, time, and type of booking.
   - Fare calculation algorithms for different booking options.
   - Notifications (email, SMS, in-app) for ride status, driver arrival, and parcel updates.

4. Admin Panel:
   - Manage users, and bookings.
   - Review and manage feedback and ratings.

5. Payment Gateway Integration:
   - Multiple payment methods (credit/debit cards, wallets, etc.).
   - Invoicing and receipt generation.

6. Real-Time Notifications & Alerts:
   - Push notifications for booking confirmations, driver details, ride status, and parcel updates.

7. Technology Stack:
   - Frontend: Next.js for high performance, server-side rendering, and responsive UI.
   - Backend: Node.js with Express for REST API development, real-time functionalities via WebSockets.
   - Database: MongoDB/PostgreSQL for flexible data management.
   - Third-Party Integrations:
     - GPS/Google Maps API for live tracking and location services.
     - Twilio for SMS notifications.
     - Stripe/PayPal for secure payments.

8. Scalability & Performance:
   - A highly scalable architecture to accommodate future growth (additional features, user base expansion).
   - Optimization for fast loading times and real-time responsiveness.

9. Testing & Security:
    - Unit and integration testing (Jest, Mocha).
    - Data encryption and adherence to security best practices (SSL, two-factor authentication).

10. Deployment & Maintenance:
    - CI/CD pipeline setup for automated testing, deployment, and updates.
    - Ongoing support and maintenance post-launch.

 Ideal Developer Profile:
We are looking for a senior developer with:
- 5+ years of experience in web development, with expertise in Next.js and Node.js.
- Experience with real-time functionalities, GPS tracking, and third-party API integrations.
- Familiarity with secure payment gateways and building modular, scalable systems.

 Deliverables:
- Fully functional taxi booking application with all specified features.
- Clean, well-documented code.
- Deployment on cloud infrastructure (AWS, Google Cloud, etc.).
- Comprehensive user and admin manuals.
- Post-launch support for a smooth transition.

 Timeline & Budget:
To be discussed based on the final scope and milestones.


/jobs/Full-Stack-Nextjs-Node-developer-needed-for-taxi-booking-web-app_~021838551279677525557/?referrer_url_path=/nx/search/jobs/


Est. budget:$10,000.00
Project Phase IV - Enhancements to Core Tools and Products
Fixed price
Est. budget:$10,000.00
We are seeking a skilled developer/team to help implement additional enhancements to our App’s core tools and products, aimed at improving the platform's functionality, user experience, and market reach. 

Our App is a unique platform utilizing a combination of AI and human intelligence to create localized and relevant questions for market research and customer interaction. 

Enhancements:
* Optimizations to the Ask Anyone and Geo tools to improve sharing capabilities and user engagement.
* Enhancement of the Ask Your Customers feature to support more detailed analytics and customizable survey options.
* Introduction of more sophisticated AI algorithms to further improve question relevance and localization across all products.
* UI/UX improvements across the platform, particularly for the Results and Daily Questions sections.
* Expansion of the Web Banner feature to support additional web platforms and integration options.

Required Skills:
- Expertise in full-stack development (preferably using React, Node.js, and MySQL).
- Experience with AI and machine learning integration.
- Strong UI/UX design capabilities.
- Experience with APIs for sharing tools and survey platforms.


We are looking for a developer/team who can bring innovative ideas to the table and help ensure that our App continues to provide the best experience for users and businesses.
/jobs/Project-Phase-Enhancements-Core-Tools-and-Products_~021838554282967965155/?referrer_url_path=/nx/search/jobs/


Est. budget:$30.00
React.js and Supabase Developer Needed for Role-Based Access Control (RBAC)


Fixed price
Est. budget:$30.00
We are looking for a React.js and Supabase developer to help differentiate user roles, specifically between finance and other departments, in our application. The main tasks involve fixing event listeners and setting up custom role-based access control (RBAC) so that finance-related data is visible only to users with finance roles. If you have experience with React.js, Supabase, and setting up role-specific permissions, we'd love to work with you to ensure the right users have access to the right information securely.We can assign you some other task related to UI changes we need in our dashboard.
Thanks
/jobs/React-and-Supabase-Developer-Needed-for-Role-Based-Access-Control-RBAC_~021838553309336061719/?referrer_url_path=/nx/search/jobs/


Est. budget:$1,000.00
Retool - Full-Stack Developer (Node.js & React) with Firebase, and Book Metadata Expertise
Fixed price
Est. budget:$1,000.00
We are looking for a Full-Stack Developer (Node.js & React) who is proficient in Firebase and Retool and has experience with book metadata (especially ONIX 3.0 schema). You will be responsible for building a custom internal admin tools in Retool that allows our team to easily add, edit, and manage book data and metadata, integrating with our existing systems. The tool will also include real-time visualizations as seen in our current React app, as well as future integrations with Shopify and other tools.

Additional responsibilities include:

	•	Configuring book metadata schemas, ensuring that the system is ONIX 3.0 compliant.
	•	Integrating with multiple sales channels and handling metadata for multiple language editions.
	•	Developing workflow automation for royalty calculations, inventory management, and book orders across platforms.

Preferred Experience:

	•	Experience with book metadata and schema standards like ONIX 3.0.
	•	Working knowledge of Firebase, Retool, and API integrations.
	•	Expertise in React, Node.js, NoSQL databases, and REST APIs.
	•	Experience with publishing or book metadata systems would be a significant plus.

Additional Skills:

	•	Proficiency in API integrations with e-commerce platforms like Shopify.
	•	Knowledge of royalty reporting and inventory management workflows.

/jobs/Retool-Full-Stack-Developer-Node-React-with-Firebase-and-Book-Metadata-Expertise_~021838550514482444032/?referrer_url_path=/nx/search/jobs/


Est. budget:$125.00
implement more feature in Nuxt.js and MongoDB website 
Fixed price
Est. budget:$125.00
Hi , 
I have website and i want to implement more feature in it,  like  listing the data from MongoDB and complete the control panel 
/jobs/implement-more-feature-Nuxt-and-MongoDB-website_~021838549707322039779/?referrer_url_path=/nx/search/jobs/

"""
