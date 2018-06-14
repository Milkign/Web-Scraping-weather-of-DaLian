from bs4 import BeautifulSoup  # 用来代替正则表达式取源码中相应标签的内容
import requests  # 用来抓取网页的html源代码
import csv
from matplotlib import pyplot

'''解析网页'''


def get_html(url):
    # 模拟浏览器来获取网页的html代码
    header = {  # 请求头（网页扒下来的）
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    # 解析网址，headers：请求头， timeout：超时30秒
    re = requests.get(url, headers=header, timeout=30)
    # 编码方式：中文
    re.encoding = "utf-8"
    # 返回解析出的txt文件
    return re.text


'''数据爬取'''


def get_data(html_txt):
    weather = []
    # 创建BeautifulSoup对象
    bs = BeautifulSoup(html_txt, "html.parser")
    # 获取body部分,找到id为7d的div,获取ul部分,获取所有的li
    w = bs.body.find("div", {"id": "7d"}).find("ul").find_all("li")

    # 对每个标签中的内容进行遍历
    for day in w:
        temp = []
        date = day.find("h1").string  # 获取日期
        inf = day.find_all("p")  # 找到li中的所有p标签
        temp.append(date)  # 将日期添加到temp 中
        temp.append(inf[0].string)  # 将第一个p标签中的内容添加到temp列表中红

        # 若当前为傍晚，则没有最高气温
        if inf[1].find("span") is None:
            temperature_high = None
        else:
            temperature_high = inf[1].find("span").string  # 最高气温
            temperature_high = temperature_high.replace("℃", "")

        temperature_lower = inf[1].find("i").string  # 最低气温
        temperature_lower = temperature_lower.replace("℃", "")
        temp.append(temperature_high)
        temp.append(temperature_lower)

        weather.append(temp)  # 将temp添加到weather列表中

    return weather


# 要爬取网址的链接
url = "http://www.weather.com.cn/weather/101070201.shtml"
# 解析链接
html = get_html(url)
# 获取数据
result = get_data(html)

# 控制台输出天气数据
for i in result:
    print(i)

'''数据处理'''

# 因为数据第一项是“13日（今天）”这样的，我们只要时间 所以只取字符串前两位（用字符串切片）
days = [int(i[0][:2]) for i in result]
# 最低气温为第4项，数据项下表从0开始，所以取i[3]的数据
minnum = [int(i[3]) for i in result]
# 创建最高气温列表
maxnum = []
# 若为傍晚，则当日不存在最高气温，所以只取从明日开始的气温
for i in result:
    if i[2] != None:
        maxnum.append(int(i[2]))

'''数据分析——气温折线图'''

'''最高气温'''
# 生成最高气温图表
pyplot.plot(days, minnum)
# 设置横坐标名称 纵坐标名称 标题
pyplot.xlabel('date')
pyplot.ylabel('temperature')
pyplot.title('min temperature')
# 显示图表
pyplot.show()

'''最低气温'''
# 若为傍晚，则当日不存在最高气温，所以只取从明日开始的日期
if len(maxnum) < len(days):
    days = days[1:]

# 生成最低气温图表
pyplot.plot(days, maxnum)
# 设置横坐标名称 纵坐标名称 标题
pyplot.xlabel('date')
pyplot.ylabel('temperature')
pyplot.title('max temperature')
# 显示图表
pyplot.show()
