#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import json

a = "{\n        StudentSystemStatisticsPage(query: \"{\\\"teamstate\\\":1}\",page: 1, sort: \"{\\\"ctime\\\":\\\"desc\\\"}\"){\n            totalPages\n            totalElements\n            content {\n              studentid\n              username\n              usernum\n              nickname\n              ctime\n              utime\n              basepainting\n              birthday\n              mobile\n              mobilecity\n              mobileprovince\n              head\n              sex\n              currentsuper\n              currentlevel\n              currentunit\n              currentlesson\n              currenttotal\n              orderid\n              packagescourseweek\n              packagescourseday\n              packagesname\n              packagestype\n              sup\n              teacherid\n              teamid\n              term\n              addedgroup\n              addedwechat\n              teamname\n              teamstate\n              realname\n              departmentname\n              expressstatus\n              expresscount\n              follow\n              isnoactive\n              noactivecount\n              isactive\n              activecount\n              istask\n              taskcount\n              isflag\n              flagcount\n              devicetype\n              lastlogintime\n              isrefund\n              trialcurrentlesson\n              trialteamname\n              trialrealname\n              trialdepartmentname\n            }\n          }\n        }\n      "
b = a.replace("\n", "").replace('\\', "").replace("              ", ",").replace("            ", "|")
print(b)
'''
{StudentSystemStatisticsPage(query:"{"teamstate":1}",page:1,sort:"{"ctime":"desc"}")
{totalPagestotalElementscontent{studentidusernameusernumnicknamectimeutimebasepaintingbirthdaymobilemobilecitymobileprovinceheadsexcurrentsupercurrentlevelcurrentunitcurrentlessoncurrenttotalorderidpackagescourseweekpackagescoursedaypackagesnamepackagestypesupteacheridteamidtermaddedgroupaddedwechatteamnameteamstaterealnamedepartmentnameexpressstatusexpresscountfollowisnoactivenoactivecountisactiveactivecountistasktaskcountisflagflagcountdevicetypelastlogintimeisrefundtrialcurrentlessontrialteamnametrialrealnametrialdepartmentname}}}

'''
