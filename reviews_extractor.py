from lxml import html  
import json
import requests
import json,re
from dateutil import parser as dateparser
from time import sleep

def ParseReviews(asin,i):
	# for i in range(5):
	# 	try:
	
	#list1=['1']#,'2','3','4','5','6']

	
	amazon_url  = 'http://www.amazon.com/product-reviews/'+asin+'/pageNumber='+i+'/ref=cm_cr_othr_d_paging_btm_'+i+'?pageNumber='+i
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	page = requests.get(amazon_url,headers = headers,verify=False)
	page_response = page.text

	parser = html.fromstring(page_response)
	
	XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'

	XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
	XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

	XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
	XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
	XPATH_PRODUCT_PRICE  = '//span[@id="priceblock_ourprice"]/text()'
	
	raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
	product_price = ''.join(raw_product_price).replace(',','')

	raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
	product_name = ''.join(raw_product_name).strip()
	total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
	reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
	if not reviews:
		reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
	ratings_dict = {}
	reviews_list = []
	
	if not reviews:
		raise ValueError('unable to find reviews in page')

	for ratings in total_ratings:
		extracted_rating = ratings.xpath('./td//a//text()')
		if extracted_rating:
			rating_key = extracted_rating[0] 
			raw_raing_value = extracted_rating[1]
			rating_value = raw_raing_value
			if rating_key:
				ratings_dict.update({rating_key:rating_value})
	
	#Parsing individual reviews
	for review in reviews:
		XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
		XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
		XPATH_REVIEW_TEXT_1 = './/span[@data-hook="review-body"]//text()'
		
		raw_review_rating = review.xpath(XPATH_RATING)
		raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
		raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
		
		#cleaning data
		
		review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
		review_header = ' '.join(' '.join(raw_review_header).split())
		
		review_text = ' '.join(' '.join(raw_review_text1).split())
		
		full_review_text = review_text

		review_dict = {
							'review_text':full_review_text,
							'review_header':review_header,
							'review_rating':review_rating,

						}
		reviews_list.append(review_dict)

	data = {
				'ratings':ratings_dict,
				'reviews':reviews_list,
				'url':amazon_url,
				'price':product_price,
				'name':product_name
			}
	
	return data
			
def ReadAsin():
	
	#AsinList = ['B075QNGHS8', 'B06Y14T5YW', 'B06Y15KSBB', 'B07539DSV3', 'B079H6RLKQ' , 'B079JXY4TJ', 'B075QN8NDH', 'B075QJSQLT']
	#galaxy s8
	#AsinList = ['B06Y1652H5']#'B06Y14T5YW']
	#galaxy s8+
	#AsinList =['B06Y16RL4W', 'B06Y15KSBB']
	#iphone 8 
	#AsinList = ["B075QJSQLT"]
	#iphone 8 plus
	#AsinList = ["B075QNGHS8"]
	#galaxy s9
	#AsinList = ["B079JSZ1Z2"]
	#galaxy s9+
	#AsinList = ["B079JXY4TJ"]
	#iphone x 11
	#AsinList = ["B075QNGDZL"]
	#iphoen x 10
	#AsinList = ["B075QN8NDH"]
	#note8 12
	#AsinList = ["B075KQ622T"]
	#note8 29
	AsinList = ["B07539DSV3"]

	extracted_data = []
	for asin in AsinList:
		print "Scraping "
		list1=['1','2','3','4','5','6','7','8','9','10','11', '12', '13', '14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']#,'29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48']#,'49','50','51','52','53','54','55','56','57','58','59','60']
		for i in list1:
			extracted_data.append(ParseReviews(asin,i))
		sleep(5)
		f = open(asin+'.json','w')
		json.dump(extracted_data,f,indent=4)

if __name__ == '__main__':
	ReadAsin()