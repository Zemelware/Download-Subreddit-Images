from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
import os
from time import sleep


# This function will wait so more posts are loaded
def render_page(url):
    options = Options()
    options.add_argument("--headless")
    options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    driver = webdriver.Chrome(
        options=options, executable_path="/usr/local/bin/chromedriver")
    driver.get(url)
    print("Rendering content...")
    sleep(5)
    # Scroll down to load more posts
    # TODO - create for loop and parameter to specify how much content to load
    driver.find_element_by_tag_name("html").send_keys(Keys.END)
    sleep(2)
    driver.find_element_by_tag_name("html").send_keys(Keys.END)
    sleep(3)
    source = driver.page_source
    driver.quit()
    return source


def download_subreddit_images(subreddit):
    source = render_page(f"https://www.reddit.com/r/{subreddit}")
    soup = BeautifulSoup(source, "lxml")

    print("Downloading images...")

    i = 1
    for post in soup.find_all("div", {"data-testid": "post-container"}):
        try:
            # If the post doesn't have an image, it will skip to the next post
            link = post.find("img", alt="Post image")["src"]
        except:
            continue
        title = post.h3.text
        # The file name mustn't contain slashes
        file_name = title.replace("/", " ")

        # Create 'images' folder if it doesn't exist
        os.makedirs(os.path.dirname(f"images/{file_name}.jpg"), exist_ok=True)

        # Save the image
        with open(f"images/{i} {file_name}.jpg", "wb") as f:
            f.write(requests.get(link).content)

        i += 1


if __name__ == "__main__":
    download_subreddit_images("itookapicture")
