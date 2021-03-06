﻿# -*- coding: utf-8 -*-
import re,urllib
from tmitter.settings import *
from django.shortcuts import render_to_response
from django.template import context
from django.core.paginator import Paginator, InvalidPage

def tiny_url(url):
    u"""
    summary:
        將url轉換成tinyurl
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl

def content_tiny_url(content):
    u"""
    summary:
        讓訊息裡面的連線轉換成更短的Tinyurl
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    
    regex_url = r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tiny_url(url))
    
    return content

def substr(content, length,add_dot=True):
    u"""
    summary:
        字串截取
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    if(len(content) > length):
        content = content[:length]
        if(add_dot):
            content = content[:len(content)-3] + '...'
    return content

def pagebar(objects,page_index,username='',tempate='control/home_pagebar.html'):
    u"""
    summary:
        產生HTML分頁控制項,要使用tempate
    params:
        objects     資料清單
        page_index  目前頁數
        username    目前被存取的空間的使用者名稱，沒有傳空
        template    分頁範本
    author:
        Jason Lee <huacnlee@gmail.com>
    """
    page_index = int(page_index)
    _paginator = Paginator(objects, PAGE_SIZE)
    
    if(username):
        tempate = 'control/user_pagebar.html'
    
    return render_to_response(tempate, { 
        'paginator': _paginator,
        'username' : username,
        'has_pages': _paginator.num_pages > 1,
        'has_next': _paginator.page(page_index).has_next(),
        'has_prev': _paginator.page(page_index).has_previous(),
        'page_index': page_index,
        'page_next': page_index + 1,
        'page_prev': page_index - 1,
        'page_count': _paginator.num_pages,
        'row_count' : _paginator.count,
        'page_nums': range(_paginator.num_pages+1)[1:],
    }).content

    
    