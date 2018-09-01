from urllib.request import urlopen
import xml.etree.ElementTree as ET
from selenium import webdriver
import time
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get("https://www.youtube.com/watch?v=zppTAkoVKnA")
time.sleep(1)

try:
    videoAdUiPreSkipButton = driver.find_element(By.XPATH("//div[@class='videoAdUiPreSkipButton']"))
    if  videoAdUiPreSkipButton.is_displayed() == True:
        videoAdUiPreSkipButtonFirstDiv = driver.find_element(By.XPATH("//div[@class='videoAdUiPreSkipButton']//div[1]"))
        videoAdUiPreSkipButtonSECONDDiv = driver
        time.sleep(2)
        skipaddbutton = driver.find_element(By.XPATH("//div[@class='videoAdUiSkipContainer html5-stop-propagation']"))
        skipaddbutton.click()
except:
    try:
        driver.find_element_by_class_name("ytp-subtitles-button").click()
    except:
        driver.refresh()
        time.sleep(3)
        try:
            driver.find_element_by_class_name("ytp-subtitles-button").click()
        except:
            AttributeError()
timedtext_url=[]
for entry in driver.get_log('performance'):
    try:
        tmnt = re.search(r'\btimedtext\b.*srv3',str(entry)).group()
        print("https://www.youtube.com/api/"+ tmnt, file=open("network_outout.txt", "a"))
        results = "https://www.youtube.com/api/" + tmnt

        timedtext_url.append(results)
    except:
        searchbox_result = None

def get_transcript(timedtext_url):
    # grab the XML file at that URL
    handle = urlopen(timedtext_url[0])
    contents = handle.read()

    # parse XML
    root = ET.fromstring(contents)
    # root = tree.getroot()

    running_words = []
    body = root.find("body")
    for p in body.findall("p"):
        if p.text is None or p.text == "\n":
            # nothing here, go to the <s> inside
            words = [clean_text(s.text) for s in p.findall("s")]
        else:
            # p.text is an actual word/string!
            words = [clean_text(p.text)]
        running_words.extend(words)

    final_text = " ".join(running_words)

    return final_text


def clean_text(text):
    return text.strip().replace("\n", " ")

print(clean_text(text=get_transcript(timedtext_url)), file=open("outout.txt", "a"))