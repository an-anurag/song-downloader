user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
    ]


# -*- coding: utf-8 -*-
"""
Global variables for project level configuration
Created on 10/9/2019
@author: Anurag
"""

# imports
import os

from configparser import RawConfigParser


class ConfigReader:
    """
    A class to implement custom cfg file reader
    """

    def __init__(self):
        self.cfg_file = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/setup.cfg')
        self._config = RawConfigParser()
        self._config.read(self.cfg_file)

    def read(self, section, key):
        """
        A read method to read key and values
        :return:
        """
        return self._config.get(section, key)


conf = ConfigReader()