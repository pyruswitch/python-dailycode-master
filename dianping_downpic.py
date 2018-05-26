__author__ = 'wuhan'

from down_load_pic import DownLoadPic as dlp
import DAO
import threading


class DianpingDownloadPic(threading.Thread):
    def __init__(self, categoryId, name=""):
        self.categoryId = categoryId
        threading.Thread.__init__(self, name=name)
        self.dao = DAO.Dao()
        self.dLP = dlp()
        query_sql = " SELECT b.`shopType`,b.`categoryId` ,a.`city_name`,shopId,defaultPic, POSTER_PATH  FROM shop_bean a ,categorytoshengchan b " \
                    "WHERE a.`categoryId` = b.`categoryId` AND POSTER_PATH IS NULL AND defaultPic IS NOT NULL AND defaultPic <> '' and  b.`categoryId`  ='{}' ".format(
            categoryId)
        self.result = dao.execute_query(query_sql)
        query_sql = "SELECT cityname,cityenname FROM dianping_cities  WHERE STATUS=0"
        self.cityNames = dao.execute_query(query_sql)

    def run(self):
        if self.result is not None:
            self.downloadPic(self.result)
        print(str(self.categoryId) + "结束")

    def cityNameToEn(self, cityName):
        for dbcityname, dbcityenname in self.cityNames:
            if ( dbcityname == cityName ):
                return dbcityenname
        return "error"

    def downloadPic(self, result):
        for shopType, categoryId, cityName, shopId, picUrl, posterPath in result:
            cityEnName = self.cityNameToEn(cityName)
            if cityEnName == "error":
                return None
            # /poster/ 是从磁盘根目录开始， poster/ 是从项目根目录开始
            posterPath = '/poster/' + cityEnName + '/' + shopType + '/' + categoryId + '/' + shopId + '/' + '1.jpg'
            key = self.dLP.download_pic_from_url(picUrl, posterPath)
            update_query = "update shop_bean set POSTER_PATH = '{}' where shopId='{}' and city_name = '{}'  ".format(
                posterPath,
                shopId,
                cityName)
            if key == True:
                self.dao.execute_dmls(update_query)


if __name__ == '__main__':
    querysql = " SELECT DISTINCT a.categoryId FROM shop_bean a ,categorytoshengchan b WHERE a.`categoryId` = b.`categoryId`  "
    dao = DAO.Dao()
    cateIds = dao.execute_query(querysql)
    threads = []
    files = range(len(cateIds))
    for categoryId in cateIds:
        thread = DianpingDownloadPic(categoryId[0])
        threads.append(thread)
    for i in files:
        threads[i].start()

