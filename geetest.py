# coding: utf-8
from selenium.webdriver import ActionChains
import time
import uuid
from io import BytesIO
from PIL import Image



class BaseGeetestCrack(object):

    """验证破解基础类"""
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    def input_by_id(self, text='中国移动', element_id='searchText'):
        """
        :text: 要输入的文本
        :element_id: 输入框网页元素id

        """
        input_el = self.driver.find_element_by_id(element_id)
        input_el.clear()
        input_el.send_keys(text)
        time.sleep(3)


    def click_by_id(self,element_id='click'):
        
        """点击查询按钮
        :element_id: 查询按钮网页元素id
        """
        search_el = self.driver.find_element_by_id(element_id)
        search_el.click()
        time.sleep(3)

    

    def calculate_slider_offset(self):
        """计算滑块偏移位置，必须在点击查询按钮之后调用
        :returns: Number
        """
        # 截取原始的滑动图片
        img1 = self.crop_captcha_image()
        self.click_to_element()
        # 在源目标上按住鼠标左键偏移5像素
        #self.drag_and_drop(x_offset=10)
        img2 = self.crop_captcha_image()
        w1, h1 = img1.size
        w2, h2 = img2.size
        if w1 != w2 or h1 != h2:
            return False
        left = 0
        flag = False

        left = 0
        flag = False
        for i in range(61, w1):
            for j in range(h1-25):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    flag = True
                    break
            if flag:
                break
        left -= 5
        print(left)
        return left


    def crop_captcha_image(self, element_id="gt_box"):
        """截取验证码图片
        :element_id: 验证码图片网页元素id
        :returns: StringIO, 图片内容
        """
        captcha_el = self.driver.find_element_by_class_name(element_id)
        size = captcha_el.size
        left = int(captcha_el.location['x'])
        top = int(captcha_el.location['y'])
        right = int(captcha_el.location['x'] + size['width'])
        bottom = int(captcha_el.location['y'] +  size['height'])
        print(left, top, right, bottom)

        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        captcha  = screenshot.crop((left, top, right, bottom))
        captcha.save("%s.png" % uuid.uuid4().hex)
        return captcha

    def drag_and_drop(self, x_offset=0, y_offset=0, element_class="gt_slider_knob"):
        """拖拽滑块
        :x_offset: 相对滑块x坐标偏移
        :y_offset: 相对滑块y坐标偏移
        :element_class: 滑块网页元素CSS类名
        """
        dragger = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)
        print(x_offset)
        #action.click_and_hold(dragger)
        #action.pause(1)
        #action.move_by_offset(x_offset-10,y_offset)
        #action.move_by_offset(10,y_offset).release().perform()
        #action.move_by_offset(-10,y_offset).release().perform()
        #action.drag_and_drop_by_offset(dragger, x_offset, y_offset).perform()
        # 这个延时必须有，在滑动后等待回复原状
        action.click_and_hold(dragger).move_by_offset(x_offset,y_offset).release().perform()
        time.sleep(3)

    def is_pixel_equal(self, img1, img2, x, y):
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        # 凹进出的部分 和原图的像素比较
        if (abs(pix1[0] - pix2[0] < 60) and abs(pix1[1] - pix2[1] < 60) and abs(pix1[2] - pix2[2] < 60)):
            return True
        else:
            return False

    def click_to_element(self, element_class="gt_slider_knob"):
        """鼠标移动在网页元素上单击左键
        :element: 目标网页元素
        """
        element = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)
        action.click_and_hold(element).release().perform()
        time.sleep(4)
