#!/usr/bin/env python
	
from lxml import html  
import json
import requests
import json,re
from dateutil import parser as dateparser
from time import sleep

def ParseReviews(asin):
	
	#amazon_url  = 'http://www.amazon.com/product-reviews/'+asin+'/pageNumber='+i+'/ref=cm_cr_othr_d_paging_btm_'+i+'?pageNumber='+i
	amazon_url = 'http://www.amazon.com/product-reviews/'+asin

	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	page = requests.get(amazon_url,headers = headers,verify=False)
	page_response = page.text

	parser = html.fromstring(page_response)

	XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
	XPATH_PRODUCT_NAME = '//span[@id="productTitle"]//text()'
    
	raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
	product_name = ''.join(raw_product_name).strip()
    
	total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
	ratings_dict = {}
	

	#grabing the rating  section in product page
    
	for ratings in total_ratings:
		extracted_rating = ratings.xpath('./td//a//text()')
		if extracted_rating:
			rating_key = extracted_rating[0] 
			raw_raing_value = extracted_rating[1]
			rating_value = raw_raing_value
			if rating_key:
				ratings_dict.update({rating_key:rating_value})
	
	#Parsing individual reviews
    
	data = {
				'ratings':ratings_dict,
				'name':product_name
			}
    
        if asin is 'B06Y16RL4W':
                data['name'] = "Samsung Galaxy S8+"
        if asin is 'B06Y14T5YW':
                data['name'] = "Samsung Galaxy S8"
        if asin is 'B075QNGHS8':
                data['name'] = "iPhone 8 Plus"
        if asin is 'B075QMZH2L':
                data['name'] = "iPhone X"
        if asin is 'B079JXY4TJ':
                data['name'] = "Samsung Galaxy S9+"
        if asin is 'B079JSZ1Z2':
                data['name'] = "Samsung Galaxy S9"
        if asin is 'B075QJSQLT':
                data['name'] = "iPhone 8"
        if asin is 'B07539DSV3':
                data['name'] = "Samsung Galaxy Note8"
        return data
def ReadAsin():
	
	#AsinList = ['B075QNGHS8', 'B06Y14T5YW', 'B06Y15KSBB', 'B07539DSV3', 'B079H6RLKQ' , 'B079JXY4TJ', 'B075QN8NDH', 'B075QJSQLT']
	#galaxy s8
	#AsinList = ['B06Y14T5YW', 'B06Y1652H5']
	#galaxy s8+
	#AsinList =['B06Y16RL4W']#, 'B06Y15KSBB']
	#iphone 8 
	#AsinList = ["B075QJSQLT"]
	#AsinList = ["B075QNGHS8"]
	#galaxy s9
	#AsinList = ["B079JSZ1Z2"]
	#galaxy s9+
	#AsinList = ["B079JXY4TJ"]
	#iphone x
	AsinList = ['B06Y16RL4W', 'B06Y14T5YW', 'B075QNGHS8', 'B075QMZH2L', 'B079JXY4TJ', 'B079JSZ1Z2', 'B075QJSQLT', 'B07539DSV3']
    #AsinList = []

	extracted_data = []
	for asin in AsinList:
		print("Downloading and processing page http://www.amazon.com/dp/"+asin)
		extracted_data.append(ParseReviews(asin))
		sleep(5)
	f = open('data.json','w')
	json.dump(extracted_data,f,indent=4)

if __name__ == '__main__':
	ReadAsin()