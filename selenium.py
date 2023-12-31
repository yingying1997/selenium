# 内置库
import time
# 加载驱动
from selenium import webdriver
# 定位元素
from selenium.webdriver.common.by import By
# 正则
import re

class JuJin(object):

    # 定义初始化方法
    def __init__(self):
        # 实例属性
        # 加载驱动
        self.driver = webdriver.Chrome()
        # 窗口最大化
        self.driver.maximize_window()
        # 加载网站
        self.driver.get('https://juejin.cn/')

    # 解析数据
    def parse_html(self):
        # 等待2秒
        time.sleep(2)
        # 获取 li 里的所有数据
        lis = self.driver.find_elements(By.XPATH, '//div[@class="entry-list list"]/li')
        # 循环处理数据
        for li in lis:
            # 捕获异常
            try:
                # 等待2秒
                time.sleep(2)
                # 获取文章标题标签
                a = li.find_element(By.CLASS_NAME, 'title')
                # 点击标题标签进入详情页
                self.driver.execute_script('arguments[0].click();', a)
                # 切换窗口到内容页
                self.driver.switch_to.window(self.driver.window_handles[1])
                # 等待2秒
                time.sleep(2)
                # 获取标题标签
                title = self.driver.find_elements(By.CLASS_NAME, 'article-title')
                # 获取文章内容标签
                contents = self.driver.find_elements(By.XPATH, '//div[@class="markdown-body cache"]/p')
                # 判断标题是否是空列表，如果是空列表，说明文章是广告文章
                if not title:
                    # 获取标题标签
                    title = self.driver.find_elements(By.XPATH, '//a[@class="title"]/span')
                    # 获取文章内容标签
                    contents = self.driver.find_elements(By.XPATH, '//div[@class="markdown-body"]/p')
                # 获取标题文本
                titles = title[0].text
                # 正则表达式替换标题特殊字符
                titles = re.sub(r'[,?/<>!: ()|"]', '', titles)
                # 定义组装数据的变量
                s = ''
                # 获取数据为列表，需循环取出
                for i in contents:
                    # 组装数据
                    s += i.text + '\n'
                # 打印文章标题，内容
                # print(titles)
                # 保存数据
                self.save_data(titles, s)
                # 关闭当前窗口
                self.driver.close()
                # 切换窗口到列表页
                self.driver.switch_to.window(self.driver.window_handles[0])
                # 等待1秒
                time.sleep(1)
            except Exception as e:
                # 打印异常
                print(e)
                print("没有文章内容")
                # 关闭当前窗口
                self.driver.close()
                # 切换窗口到列表页
                self.driver.switch_to.window(self.driver.window_handles[0])

    # 保存数据
    def save_data(self, title, contents):
        # 创建 txt 文本文档
        with open(f'掘金/{title}.txt', 'w', encoding='utf-8') as f:
            # 文件写入
            f.write(contents)

    # 滚动方法
    def slide(self, height):
        # 滑动滚动条
        self.driver.execute_script(
            f'window.scrollTo(0,{height})'
        )

    # 处理主逻辑
    def main(self):
        # 获取窗口的高度
        heights = self.driver.get_window_size()['height']
        # 滑动次数
        page = 1
        # 滑动
        while page <= 5:
            self.slide(heights)
            # 加高度
            heights = heights + heights
            # 滑动次数+1
            page += 1
            # 等待1秒
            time.sleep(1)
        # 解析数据
        self.parse_html()

# 创建对象
data = JuJin()
# 调用 main 方法，开始执行主程序
data.main()