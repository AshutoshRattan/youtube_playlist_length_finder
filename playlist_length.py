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
    no = int(wd.find_element(By.XPATH, '//*[@id="stats"]/yt-formatted-string[1]/span[1]').text)

    for i in range(no // 5):
        if ((i + 1) * 5) % 100 == 0:  # make this better
            time.sleep(5)
        ele = wd.find_elements(By.CLASS_NAME, "style-scope ytd-thumbnail-overlay-time-status-renderer")
        WebDriverWait(wd, timeout=10).until(lambda d: in_text(d.find_elements(By.CLASS_NAME, "style-scope "
                                                                                             "ytd-thumbnail-overlay"
                                                                                             "-time-status-renderer")[
                                                                  (i) * 5].text))
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
        try:
            a, b = i.split(":")
            a = int(a)
            b = int(b)
            tot += a * 60 + b
        except ValueError:
            a, b, c = i.split(":")
            a = int(a)
            b = int(b)
            c = int(c)
            tot += a * 3600 + b * 60 + c
    days = tot // 86400
    hours = (tot // 3600) % 24
    minutes = int((tot / 60) % 60)
    seconds = tot % 60
    wd.quit()
    return days, hours, minutes, seconds


if __name__ == "__main__":
    url = str(input("URL: "))
    try:
        last = int(input("type -1 if you want to find of duration of entire playlist or first n videos: "))
    except ValueError:
        last = -1
    days, hours, minutes, seconds = playlist_length(r"C:\Users\ashut\Desktop\scraping\chromedriver", url, last)
    print("This playlist is {} days, {} hours, {} minutes and {} seconds long".format(days, hours, minutes, seconds))
