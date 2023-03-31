import requests
from bs4 import BeautifulSoup
import xlwt
import os
import re
def get(url):
  return requests.get(url)

re_url_path = re.compile('[\/\/](.[^\/]*?)[\/]{1}')
re_find_text = re.compile(r'<span.*?>([\s\S]*?)</span*?>',re.M)
re_find_title = re.compile(r'<title.*?>([\s\S]*?)</title*?>',re.M)
def save_data(sheet_name:str,data: list,save_path:str):
  print('save data to file...',sheet_name)
  book = xlwt.Workbook(encoding='utf-8', style_compression=0)
  sheet = book.add_sheet(sheet_name, cell_overwrite_ok=True)
  for i in range(len(data)):
      for j in range(len(data[i])):
          sheet.write(i, j, data[i][j])
  book.save(save_path)
  print('saved done!')
def catch_site(url:str,is_title:bool=False):
  res = get(url)
  res.encoding = 'gbk2312'
  content = BeautifulSoup(res.text, 'html.parser')
  data_list = content.find_all('tr')
  title = content.find_all('title')
  save_raw_path = re.sub(r'\.','_',re_url_path.search(url).group(1))
  save_path ='./data'+ save_raw_path + '.xls'
  data_info = []
  xls_name = save_raw_path[1:]
  if re_find_title.findall(str(title))[0]:
    save_path = './data/' + re_find_title.findall(str(title))[0] + '.xls'
  for i in range(len(data_list)):
      text = re.findall(re_find_text,str(data_list[i]))
      if text:
        if i == 0 and is_title:
          xls_name = text[0]
        else:
          for i in range(len(text)):
            if text[i] == '<br/>':
              text[i] = ''
          data_info.append(text)
  save_data(xls_name,data_info,save_path)
  
 