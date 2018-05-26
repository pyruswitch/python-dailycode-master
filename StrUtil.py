__author__ = 'wuhan'

import re


def find_Phone_Num(str):
    # 将正则表达式编译成Pattern对象
    a = ""
    pattern = re.compile(r'\d{5,13}')
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    match = pattern.findall(str)
    if match:
        # 使用Match获得分组信息
        a = ",".join(match)
        # print(a)

    return a


def find_name(str):
    i = str.find("电话")
    print(i)
    if i > 0:
        return str.split("电话")[0]
    else:
        return str


def substr(mainstr, startstr, endstr):
    try:
        start_index = mainstr.index(startstr) + len(startstr)
        try:
            end_index = mainstr.index(endstr, start_index + 1)
            return mainstr[start_index:end_index]
        except:
            return mainstr[start_index:]
    except:
        try:
            return mainstr[0:mainstr.index(endstr)]
        except:
            return mainstr


if __name__ == '__main__':
    print(substr(
        "(紫翔公寓17号)烟台驻深圳办事处(罗湖区南湖街道和平社区沿河东路15号).xlsx ",
        "#", "("))