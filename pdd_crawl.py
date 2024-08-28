import uiautomator2 as u2
import time

class PDD:
    def __init__(self, shop, devices, account):
        """
        初始化PDD类，连接到设备并设置店铺名称。

        :param shop: 店铺名称
        :param devices: 设备的IP地址或序列号
        :param account: 要获取的商品数量
        """
        self.shop_name = shop
        self.device = u2.connect(devices)
        self.account = account

    def __get_current_package(self):
        """
        搜索当前界面的包名
        """
        current_package = self.device.app_current()['package']
        return current_package

    def __search(self):
        """
        在设备上执行搜索操作。
        """
        self.device(resourceId='com.xunmeng.pinduoduo:id/pdd').click()
        self.device.send_keys(self.shop_name)
        self.device(text='搜索').click()
        time.sleep(1)

    def __slide(self):
        """
        滑动浏览页面，并获取符合条件的商品详细信息。
        """
        temp_account = 1
        recent_elements = []
        detail_dict = {}
        while 1:
            elems = self.device.xpath('//*[contains(@text, "¥")]/following-sibling::*[1]').all()
            for elem in elems:
                if elem.text and elem.text not in recent_elements:
                    recent_elements.append(elem.text)
                    if len(recent_elements) >= 3:
                        recent_elements.pop(0)  # 移除最早添加的元素
                    elem.click()
                    #操作
                    detail = self.__get_detail()
                    detail_dict[temp_account] = detail
                    # 返回到上一级页面
                    self.device.xpath(
                        '//*[@content-desc="顶部工具栏"]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
                if temp_account >= self.account:
                    return detail_dict
                temp_account += 1  # 将该行移动到这里，确保每次处理都会增加计数器
            self.device.swipe_ext("up", 0.5)
            time.sleep(3)
    def __get_detail(self):
        """
        获取商品的详细信息，包括价格、标题和店名。

        :return: 包含商品详细信息的字典
        """
        detail = {}
        # 获取价格
        price = ''
        time.sleep(2)
        price_elements = self.device.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]').child(
            '//*').all()
        for elem in price_elements:
            if elem.text:
                price += elem.text
        detail['price'] = price
        # print(detail)

        # 获取标题
        time.sleep(1)
        Line_elements = self.device.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.support.v7.widget.RecyclerView[1]').child(
            'android.widget.LinearLayout').all()
        for num in range(1, len(Line_elements)+1):
            index = 0
            test_title_elements = self.device.xpath(
                f'//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[{num}]/android.view.ViewGroup').child(
                '//android.widget.TextView').all()
            for title in test_title_elements:
                if "正品" in title.text:
                    index = num
                    break
            if index != 0:
                break
        real_title_elements = self.device.xpath(
            f'//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[{index-1}]/android.widget.FrameLayout[1]').child(
            '//android.widget.TextView').all()
        real_title_list = []
        for temp_title in real_title_elements:
            real_title_list.append(temp_title.text)
        real_title = ''.join(real_title_list[0:2]) #得到标题

        # 向上滑动页面以获取更多内容
        self.device.swipe_ext("up", 1)
        self.device.swipe_ext("up", 0.5)
        self.device.swipe_ext("up", 0.3)

        # 获取店名
        num_elem = self.device.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.support.v7.widget.RecyclerView[1]').child(
        'android.view.ViewGroup').all()
        index = len(num_elem)
        store_elements = self.device.xpath(
            f'//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.support.v7.widget.RecyclerView[1]/android.view.ViewGroup[{index}]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.LinearLayout').child(
            'android.widget.TextView').all()
        for i in store_elements:
            store = i.text
        detail['store'] = store
        return detail

    def test(self):
        """
        用于调试私有函数模块
        """

        # self.device.swipe_ext("up", 1)
        # self.device.swipe_ext("up", 0.5)
        # self.device.swipe_ext("up", 0.3)
        real_title_list = []
        num_elem = self.device.xpath(
            ('//*[@resource-id="com.xunmeng.pinduoduo:id/tv_title"]')).child('android.widget.TextView').all()
        for temp_title in num_elem:
            real_title_list.append(temp_title.text)
        real_title = ''.join(real_title_list[0:2]) #得到标题
        print(real_title)




    def inspect_current_package(self):
        """
        检测当前页面是否为拼多多，若不是则打开拼多多
        """
        current_package = self.__get_current_package()
        if current_package != 'com.xunmeng.pinduoduo':
            self.device.app_start('com.xunmeng.pinduoduo')

    def search(self):
        self.__search()

    def run(self):
        """
        主方法，执行搜索并开始滑动浏览商品。

        :return: 包含所有商品详细信息的列表
        """
        self.inspect_current_package()
        self.__search()
        return self.__slide()  # 添加return语句以返回结果

# 使用示例
if __name__ == "__main__":
    devices = '8033712a'
    pdd = PDD('茅台', devices, 10)
    pdd.test()
    # result = pdd.run()
    # print(result)


