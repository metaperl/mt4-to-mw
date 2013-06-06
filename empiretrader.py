#!/usr/bin/python

# system
import pprint
import time

# pypi
import argh
from splinter import Browser

# local
import user


pp = pprint.PrettyPrinter(indent=4)

base_url = 'http://www.empireoption.com'

action_path = dict(
    login = "",
    bonuses = 'bonuses'
)

def url_for_action(action):
    return "{0}/{1}".format(base_url,action_path[action])


class Entry(object):

    def __init__(self, user, browser, direction):
        self.user=user
        self.browser=browser
        self.direction=direction

    def login(self):
        print("Logging in...")
        self.browser.visit(url_for_action('login'))
        self.browser.find_by_id('loginInputlogin').first.value = self.user['username']
        self.browser.find_by_id('loginInputPassword').first.value = self.user['password']
        lookup = '//input[@value="Login"]'
        button = self.browser.find_by_xpath(lookup).first
        button.click()

    def click_60s(self):
        lookup = '//li[@class="sixtySeconds"]'
        clickable = self.browser.find_by_xpath(lookup).first
        clickable.click()

    def click_xpath(self, lookup):
        clickable = self.browser.find_by_xpath(lookup).first
        clickable.click()

    def select_asset(self):
        self.click_xpath('//input[@id="assetChoose_input"]')
        time.sleep(2)
        self.click_xpath('//li[@id="assetChoose_input_2"]')

    def choose_direction(self):
        lookup = '//input[@title="{0}"]'.format(self.direction)
        self.click_xpath(lookup)

    def click_start(self):
        self.click_xpath('//div[@class="startButtonText"]')

    def trade(self):
        self.click_60s()
        self.select_asset()
        self.choose_direction()
        self.click_start()


def main(direction):

    with Browser() as browser:

        _u = user.User().live

        e = Entry(_u, browser, direction)
        e.login()
        e.trade()

        while True: pass

if __name__ == '__main__':
    argh.dispatch_command(main)
