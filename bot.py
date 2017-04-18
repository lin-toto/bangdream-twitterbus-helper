#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from termcolor import colored
from config import *
import tweepy
import re
import signal
import sys

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def signal_handler(signal, frame):
    print('Ctrl+C - Quit')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def replace_number(str):
    return str.replace(u"０","0").replace(u"１","1").replace(u"２","2").replace(u"３","3").replace(u"４","4").replace(u"５","5").replace(u"６","6").replace(u"７","7").replace(u"８","8").replace(u"９","9")


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        bus = replace_number(status.text)
        bus_detail = []
        match = re.search(r"[0-9]{5}", bus)
        if match is None: return
        if u"しゅわ" in bus: bus_detail.append(u"しゅわりん")
        if u"ハピネス" in bus or u"ハピマジ" in bus: bus_detail.append(u"ハピネス")
        if "HHP" in bus: bus_detail.append("HHP")
        if "LOUDER" in bus: bus_detail.append("LOUDER")
        if u"まかせ" in bus or u"任せ" in bus: bus_detail.append(u"おまかせ")
        if u"自由" in bus: bus_detail.append(u"曲自由")

        score_match = re.search(u"[0-9\.]+万", bus)
        if score_match is not None:
            bus_detail.append(colored(score_match.group(0), "green"))

        if u"レギュラー" in bus:
            bus_type = colored("Regular", "blue")
        elif u"ベテラン" in bus:
            bus_type = colored("Veteran", "red")
        else:
            bus_type = "Unknown"

        bus_id = colored(match.group(0), "yellow")

        print("[%s] %s %s %s" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), bus_type, bus_id, " ".join(bus_detail)))


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = auth, listener=myStreamListener)
myStream.filter(track=[u"#バンドリ協力,#ガルパ協力"])