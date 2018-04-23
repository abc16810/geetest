# coding: utf-8
from selenium import webdriver
from geetest import BaseGeetestCrack

import time




class Run(BaseGeetestCrack):

    """工商滑动验证码破解"""
    def __init__(self, driver):
        super(Run, self).__init__(driver)

    def crack(self):
        """执行破解程序"""
        print("自动输入内容")
        self.input_by_id()
        print("单击提交按钮")
        self.click_by_id()
        time.sleep(2)
        x_offset = self.calculate_slider_offset()
        self.drag_and_drop(x_offset = x_offset)




def main():
    
    #options = Options()
    #options.add_argument('-headless')  # 无头参数
    # 使用第三方firfox浏览器驱动
    #driver = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    driver.get('http://gsxt.hljaic.gov.cn/index.jspx')
    cracker = Run(driver)
    cracker.crack()
    


if __name__ == '__main__':
    main()
