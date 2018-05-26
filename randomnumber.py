__author__ = 'vincent'


def group(list):
    grouplist=[[]]
    list.sort()
    j=0
    grouplist[j].append(list[0])
    for i in range(0,len(list)-1):
        if list[i+1]-list[i]<=1:
            grouplist[j].append(list[i+1])
        else:
            j=j+1
            grouplist.append([])
            grouplist[j].append(list[i+1])
    print(grouplist)
if __name__ == '__main__':
    list=[8,10,5,6,100,103,18,22,56,3,4,14,13,12,11,1000,10001,10002]
    group(list)