import argparse
import requests
import os.path
import tempfile
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def getVRedditObject(link):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(link)

    elem = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/div[1]/a").get_attribute("href")
    video = elem + "/DASH_720"
    audio = elem + "/audio"

    return (video, audio)


ap = argparse.ArgumentParser()
ap.add_argument("-l", "--reddit-link", required=True, help="The reddit link with a vreddit video")
ap.add_argument("-o", "--output-name", required=False, help="The file name to output (defaults to output.mp4)")

try:
    subprocess.run(["ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    print("This script requires ffmpeg to be installed on your system. Please install it using your favourite package manager and try again.")
    sys.exit(1)


args = vars(ap.parse_args())
output = args['output_name']

if not output:
    output = "output.mp4"
else:
    if not output.endswith(".mp4"):
        output = output + ".mp4"

link = args['reddit_link']
link.replace("www.reddit.com", "old.reddit.com")
obj = getVRedditObject(link)
with tempfile.NamedTemporaryFile() as tmpVideo:
    with tempfile.NamedTemporaryFile() as tmpAudio:
        tmpVideo.write(requests.get(obj[0], stream=True).content) #todo: add loading bars?
        tmpAudio.write(requests.get(obj[1], stream=True).content)
        subprocess.run(["ffmpeg", "-i", tmpVideo.name, "-i", tmpAudio.name, "-c", "copy", output])