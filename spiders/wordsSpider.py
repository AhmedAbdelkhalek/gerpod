# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

def word_and_sound_extractor(tag, css_class):
    tag = tag.find(attrs={"class": css_class})
    try:
        txt = tag.find("span").text
        url = tag.find("audio")["src"]
    except AttributeError:
        return "", ""
    return txt, url


class WordsSpider(scrapy.Spider):
    name = 'wordsSpider'
    allowed_domains = ['www.germanpod101.com']
    start_urls = ['https://www.germanpod101.com/german-word-lists/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        item_boxes = soup.find_all(attrs={"class": "wlv-item__box"})
        words = {}
        for item_box in item_boxes:
            ger_word, ger_word_sound_url = word_and_sound_extractor(item_box, "wlv-item__word-container")
            eng_word, eng_word_sound_url = word_and_sound_extractor(item_box, "wlv-item__english-container")
            example_box = item_box.find(attrs={"class": "wlv-item__samples-box"})
            ger_example, ger_example_sound_url = word_and_sound_extractor(example_box, "wlv-item__word-container")
            eng_example, eng_example_sound_url = word_and_sound_extractor(example_box, "wlv-item__english-container")
            yield {
                "ger_word": ger_word,
                "ger_word_sound_url": ger_word_sound_url,
                "eng_word": eng_word,
                "eng_word_sound_url": eng_word_sound_url,
                "ger_example": ger_example,
                "ger_example_sound_url": ger_example_sound_url,
                "eng_example": eng_example,
                "eng_example_sound_url": eng_example_sound_url
            }

