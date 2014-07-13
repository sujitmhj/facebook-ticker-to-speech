#!/usr/bin/env python
# encoding: utf-8
from lxml import html
import urllib3
import json
pool = urllib3.PoolManager()
import urllib
import pyttsx
engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)


def main():

	params = {}
	params["channel"]="p_38441776904"
	params["seq"] =0
	params["partition"] = -2
	params["clientid"]="172ad47c"
	params["cb"]="303l"
	params["idle"]="11"
	params["cap"]=0
	params["sticky_token"] = 419
	params["state"] = "active"
	params["mode"] = "stream"
	params["format"]="json"

	while(True):
	    path = "/pull?"+urllib.urlencode(params)
	    headers = {
	    "host":"1-channel-proxy-07-ash2.facebook.com",
	    "method":"GET",
	    "path":path,
	    "scheme":"https",
	    "version":"HTTP/1.1",
	    "accept":"*/*",
	    "accept-encoding":"gzip,deflate,sdch",
	    "accept-language":"en-US,en;q=0.8",
	    "cache-control":"no-cache",
	    "cookie":"lu=gQlPjiQEMb7GdiecOzmTuld16Q; datr=edGEUt0hP2Q1-PZhha4DKBaJ; js_ver=1645; c_user=1741776904; fr=06jldMROAkuNWly9e.AWX10vnDRuUOFzQSsye0xpRMDeQ.BShNJj.bA.FO7.AWWS6ATV; xs=220%3A3BJPMCwvwx4pBg%3A2%3A1404112224%3A18283; csm=2; s=Aa5EoZ_ZHg3fm87M.BTsQ1g; p=-2; act=1404956701168%2F213; presence=EM404956750EuserFA21741776904A2EstateFDsb2F0Et2F_5b_5dElm2FnullEuct2F1404954545BEtrFA2loadA2EtwF374166710EatF1404956736087G404956750385CEchFDp_5f1741776904F27CC",
	    "origin":"https://www.facebook.com",
	    "pragma":"no-cache",
	    "referer:https":"//www.facebook.com/",
	    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
	    }
	    r = pool.request('GET', 'https://1-channel-proxy-06-ash2.facebook.com'+path,
	                      headers = headers
	                      )

	    response = "[" + r.data.replace("for (;;);", "").replace("}\n{","},{") +"]"

	    json_response = json.loads(response)
	    print json_response
	    for res in json_response:
	        if res.get('t') == "msg":
	            messages = res.get("ms")

	        if res.get("seq") != None:
	            params["seq"] = res.get("seq")
	        if res.get("tr") !=None:
	            params["traceid"] = res.get("tr")

	            for msg in messages:
	                if msg.get("type")=="ticker_update:home":
	                    html_page = msg.get("story_xhp")
	                    tree = html.fromstring(html_page) # corrected, used to be `lxml.html.fromstring`
	                    xp = "//div[@class='tickerFeedMessage fwn']"
	                    xp_username = "//span[@class='fwb']"
	                    try:
	                        content= tree.xpath(xp)[0]
	                        actor = content.xpath(xp_username)[0].text
	                        message = content.xpath("./text()")[0]
	                        engine.say(actor)

	                        engine.say(message)
	                        engine.runAndWait()
	                        print actor, message
	                    except:
	                        print json_response

	                if msg.get("seq") !=None:
	                    params["seq"] = msg.get("seq")
	                if msg.get("tr") !=None:
	                    params["traceid"] = msg.get("tr")

if __name__== "__main__":
	main()	                 
