from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city1 = os.environ['CT']
city2 = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id1 = os.environ["USER_ID1"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather_sz():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?key=dea7a9c908b78514f61678bce2969a8f&city="+city1+"&extensions=all&output=JSON"
  res = requests.get(url).json()
  weather = res['forecasts'][0]['casts'][0]['dayweather']
  temp=res['forecasts'][0]['casts'][0]['daytemp']
  return weather, int(temp)

def get_weather_tz():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?key=dea7a9c908b78514f61678bce2969a8f&city="+city2+"&extensions=all&output=JSON"
  res = requests.get(url).json()
  weather = res['forecasts'][0]['casts'][0]['dayweather']
  temp=res['forecasts'][0]['casts'][0]['daytemp']
  return weather, int(temp)

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']





client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea_sz, temperature_sz = get_weather_sz()
wea_tz, temperature_tz = get_weather_tz()
data = {"weather_tz":{"value":wea_tz},"weather_sz":{"value":wea_sz},"temperature_tz":{"value":temperature_tz},"temperature_sz":{"value":temperature_sz},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words()}}
res = wm.send_template(user_id, template_id,data)
res = wm.send_template(user_id1,template_id,data)
print(res)
