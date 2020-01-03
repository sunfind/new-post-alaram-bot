#!/usr/bin/env python

# encoding=utf-8



import requests

import time

from bs4 import BeautifulSoup

import telegram



bot = telegram.Bot(token='1040931523:AAEeJCG1Ta8zf3vQSo0-sqkknNqE1oeYyN8')



if __name__ == '__main__':

    # 제일 최신 게시글의 번호 저장
    latest_num = 0
    while True:
        req = requests.get('http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu')
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find("tr", {"class" : "list1"})
        post_num = posts.find("td", {"class" : "eng list_vspace"}).text


        # 제일 최신 게시글 번호와 30초 마다 크롤링한 첫번째 게시글의 번호 비교
        # 비교 후 같지 않으면 최신 게시글 업데이트 된 것으로 텔레그램 봇으로 업데이트 메시지 전송
        if latest_num != post_num :
            latest_num = post_num
            link = 'http://www.ppomppu.co.kr/zboard/'+posts.find("td", { "valign" : "middle"}).find("a").attrs['href']
            title = posts.find("font", {"class" : "list_title"}).text

            text = '<뽐뿌 게시글 업데이트>'+'\n'+title+'\n'+link
            bot.sendMessage(-265645381, text)
            # 프롬프트 로그
            print(post_num)
            print(title)
            print(link)
        time.sleep(30) # 30초 간격으로 크롤링
        print('bot 동작 중 현재 게시글 번호' + latest_num)