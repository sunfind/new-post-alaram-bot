#!/usr/bin/env python

# encoding=utf-8



import requests

import time

from bs4 import BeautifulSoup

import telegram

import os



bot = telegram.Bot(token='1040931523:AAEeJCG1Ta8zf3vQSo0-sqkknNqE1oeYyN8')

# heroku 서버의 환경변수 사용하여 최신글 번호 업데이트

ppompu_latest_num = os.environ.get('PPOMPU_ID')



def ppomppu():

    global ppompu_latest_num
    req = requests.get('http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser') #, from_encoding='utf-8')
    posts = soup.find("tr", {"class" : "list1"})
    post_num = posts.find("td", {"class" : "eng list_vspace"}).text
  post_num.strip()

    # 스케쥴러가 10분 마다 제일 최신 게시글 번호와 크롤링한 최신 게시글 번호 비교
    # 비교 후 같지 않으면 최신 게시글 업데이트 된 것으로 텔레그램 봇으로 업데이트 메시지 전송
    if ppompu_latest_num != post_num :
        ppompu_latest_num = post_num
        # PPOMPU_ID 환경 변수 최신글의 번호로 업데이트
        os.environ["PPOMPU_ID"] = ppompu_latest_num.strip()
        link = 'http://www.ppomppu.co.kr/zboard/'+posts.find("td", { "valign" : "middle"}).find("a").attrs['href']
        title = posts.find("font", {"class" : "list_title"}).text
        text = '<뽐뿌 게시글 업데이트>'+'\n'+title+'\n'+link
        bot.sendMessage(-265645381, text)
        # 프롬프트 로그
        print(text)
     print(os.environ)

    print('bot 동작 중...현재 게시글 번호 ' + ppompu_latest_num.strip())
    print('heroku PPOMPU_ID 환경변수' + os.environ.get('PPOMPU_ID'))
if __name__ == '__main__':

    try:
        ppomppu()
    except AttributeError as e:
        print(e)