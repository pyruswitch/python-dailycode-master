__author__ = 'wuhan'
import urllib.request
import time


class DownLoadPic():
    def download_pic_from_url(self, url, path):
        try:
            print(url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            request = urllib.request.Request(url=url, headers=headers)
            conn = urllib.request.urlopen(request, timeout=500)
            dir = path[0:path.rfind("/")]
            self.mkdir(dir)
            f = open(path, 'wb')
            f.write(conn.read())
            f.close()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def mkdir(dir):
        # 引入模块
        import os
        # 去除首位空格
        dir = dir.strip()
        # 去除尾部 \ 符号
        dir = dir.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(dir)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print(dir + ' 创建成功')
            # 创建目录操作函数
            os.makedirs(dir)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(dir + ' 目录已存在')
            return False


if __name__ == "__main__":
    for i in range(200, 300):
        count = 0
        for j in range(1, 200):
            time.sleep(5)
            a = str(i)
            b = str(j)
            if i < 10:
                a = "00" + a
            if i < 100:
                a = "0" + a
            if j < 100:
                b = "00" + b
            if j < 10:
                b = "0" + b

            url = "http://img.xiuren.com/taotu/{}/samples_o/{}.jpg".format(a, b)
            name = "test/423/{}.jpg".format(a + b)
            # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
            d = DownLoadPic()
            if d.download_pic_from_url(url, name):
                count = count + 1
            if count == 3:
                break
