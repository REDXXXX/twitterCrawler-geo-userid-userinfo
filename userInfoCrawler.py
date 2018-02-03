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
def init():
    global twitter, arguments, tid_list

    credentials = []
    with codecs.open("cred.txt",'r','utf-8') as fr:
        for l in fr:
            credentials.append(l.strip())
    twitter = Twython(credentials[0], credentials[1], credentials[2], credentials[3])

    tid_list = []
    #nextSum.append(-1)
    countList=[]
    with codecs.open('parse.json.JsonOut','r','utf-8') as fr:
        for l in fr:
            #jobj = json.loads(l.strip())
            #tid = jobj['tweet_id']
            # tid = jobj
            tid_list.append(l.strip())  # 提取出tid
    fr.close()
    file2=codecs.open('userInfoCount.txt','r','utf-8')
    temp=file2.readlines()
    for l in temp:
        countList.append(l)
    if len(countList)>0:
        count=countList[-1].strip()
    else:
        count=0
    print(len(tid_list))
    return tid_list,count
def download(tid_list,count):
    with codecs.open("userInfo.txt",'a','utf-8') as uT,codecs.open('userInfoCount.txt','a','utf-8') as c:
        #for i in range(2000000):
        id=tid_list[count]
        #print(ids)
        jobjs = []
        print('正在爬取第 %d组数组'%count)
        c.write(str(count) + '\n')
        try:
            jobjs = twitter.lookup_user(user_id=id)
            #print(jobjs)
            content=jobjs[0]
            id_str=content['id_str']
            name=content['name']
            location=content['location']
            time_zone=content['time_zone']
            lang=content['lang']
            uT.write(id_str+';'+str(name)+';'+str(location)+';'+str(time_zone)+';'+str(lang)+'\n')
            c.write(str(count)+'\n')
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
'''


def download(nextSum):
    try:
        global twitter,tid_list
        #with open(arguments.inputfile + ".JsonOut", "w") as fwJson, open(arguments.inputfile + ".TweetOut", "w") as fwTweet:
        with codecs.open("userTwitter.JsonOut",'a',"utf-8") as fwJson, codecs.open("userTwitter.TweetOut", "a","utf-8") as fwTweet:
            next=nextSum[-1]
            while next!=0:
                print("yes1");
                jobjs = twitter.get_followers_ids(user_id="27260086",cursor=next);
                print(jobjs);
                #fwJson.write(str(jobjs))
                ids = jobjs["ids"];
                for l in ids:
                    fwJson.write(str(l)+"\n");
                next = jobjs["next_cursor"]
                nextSum.append(next);
                fwTweet.write(str(next)+'\n');
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
    os.remove("userTwitter.JsonOut");
    os.rename('temp.txt',"userTwitter.JsonOut");
'''


def main():
    #nextSum=[]
    tid_list,count=init()
    #枚十五分钟执行一次
    second=30;
    print("Start time: " +str(datetime.datetime.now().time()))
    #count=0;
    #download(nextSum)
    count=int(count)
    while count<5000000:
        print("当前第 %d 次运行"%(count));
        #time.sleep(second);
        download(tid_list,count)
        count=count+1;
    print("Completed time: " +str(datetime.datetime.now().time()))

if __name__ == "__main__":
    main()
