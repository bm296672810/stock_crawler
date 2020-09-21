import requests
import random

# 根据股票代码请求当前交易日的分时数据
def get_time_data(code):
    random_num = random.uniform(0, 1)
    request_url = "http://www.szse.cn/api/market/ssjjhq/getTimeData?random=%0.16f&marketId=1&code=%s" % (random_num, code)
    print(request_url)
    r = requests.get(request_url)

    return r.content.decode()
# 拉取股票列表
def get_stock_list(page_num = 1):
    random_num = random.uniform(0, 1)
    # http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=%d&random=0.886758800604933
    request_url = "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=%d&random=%.16f" % (page_num, random_num)
    r = requests.get(request_url)
    return r.content.decode()