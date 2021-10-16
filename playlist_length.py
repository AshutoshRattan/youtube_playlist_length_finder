from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def playlist_length(driver_path, link, last=-1):
    wd = webdriver.Chrome(executable_path=driver_path)
    wd.maximize_window()
    wd.get(link)
    WebDriverWait(wd, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME,
                                                                 "style-scope ytd-thumbnail-overlay-time-status"
                                                                 "-renderer"))
    no = int(wd.find_element(By.XPATH, '//*[@id="stats"]/yt-formatted-string[1]/span[1]').text)

    for i in range(no // 5):
        wd.execute_script("window.scrollTo({a}, {b});".format(a=500 * i, b=500 * (i + 1)))
        time.sleep(0.5)  # make this better
    ele = wd.find_elements(By.CLASS_NAME, "style-scope ytd-thumbnail-overlay-time-status-renderer")
    li = []
    for i in ele[:last]:
        li.append(i.text)
    tot = 0
    for i in li:
        a, b = i.split(":")
        a = int(a)
        b = int(b)
        tot += a * 60 + b
    hours = tot // 3600
    minutes = int((tot / 60) % 60)
    seconds = tot % 60
    print("This playlist is {} hours, {} minutes and {} seconds long".format(hours, minutes, seconds))
    wd.quit()


if __name__ == "__main__":
    playlist_length(r"",  # enter the location of webdriver here
                    "")  # enter the link to the playlist here
    # if you want to find length of first x videos add ", x" in playlist_length
