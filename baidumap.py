# -*- coding:utf-8 -*-
import urllib.request
import json


class xBaiduMap:
    def __init__(self, key='your_key'):
        self.host = 'http://api.map.baidu.com'
        self.path = '/geocoder/v2/?'

        self.param = {
            'output': 'json',

            'ak': 'Rr3LxDiDvFidbqqzLtHfunxi',
        }

    def getSuggestion(self, address, city=None):
        result = []
        param = {
            'query': address,
            'region': city,
            'output': 'json',
            'ak': 'Rr3LxDiDvFidbqqzLtHfunxi'
        }
        url = "http://api.map.baidu.com/place/v2/suggestion?" + urllib.parse.urlencode(param)
        r = urllib.request.urlopen(url)
        rlt = json.loads(r.read().decode('UTF-8'))
        if rlt['status'] == 0:
            return rlt["result"]
        else:
            print("Decoding Failed")
            return None


    def getLocation(self, address, city=None):
        rlt = self.geocoding('address', address, city)
        if rlt != None:
            l = rlt['result']
            if isinstance(l, list):
                return None
            return l['location']

    def getAddress(self, lat, lng):
        rlt = self.geocoding('location', "{0},{1}".format(lat, lng))
        if rlt != None:
            l = rlt['result']
            return l['formatted_address']
            # Here you can get more details about the location with 'addressComponent' key
            # ld=rlt['result']['addressComponent']
            # print(ld['city']+';'+ld['street'])
            #

    def getAroundMerchent(self, lat, lng, queryStr, radius=5000):
        result = []
        param = {
            'query': queryStr,
            'location': "{0},{1}".format(lat, lng),
            'output': 'json',
            'page_size': 20,
            'page_num': 0,
            'radius': radius,
            'scope': '2',
            'ak': 'Rr3LxDiDvFidbqqzLtHfunxi'

        }
        for i in range(0, 1000):
            try:
                param['page_num'] = i
                r = urllib.request.urlopen("http://api.map.baidu.com/place/v2/search?" + urllib.parse.urlencode(param))
                rlt = json.loads(r.read().decode('UTF-8'))
                if rlt['message'] == 'ok':
                    if rlt != None:
                        result = result + rlt['results']
                    else:
                        break
                else:
                    break
            except Exception as e :
                print(param)
                print(e)
                return result
        return result

    def geocoding(self, key, value, city=None):

        if key == 'location':
            if 'city' in self.param:
                del self.param['city']
            if 'address' in self.param:
                del self.param['address']

        elif key == 'address':
            if 'location' in self.param:
                del self.param['location']
            if city == None and 'city' in self.param:
                del self.param['city']
            else:
                self.param['city'] = city
        self.param[key] = value
        r = urllib.request.urlopen(self.host + self.path + urllib.parse.urlencode(self.param))
        rlt = json.loads(r.read().decode('UTF-8'))
        if rlt['status'] == 0:
            return rlt
        else:
            print("Decoding Failed")
            return None


if __name__ == '__main__':
    bm = xBaiduMap()
    zuobiao = bm.getAddress("32.04687", "120.859085")
    print(zuobiao)
    # print(str(zuobiao[1]) + "," + str(zuobiao[0]))
    #lo = bm.getAddress(33.967198, 116.809014)
    #print(lo)
    # merlist = bm.getAroundMerchent(22.656673, 114.06553, "银行")
    # print(merlist)