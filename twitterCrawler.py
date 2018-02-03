import json,requests;
import linecache;
import sys
import codecs
import os
import argparse
import time
import datetime
from collections import OrderedDict
from twython import Twython,TwythonError,TwythonRateLimitError
#怎么写？首先给定初始的id，然后获得一匹id，随后根据这初始id获取。
#将所有的id放在 suerTable.txt里。然后是，userResult.txt里放
#然后，检查所有的id，去除重复。

#步骤一，初始化接口

MAX_LOOKUP_NUMBER = 100
#SLEEP_TIME = 15 + 1
SLEEP_TIME = 5
twitter = None
arguments = None
tid_list = None
def init(nextSum):
    global twitter, arguments, tid_list

    credentials = []
    with codecs.open("cred.txt",'r','utf-8') as fr:
        for l in fr:
            credentials.append(l.strip())
    twitter = Twython(credentials[0], credentials[1], credentials[2], credentials[3])

    tid_list = []
    with codecs.open('parse.json.JsonOut','r','utf-8') as fr:
        for l in fr:
            #jobj = json.loads(l.strip())
            #tid = jobj['tweet_id']
            # tid = jobj
            tid_list.append(l.strip())  # 提取出tid
    print(len(tid_list))
    file=codecs.open('count.txt','r','utf-8')
    temp=file.readlines()
    file.close()
    countList=[]
    if len(temp)>0:
        for l in temp:
            countList.append(l.strip())
        count=int(countList[-1])
    else:
        count=0
    with codecs.open("userTwitterSecond.txt",'a','utf-8') as uT,codecs.open('count.txt','a','utf-8') as c:
        for i in range(count+1,len(tid_list)):
            ids=tid_list[i]
            #print(ids)
            jobjs = []
            print('正在爬取第 %d组数组'%i)
            c.write(str(i) + '\n')
            try:
                jobjs = twitter.get_user_timeline(user_id=ids,count=200)
                #print(jobjs)
                flag=False
                max_id=None
                for content in jobjs:
                    id=content['id_str']
                #print(id)
                    time1=content['created_at']
                #print(time)
                    geo=content['geo']
                #print(geo)
                    coordinates=content['coordinates']
                #print(coordinates)
                    places=content['place']
                #print(places)
                    if places!=None:
                        uT.write(ids+";"+id+";"+time1+";"+str(geo)+";"+str(coordinates)+";"+str(places)+"\n")
                    if geo!=None or coordinates!=None or places!=None:
                        #如果找到了地理位置信息，那么就获取它所有的信息
                        flag=True
                        max_id=id
                nextSum.append(i)
                while flag==True:
                    jobjs=twitter.get_user_timeline(user_id=ids,count=200,max_id=max_id)
                    flag=False
                    originMaxId=max_id
                    #max_id=None
                    for content in jobjs:
                        id = content['id_str']
                        # print(id)
                        time1 = content['created_at']
                        # print(time)
                        geo = content['geo']
                        # print(geo)
                        coordinates = content['coordinates']
                        # print(coordinates)
                        places = content['place']
                        # print(places)
                        if places!=None:
                            uT.write(ids + ";" + id + ";" + time1 + ";" + str(geo) + ";" + str(coordinates) + ";" + str(places) + "\n")
                            # 如果找到了地理位置信息，那么就获取它所有的信息
                        max_id = id
                    if max_id != originMaxId:
                        flag=True
                    else:
                        flag=False
            except TwythonRateLimitError as e:
                time.sleep(300)
            except TwythonError as e:
                print(repr(e))


            #ids=jobjs["ids"];
            #for l in ids:
                #fwJson.write(str(l)+"\n");
            #fwJson.write(str(jobjs))
            #print(str(jobjs));
            #fwJson.close();
            #next=jobjs["next_cursor"]
            #nextSum.append(next);



def download(nextSum):
    try:
        global twitter,tid_list
        #with open(arguments.inputfile + ".JsonOut", "w") as fwJson, open(arguments.inputfile + ".TweetOut", "w") as fwTweet:
        with codecs.open("userTwitter.JsonOut",'a',"utf-8") as fwJson, codecs.open("userTwitter.TweetOut", "a","utf-8") as fwTweet:
            next=nextSum[-1]
            while next!=0:
                print("yes1");
                jobjs = twitter.lookup_status(id="17919972");
                print(jobjs);
                fwJson.write(str(jobjs))
                #ids = jobjs["ids"];
                #for l in ids:
                    #fwJson.write(str(l)+"\n");
                #next = jobjs["next_cursor"]
                #nextSum.append(next);
                #fwTweet.write(next);
    except:
        checkRepeat()
        return nextSum

def checkRepeat():
    global arguments
    file=codecs.open('userTwitter.JsonOut','r','utf-8');
    temp=file.readlines();
    sum=len(temp);
    print("共有 %d 条数据"%(sum));
    file.close();
    outputDir="temp.txt";
    tempset=set();
    tempFile=codecs.open('temp.txt','w','utf-8')
    for line in temp:
        if line.strip() not in tempset:
            tempset.add(line.strip());
            tempFile.write(line.strip()+"\n");
    tempFile.close();
    tempFile=codecs.open("temp.txt",'r','utf-8');
    sum1=len(tempFile.readlines());
    print("去重后共有 %d 条记录"%(sum1));
    tempFile.close();
    os.remove(arguments.inputfile+".JsonOut");
    os.rename('temp.txt',arguments.inputfile+".JsonOut");



def main():
    nextSum=[]
    init(nextSum)
    #枚十五分钟执行一次
    '''
    second=5*60;
    print("Start time: " +str(datetime.datetime.now().time()))
    count=0;
    download(nextSum)
    while count<5000:
        print("当前第 %d 次运行"%(count));
        time.sleep(second);
        download(nextSum)
        count=count+1;
    print("Completed time: " +str(datetime.datetime.now().time()))
    '''
if __name__ == "__main__":
    main()


