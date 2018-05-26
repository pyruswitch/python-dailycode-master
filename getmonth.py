__author__ = 'vincent'
import datetime


def getBetweenDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y/%m")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)

    return set(date_list)


if __name__ == '__main__':
    #list1,list2,list3,list4,list5,list6=incomedata()
    #print(list1,'\n',list2,'\n',list3,'\n',list4,'\n',list5,'\n',list6)
    list1=getBetweenDay("2017-09-20" ,"2017-11-21")
    print(list1)