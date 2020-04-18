
#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)

from modules.executor.Wordpress import Wordpress
from modules.executor.Magento import Magento
from modules.executor.Prestashop import Prestashop
from modules.executor.Lokomedia import Lokomedia
from modules.executor.Lokomedia2 import Lokomedia2
from modules.executor.Drupal import Drupal
from modules.executor.Joomla import Joomla
from modules.executor.Uknown import Uknown
from modules.executor.Opencart import Opencart

import re,requests


class CMS(object):

    def __init__(
        self,url,
        headers=None,
        exploit=False,
        domain=False,
        webinfo=False,
        serveros=False,
        cmsinfo=False,
        dnsdump=False,
        port=False
        ):

        self.url = url
        self.headers = headers
        self.exploit = exploit
        self.domain = domain
        self.webinfo = webinfo
        self.serveros = serveros
        self.cmsinfo = cmsinfo
        self.dnsdump = dnsdump
        self.port = port

    
    def __getlmcontent__(self):
        lm_content = self.url + '/smiley/1.gif'
        return requests.get(lm_content, self.headers).text

    def __getlm2content__(self):
        lm2_content = self.url + '/rss.xml'
        return requests.get(lm2_content, self.headers).text
    
    def __getcontent__(self):
        return requests.get(self.url, self.headers).text

    def __getexploit__(self):
        if self.exploit:
            return True

    def __getdomain__(self):
        if self.domain:
            return True

    def __getwebinfo__(self):
        if self.webinfo:
            return True

    def __getserveros__(self):
        if self.serveros:
            return True

    def __getcmsinfo__(self):
        if self.cmsinfo:
            return True

    def __getdnsdump__(self):
        if self.dnsdump:
            return True

    def __getport__(self):
        if self.port:
            return self.port

    def detect(self):
        """
        this module to detect cms & return type of cms.
        & make instance of cms.
        """
        if re.search(re.compile(r'<script type=\"text/javascript\" src=\"/media/system/js/mootools.js\"></script>|/media/system/js/|com_content|Joomla!'), self.__getcontent__()):
            name = 'Joomla'
            return name
        
        elif re.search(re.compile(r'wp-content|wordpress|xmlrpc.php'), self.__getcontent__()):
            name = 'Wordpress'
            return name
        elif re.search(re.compile(r'Drupal|drupal|sites/all|drupal.org'), self.__getcontent__()):
            name = 'Drupal'
            return name

        elif re.search(re.compile(r'Prestashop|prestashop'), self.__getcontent__()):
            name = 'Prestashop'
            return name
        elif re.search(re.compile(r'route=product|OpenCart|route=common|catalog/view/theme'), self.__getcontent__()):
            name = 'Opencart'
            return name

        elif re.search(re.compile(r'Log into Magento Admin Page|name=\"dummy\" id=\"dummy\"|Magento'), self.__getcontent__()):
            name = 'Magento'
            return name
        elif re.search(re.compile(r'image/gif'), self.__getlmcontent__()):
            name = 'Lokomedia1'
            return name

        elif re.search(re.compile(r'lokomedia'), self.__getlm2content__()):
            name = 'Lokomedia2'
            return name
        else:
            name = 'Uknown'
            return name

    def serialize(self):
        result = dict(
            name=self.detect(),
            exploit=self.__getexploit__(),
            domain=self.__getdomain__(),
            webinfo=self.__getwebinfo__(),
            serveros=self.__getserveros__(),
            cmsinfo=self.__getcmsinfo__(),
            dnsdump=self.__getdnsdump__(),
            port=self.__getport__()
        )
        return result

    def instanciate(self):
        cms = self.serialize()
        if cms['name']:
            instance = eval(cms['name'])(self.url,self.headers)
            print(' CMS : {}'.format(cms['name']))
            if cms['exploit']:
                instance.exploit()
            if cms['webinfo']:
                instance.webinfo()
            if cms['serveros']:
                instance.serveros()
            if cms['cmsinfo']:
                instance.cmsinfo()
            if cms['dnsdump']:
                instance.dnsdump()
            if cms['domain']:
                instance.domaininfo()
            if cms['port']:
                instance.ports(cms['port'])