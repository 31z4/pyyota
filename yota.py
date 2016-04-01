import cookielib
import httplib
import json
import re
import urllib
import urllib2


class Yota(object):
    __LOGIN_URL = 'https://login.yota.ru/UI/Login'
    __CHANGE_OFFER_URL = 'https://my.yota.ru/selfcare/devices/changeOffer'
    __DEVICES_URL = 'https://my.yota.ru/selfcare/devices'

    def __init__(self, username, password):
        self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.__product, self.__tariff, self.__offers = self.__parse_slider_data(self.__login(username, password))

    @staticmethod
    def __parse_slider_data(html):
        slider_data = json.loads(re.search(' var sliderData = (.*?);', html).group(1))
        product = slider_data.keys()[0]
        product_data = slider_data[product]
        current_offer = product_data['offerCode']
        offers = {
            step['code']: step['name']
            for step in product_data['steps']
        }

        return product, current_offer, offers

    def __request(self, url, **kwargs):
        response = self.__opener.open(urllib2.Request(url, urllib.urlencode(kwargs)))
        assert (response.getcode(), response.geturl()) == (httplib.OK, self.__DEVICES_URL)
        return response.read()

    def __login(self, username, password):
        return self.__request(self.__LOGIN_URL, IDToken1=username, IDToken2=password)

    def __change_offer(self, code):
        assert code in self.__offers
        return self.__request(self.__CHANGE_OFFER_URL, product=self.__product, offerCode=code)

    @property
    def offers(self):
        return self.__offers

    @property
    def tariff(self):
        return self.__tariff

    @tariff.setter
    def tariff(self, code):
        self.__product, self.__tariff, self.__offers = self.__parse_slider_data(self.__change_offer(code))
        assert self.__tariff == code
