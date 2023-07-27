from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


def playlist_length(driver_path, link, last=-1):
    def in_text(text: str):
        if ":" in text:
            return True
        return False

    o = webdriver.ChromeOptions()
    o.headless = True
    wd = webdriver.Chrome(executable_path=driver_path, options=o)
    wd.maximize_window()
    wd.get(link)
    WebDriverWait(wd, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME,
                                                                 "style-scope ytd-thumbnail-overlay-time-status"
                                                                 "-renderer"))
    no = int(wd.find_element(By.XPATH, '//*[@id="page-manager"]/ytd-browse/ytd-playlist-header-renderer/div/div[2]/div[1]/div/div[1]/div[1]/ytd-playlist-byline-renderer/div/yt-formatted-string[1]/span[1]').text)

    for i in range(no // 5):
        if ((i + 1) * 5) % 100 == 0:  # make this better
            time.sleep(5)
        ele = wd.find_elements(By.CLASS_NAME, "style-scope ytd-thumbnail-overlay-time-status-renderer")
        WebDriverWait(wd, timeout=10).until(lambda d: in_text(d.find_elements(By.CLASS_NAME, "style-scope "
                                                                                             "ytd-thumbnail-overlay"
                                                                                             "-time-status-renderer")[
                                                                  i * 5].text))
        wd.execute_script("window.scrollTo({a}, {b});".format(a=0, b=515 * (i + 1)))
        if last != -1 and (i * 5) >= last:
            break  # Mystery if you exchange this line with return you get TypeError: cannot unpack non-iterable
            # NoneType object

    li = []
    if last == -1:
        for i in ele:
            li.append(i.text)
    else:
        for i in ele[:last]:
            li.append(i.text)
    tot = 0
    for i in li:
        abc = i.split(":")
        if len(abc) == 1:
            print(abc[0])
            tot += int(abc[0])
        elif len(abc) == 2:
            tot += int(abc[0]) * 60 + int(abc[1])
        else:
            tot += int(abc[0]) * 3600 + int(abc[1]) * 60 + int(abc[2])
    days = tot // 86400
    hours = (tot // 3600) % 24
    minutes = int((tot / 60) % 60)
    seconds = tot % 60
    wd.quit()
    return days, hours, minutes, seconds


if __name__ == "__main__":
    url = str(input("URL: "))
    try:
        last = int(input("of how many videos do you want to know duration of: "))
    except ValueError:
        last = -1
    days, hours, minutes, seconds = playlist_length(r"C:\Users\ashut\Downloads\chromedriver_win32\chromedriver.exe", url, last)
    print("This playlist is {} days, {} hours, {} minutes and {} seconds long".format(days, hours, minutes, seconds))
