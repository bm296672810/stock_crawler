import parse_json as pj
import request as rq
# r = requests.get("http://www.szse.cn/certificate/individual/index.html?code=000001")
# r = requests.get("http://www.szse.cn/api/market/ssjjhq/getTimeData?random=0.6166297118126336&marketId=1&code=000001")

if __name__ == "__main__":
    # run = True
    # page_num = 1
    # while run:
    #     stock_list_data = rq.get_stock_list(page_num)
    #     page_info = pj.parse_stock_list(stock_list_data)
    #     if page_info[0] >= page_info[1]:
    #         run = False
    #     else:
    #         page_num = page_info[0] + 1
    
    codes = pj.get_all_code()

    for code in codes:
        json_response = rq.get_time_data(code)
        pj.parse_data_json(json_response)

