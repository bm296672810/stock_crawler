# stock_crawler
该项目主要是爬取深交所所有股票的分时数据
本人ide用的是vscode，接下来主要是配置vscode下的python环境

## 1. vscode环境搭建参照(https://code.visualstudio.com/docs/python/environments)
## 2. python3 创建虚拟环境(本人使用的是3.8.3的环境)
   打开vscode的命令界面选择 Terminal: Create New Integrated Terminal 项
   创建虚拟环境 输入: python3 -m venv .venv
   创建完虚拟环境再次选择 Terminal: Create New Integrated Terminal 重新打开命令终端，不然无法执行下面的命令
   安装requests库 输入: python3 -m pip install requests

注:
其中 create.sql 是创建sqlite数据库的sql语句
main.py       python文件入口
request.py    发起http请求数据的接口
parse_json.py 请求到的json数据解析以及数据保存到数据库