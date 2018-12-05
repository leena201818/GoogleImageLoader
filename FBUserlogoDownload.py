# encoding=utf-8
from selenium import webdriver
import random,time,os
import urllib.request
import base64

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui


class FBUserlogoDownload:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)

    def is_visible(slef,locator, timeout=10):
        try:
            ui.WebDriverWait(slef.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def is_not_visible(slef,locator, timeout=10):
        try:
            ui.WebDriverWait(slef.driver, timeout).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def scroll2Bottom(self,browser, maxCount=None):
        allBodyPre = browser.page_source
        iCount = 0
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            iCount += 1
            time.sleep(random.randint(4, 5))
            print("%sth time Scroll to the bottom to fetch more information" % iCount)

            if maxCount is not None:
                if iCount > maxCount:
                    break
            allBodySrolled = browser.page_source
            if len(allBodySrolled) == len(allBodyPre):
                print("no more information can be found!")
                break
            else:
                allBodyPre = allBodySrolled


    def base64tofile(self,base64src,localUrl):
        ori_image_data = base64.b64decode(base64src)
        with open(localUrl,'wb') as f:
            f.write(ori_image_data)

    def loginFB(self,usr,pwd):
        self.driver.get('https://www.facebook.com/')
        time.sleep(random.randint(3,5))
        xp_iu= "//input[@id='email']"
        xp_ip = "//input[@id='pass']"
        xp_login = "//input[@data-testid='royal_login_button']"
        if self.is_visible(xp_iu) and self.is_visible(xp_ip):
            e_usr = self.driver.find_element_by_xpath(xp_iu)
            e_pas = self.driver.find_element_by_xpath(xp_ip)
            e_login = self.driver.find_element_by_xpath(xp_login)
            e_usr.clear()
            e_pas.clear()
            e_usr.send_keys(usr)
            e_pas.send_keys(pwd)
            e_login.click()
            time.sleep(random.randint(5,10))

        else:
            print('input not visible')

        if self.is_visible(By.XPATH,"//input[@class='_1frb']"):
            return True
        return False


    def loadMemberByURL(self,surl):
        try:
            loginFlag = self.loginFB('leena201818@gmail.com','1qaz@WSX3edc')
            if not loginFlag:
                print("login failed!")
                return

            #surl = 'https://www.facebook.com/groups/8578301243/members/'
            self.driver.get(surl)
            time.sleep(random.randint(5,10))

            self.scroll2Bottom(self.driver)

            xp_seemore = "//a[@class='pam uiBoxLightblue uiMorePagerPrimary']"

            while self.is_visible(xp_seemore):
                btn_seemore = self.driver.find_element_by_xpath(xp_seemore)
                btn_seemore.click()
                time.sleep(random.randint(1, 4))
                self.scroll2Bottom(self.driver)

        except Exception as e:
            print(e)
            return False

    def savePages(self,targetfile):
        #all images are displayed
        title = self.driver.title
        print(title)
        os.system(r'd:\saveas.exe "{0}" {1}'.format(title,targetfile))
        print('save ok:{0}'.format(targetfile))

        # all images are displayed

        images = self.driver.find_elements_by_xpath("//img[@class='rg_ic rg_i']")
        for img in images:
            src = img.get_attribute('src')
            name = img.get_attribute('name').replace(':', '')
            dir = os.path.splitext(targetfile)[0]+'_files'
            localfile = os.path.join(dir, name + '.jpeg')

            print(src)

            if src is not None and src.startswith('data'):
                print('data')
                src = src.split(',')
                base64src = src[1]
                self.base64tofile(base64src, localfile)
                print('download base64 img:{0}'.format(localfile))
            else:
                print('{0} is not acceptable'.format(src))


if __name__ == '__main__':
    surl = 'https://www.facebook.com/groups/117245955585344/members/'
    ndaurl = 'https://www.facebook.com/groups/1615742195336598/members/'
    fu = FBUserlogoDownload()

    fu.loginFB('leena201818@gmail.com', '1qaz@WSX3edc')

    # fu.loadMemberByURL(surl)
    # targetfile = r'd:\img\samples\normal\117245955585344.htm'
    # fu.savePages(targetfile)
