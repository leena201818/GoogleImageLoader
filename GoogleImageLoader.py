# encoding=utf-8
from selenium import webdriver
import random,time,os
import urllib.request
import base64

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui


class GoogleImagerLoader:

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

    def downing(self,remoteUrl,localUrl):
        content = urllib.request.urlopen(remoteUrl).read()
        with open(localUrl,'wb') as f:
            f.write(content)

    def base64tofile(self,base64src,localUrl):
        ori_image_data = base64.b64decode(base64src)
        with open(localUrl,'wb') as f:
            f.write(ori_image_data)

    def searchImgByUrl(self,url):
        self.driver.get(url)
        ui.WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='hdtb-mitem hdtb-msel hdtb-imb']")))

        self.scroll2Bottom(self.driver,1)
        more = self.driver.find_element_by_xpath("//input[@class='ksb _kvc']")
        if more is not None:
            more.click()
            time.sleep(4)
            self.scroll2Bottom(self.driver)
        else:
            print('find all')

    def searchImgByImg(self,srcimg):
        localfile = os.path.abspath(srcimg)

        # # surl = 'https://www.google.com'
        # surl = 'https://www.google.co.jp/imghp'
        # self.driver.get(surl)
        # ui.WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='gb_P' and @data-pid='2']")))
        #
        # btn = self.driver.find_element_by_xpath("//a[@class='gb_P' and @data-pid='2']") #search by image
        # btn.click()

        try:
            surl = 'https://www.google.co.jp/imghp'
            self.driver.get(surl)

            if self.is_visible("//a[@class='gsst_a']"):
                uploadbtn = self.driver.find_element_by_xpath("//a[@class='gsst_a']") #open image btn
                uploadbtn.click()

            if self.is_visible("//a[@class='qbtbha qbtbtxt qbclr']"):
                uploadtab = self.driver.find_element_by_xpath("//a[@class='qbtbha qbtbtxt qbclr']") #tab upload
                uploadtab.click()

            if self.is_visible("//input[@id='qbfile']"):
                inputfileurl = self.driver.find_element_by_xpath("//input[@id='qbfile']") #browser btn
                #inputfileurl.send_keys(localfile)
                #inputfileurl.send_keys(r"d:/img/samples/searchbyimg/100003567040399.JPG")
                inputfileurl.click()
                print('d:\\upfile.exe {0}'.format(localfile))
                os.system('d:\\upfile.exe {0}'.format(localfile))
                time.sleep(6)
                print('search image like {0}'.format(os.path.split(srcimg)[1]))

                if self.is_visible("//a[@class='iu-card-header']"):
                    alikeimg = self.driver.find_element_by_xpath("//a[@class='iu-card-header']")
                    alikeimg.click()
                    time.sleep(6)

                    self.scroll2Bottom(self.driver)
                    if self.is_visible("//input[@class='ksb _kvc']"):
                        more = self.driver.find_element_by_xpath("//input[@class='ksb _kvc']")
                        if more is not None:
                            more.click()
                            time.sleep(4)
                            self.scroll2Bottom(self.driver)
                    else:
                        print('find all')
            print('return TRUE')
            return True
        except Exception as e:
            print(e)
            return False

    def downloadImg(self,dir):
        #all images are displayed
        if not os.path.exists(dir):
            return '{0} not exist'.format(dir)

        images = self.driver.find_elements_by_xpath("//img[@class='rg_ic rg_i']")
        for img in images:
            src = img.get_attribute('src')
            name = img.get_attribute('name').replace(':','')
            localfile = os.path.join(dir, name+'.jpeg')

            print(src)
            if src.startswith('http'):
                print(src)
                self.downing(src,localfile)
                print('download http img:{0}'.format(localfile))
            elif src.startswith('data'):
                pass
                print('data')
                src=src.split(',')
                base64src = src[1]
                self.base64tofile(base64src,localfile)
                print('download base64 img:{0}'.format(localfile))
            else:
                print('{0} is not acceptable'.format(src))

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
    gl = GoogleImagerLoader()

    # url = 'https://www.google.co.jp/search?q=indian+soldier&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiuooKpir_WAhUEbbwKHSkFAhgQ_AUICigB&biw=1280&bih=918'
    # url = 'https://www.google.co.jp/search?biw=1280&bih=891&tbm=isch&sa=1&q=panda&oq=panda&gs_l=psy-ab.3..0l4.7492922.7493353.0.7493725.5.5.0.0.0.0.364.600.2-1j1.2.0....0...1.1.64.psy-ab..3.2.598....0.p3LH4YJFKZs'
    # targetdir = r'd:\img\samples\resultbyurl'
    # gl.searchImgByUrl(url)
    # gl.downloadImg(targetdir)

    resultbyimgdir = r'd:\img\samples\resultbyimg'

    wk = os.walk(r'd:\img\samples\searchbyimg')
    for path,subpath,files in wk:
        for file in files:
            imgfilepath = os.path.join(path,file)

            targetfile = os.path.join(resultbyimgdir,os.path.splitext(file)[0]+'.htm')

            if gl.searchImgByImg(imgfilepath):
                print(targetfile)
                gl.savePages(targetfile)
                time.sleep(10)
