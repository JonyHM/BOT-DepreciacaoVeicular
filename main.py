#!/usr/bin/env python3.7
# encoding: utf-8

from BotTelegram import App

class Main(object):       
    def __init__(self):
        self.bot = App()

    def start(self):                
        self.bot.main()
        
if __name__ == "__main__":
    main = Main()
    main.start()