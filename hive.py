import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
import os
from PIL import Image

# Selenium lets us automate web broswers, but we need the web drivers for the browsers we want to automate.
# The paths for those will be here:

# Path for Chrome broswer driver
PATH = "C:\\Users\\joshw\\Documents\\Code Projects\\Python RESOURCES\\Web Scraping\\chromedriver.exe" 

web_driver = webdriver.Chrome(PATH)


def start():
    hive_folder_location = startup_routine()
    hive_folder_location_inner = hive_folder_location + '\\'
    urls = get_images_from_browser(web_driver, 0.01, 10, hive_folder_location_inner)
    web_driver.close()

    print(urls)

    extra_copies(5, urls, hive_folder_location_inner)

    return


# Make necessary startup checks (directory for file storage, etc.)
def startup_routine():
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    to_desktop_command = 'cd ' + desktop_path
    os.system(to_desktop_command + '&&' + 'mkdir HIVE')
    print(desktop_path)
    return desktop_path + '\\HIVE'

def get_images_from_browser(web_driver, delay, max_images, download_path):
    def scroll_down(web_driver):
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    
    bee_google_image_url = 'https://www.google.com/search?q=bee&client=firefox-b-1-d&sxsrf=ALiCzsY0Ca3ylje1FVlSUN9xOjtmMV6m6w:1651162199814&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiLqIvDkrf3AhXXg4kEHVfwAHsQ_AUoAXoECAIQAw&biw=1280&bih=909&dpr=1'
    web_driver.get(bee_google_image_url)

    image_urls = set()
    skips = 0
    while len(image_urls) + skips < max_images:
        scroll_down(web_driver)

        thumbnails = web_driver.find_elements(By.CLASS_NAME, "Q4LuWd")

        for image in thumbnails[len(image_urls) + skips: max_images]:
            try:
                image.click()
                time.sleep(delay)
            except:
                continue

            images = web_driver.find_elements(By.CLASS_NAME, "n3VNCb")
            for img in images:
                if img.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                if img.get_attribute('src') and 'http' in img.get_attribute('src'):
                    image_urls.add(img.get_attribute('src'))
                    print("Found image: " + str(len(image_urls)))
                    download_image(download_path, img.get_attribute('src'), 'bee' + str(len(image_urls)) + '.JPEG')
    
    return image_urls



def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content       # Getting contents of the url (image urls only)
        image_file = io.BytesIO(image_content)          # Storing file in memory (essentially binary data)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, 'wb') as f:
            image.save(f, "JPEG")
        print("\tSUCCESSFUL DOWNLOAD")
    except Exception as error:
        print('\tFAILED DOWNLOAD: ', error)

def extra_copies(copies, urls, hive_folder_location_inner):
    copies = 5
    for bee_img in range(len(urls)):
        current_copy = 0
        while current_copy < copies:
            zees = 'z' * (current_copy+1)
            current_name = hive_folder_location_inner + 'bee' + str(bee_img+1) + '.JPEG'
            copy_name = hive_folder_location_inner + 'bee' + str(bee_img+1) + zees + '.JPEG'
            print(current_name, copy_name)
            shutil.copy(current_name, copy_name)
            current_copy += 1


start()