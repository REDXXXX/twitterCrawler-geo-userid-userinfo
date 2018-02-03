# twitterCrawler-geo-userid-userinfo
#这个爬虫的使用事项如下：
  1.此爬虫是使用twitter的api进行爬取，并不是网页抓取。
  2.要使用此爬虫，请现在twitter developer里注册开发者账号，create app，然后获得consumer key，consumer secret，access token，access secret，
  然后按照这个顺序写在cred.txt里，一行一个
  3.userinfocrawler会爬取用户的个人信息
    twitterCrawler爬取用户的twitter。但只会保留用户的地理位置信息。因为之前的项目需要，所以我只需要用户的公开地理位置。
    userIdCrawler爬取用户的id。
  4.程序里面带有保存点，即使中断程序运行也没关系。再次运行的时候，它会自动从上次的保存点进行爬取。
    程序里面有去重函数，当速率超过的时候它会运行去重函数去除重复数据。
    程序里有速度超时处理。当爬取的次数达到限制时，程序会暂停运行一段时间。
  5.程序的运行，在cmd里cd到文件目录下 输入 python twitterCrawler.py 即可运行。其他两个爬虫的运行也相同。
