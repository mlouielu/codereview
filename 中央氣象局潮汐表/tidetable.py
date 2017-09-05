# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


# 潮汐資料物件
# from Tidal import (
#     TidalObject
# )

class GetTidal:
    """
    中央氣象局潮汐取得
    """
    # 對應字典
    tidalDict: {str: str} = {"彭佳嶼基隆海面": "NSea01",
                             "新竹鹿港沿海": "NSea02",
                             "鹿港東石沿海": "NSea04",
                             "東石安平沿海": "NSea05",
                             "安平高雄沿海": "NSea06",
                             "高雄枋寮沿海": "NSea07",
                             "枋寮恆春沿海": "NSea08",
                             "鵝鑾鼻沿海": "NSea09",
                             "成功臺東沿海": "NSea10",
                             "臺東大武沿海 ": "NSea10_1",
                             "花蓮沿海": "NSea12",
                             "澎湖海面": "NSea14",
                             "馬祖海面": "NSea15",
                             "金門海面": "NSea16",
                             }
    HTML_PARSER = "html.parser"
    HTML_Html5 = "html5lib"
    # 預設台南, 嘉義 NSea05
    keyword: str = "NSea06"
    head_URL = "http://www.cwb.gov.tw/V7/forecast/fishery/"
    tail_URL = "_1.htm"

    LIST_URL = "http://www.cwb.gov.tw/V7/forecast/fishery/" + keyword + "_1.htm"
    def __init__(self , keyword):
        self.keyword = keyword

    def get(self, areaText: str) -> str:
        # 替換 keyword
        URL = self.head_URL + self.keyword + self.tail_URL
        list_req = requests.get(URL)

        if list_req.status_code == requests.codes.ok:
            soup = BeautifulSoup(list_req.content, self.HTML_Html5)
            # print(soup)
            table = soup.find("table")
            # print(table)
            headings = [th.get_text() for th in table.find_all("td")]
            print(headings)
            arrayIndex = 0
            for index, text in enumerate(headings):
                try:
                    tt = str(text).split(" ")[1][:2]
                    if tt == areaText:
                        arrayIndex = index
                except:
                    continue

            return self.outputText(texts=headings, index=arrayIndex)

        else:
            return "request error"

    def outputText(self, texts , index: int) -> str:

        # 物件操作
        tidal = TidalObject.TidalObject()

        try:
            areaString = texts[index]
        except:
            return 'IndexError: list index out of range'
        try:
            tidal.area = str(areaString).rsplit(" ")[1][:2]
        except:
            return 'IndexError: list index out of range'
        try:
            tidal.tidalState = texts[index + 1]
        except:
            tidal.tidalState = ' '

        tidal.tidalTime_1_1 = texts[index + 2] + texts[index + 3]
        tidal.waterLevel_1_1 = texts[index + 5]
        tidal.tidalTime_1_2 = texts[index + 7] + texts[index + 8]
        tidal.waterLevel_1_2 = texts[index + 10]

        tidal.tidalTime_2_1 = texts[index + 12] + texts[index + 13]
        tidal.waterLevel_2_1 = texts[index + 15]
        tidal.tidalTime_2_2 = texts[index + 17] + texts[index + 18]
        tidal.waterLevel_2_2 = texts[index + 20]

        # outputs
        msg = "\n" + \
              tidal.area + "   " + tidal.tidalState + \
              "\n" + \
              tidal.tidalTime_1_1 + \
              "  " + tidal.waterLevel_1_1 + "\n" + \
              tidal.tidalTime_1_2 + \
              "  " + tidal.waterLevel_1_2 + "\n" + \
              tidal.tidalTime_2_1 + \
              "  " + tidal.waterLevel_2_1 + "\n" + \
              tidal.tidalTime_2_2 + \
              "  " + tidal.waterLevel_2_2 + "\n"
        return msg

if __name__ == "__main__":
    object = GetTidal(keyword="NSea06")

    msg = object.get(areaText="左營")
    print(msg)
	
	
class TidalObject:
    # 台南市
    area = ""
    # 潮汐時間
    tidalTime_1_1 = ""
    tidalTime_1_2 = ""

    tidalTime_2_1 = ""
    tidalTime_2_2 = ""

    # 潮汐水位
    waterLevel_1_1 = ""
    waterLevel_1_2 = ""

    waterLevel_2_1 = ""
    waterLevel_2_1 = ""

    # 潮汐狀態
    tidalState = ""

    def setArea(self,area):
        # 台南市
        self.area = area

