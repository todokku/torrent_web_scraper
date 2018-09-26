#!/usr/bin/python
from datetime import datetime as dtime
import os
import web_scraper_01
import web_scraper_02
import web_scraper_lib

#####################################################################
# set you file path
# For example: 
# JD = JsonParser("/home/pi/localbin/web_scraper_settings.json")
#####################################################################
SETTING_FILE = "YOUR_FILE_PATH/web_scraper_settings.json"

if __name__ == '__main__':

    print("%s is going to work at %s." % (os.path.basename(__file__), dtime.now()))
    
    JD = web_scraper_lib.JsonParser(SETTING_FILE)
    webpage_max = JD.get('page_scrwap_max')
  
    # This list is to scrap websites.
    siteList = [web_scraper_01, web_scraper_02]
 
    for site in siteList:
        scraper = site.site_scraper(JD)
        
        #Step 1. test for access with main url
        print("====================================\n=> Try to access site : ", scraper.getMainUrl())
        if not scraper.checkMainUrl():
            continue
        
        #Step 2. Iterate category for this site
        for cateIdx in web_scraper_lib.getCateList():
            #print(cateIdx)
        
        #Step 3. setup Latest Id for this site/this category
            needNewLatestId = True
            print("scraping [%s][%s]" % (scraper.sitename, cateIdx))
        
        #Step 4. iterate page (up to 10) for this site/this category
            for count in range(1, webpage_max+1):
                #print(cateIdx, count)
                
                needKeepgoing = True
                cateIdxNo = web_scraper_lib.getCateIdxFromStr(cateIdx)
                
                url = scraper.getScrapUrl(cateIdxNo, count)
                        
                boardList = scraper.getParseData(url)
             
                #for board in boardList:
                for num, board in enumerate(boardList, start=1):
                    title = board.get_text().replace('\t', '').replace('\n', '')
                    href = board.get('href')
                    boardIdNum = scraper.get_wr_id(href)
                    #print("[%d][%d] - %s" % (num, boardIdNum, title))
                    
                    if needNewLatestId:
                        newLatestId = scraper.get_wr_id(href)
                        if newLatestId > 0:
                            #print("We set up for new latest ID %d." % newLatestId)
                            needNewLatestId = False
                        else:
                            print("Something wrong, cannot get new latest ID - %d." % newLatestId)

                    #boardList의 첫 게시물의 id를 확인
                    if num == 1:
                        if not (scraper.needKeepGoing(cateIdx, boardIdNum)):
                            needKeepgoing = False
                            break

                    if not web_scraper_lib.checkTitleWithProgramList(title):
                        continue

                    if not (scraper.needKeepGoing(cateIdx, boardIdNum)):
                        needKeepgoing = False
                        break

                    print("\t[%s][%s][%d][p. %d] - %s" % (scraper.sitename, cateIdx, boardIdNum, count, title))
                    #print("\t%s" % href)
                
                    magnet = scraper.getmagnetDataFromPageUrl(href)
                    #print("\t%s" % magnet)

                    web_scraper_lib.add_magnet_transmission_remote(magnet, JD)

                if not needKeepgoing:
                    break
        
        #Step 5. save scrap ID
            scraper.saveNewLatestIDwithCate(cateIdx, newLatestId)
        
    exit()
