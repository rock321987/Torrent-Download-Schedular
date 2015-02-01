'''
Author - rock321987
Created On - 2 / 1 / 2015
Download videos from torrent at given schedule..
Works on Windows with 'Schedule Task'(found in control panel)
Python Version - 3.4 with BeautifulSoup
'''

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import os
import random
import sys
import codecs

basic = 'http://torrentz.eu'

def find_link(query):

	available_torrent_client = []
	
	for link in query.find_all('a'):
		x = str(link.get('href'))
		if (re.match('(.*?)(bitsnoop)(.*?)', x)):
			available_torrent_client.append('bitsnoop')
			break
		elif (re.match('(.*?)(extratorrent)(.*?)', x)):
			available_torrent_client.append('extratorrent')
		elif (re.match('(.*?)(thepiratebay)(.*?)', x)):
			available_torrent_client.append('thepiratebay')
		elif (re.match('(.*?)(katproxy)(.*?)', x)):
			available_torrent_client.append('katproxy')
		#elif (re.match('(.*?)kickass(.*?)', x)):
			#available_torrent_client.append('kickass')

	if (len(available_torrent_client) == 0):
		return 'not_possible'

	for link in query.find_all('a'):
		for client in available_torrent_client:
			tmp = '(.*?)' + client + '(.*?)'
			ln = link.get('href')
			if (re.match(tmp, ln)):
				return (str(ln))

def find_link_new(query):
	tmp = '(magnet)(.*?)'
	for link in query.find_all('a'):
		ln = link.get('href')
		if (ln is not None and re.match(tmp, ln)):
			return (str(ln))

def calc_hash_return_link(torrent_page):
	hash_size = {}
	i = 0
	
	for link in torrent_page.find_all('span'):
		if (link.get('class') == ['s']):
			size = link.get_text()
			size = (re.findall(r'\d{1,4}', size))
			i += 1
			if (int(size[0]) > 700 and int(size[0]) < 1500):
				hash_size[i] = size[0]
	
	rand_key = random.choice(list(hash_size.keys()))
	i = 0

	for link in torrent_page.find_all('a'):
		if (rand_key + 18 == i):
			return (link.get('href'))
		i += 1

if sys.stdout.encoding != 'cp850':
  sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
if sys.stderr.encoding != 'cp850':
  sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

def construct_url(query):
	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	req = urllib.request.Request(query, headers = headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	return respData

try:
	file_location = open('C:\\Users\\python\\Desktop\\url\\episode.txt', 'r+')
	episode_read = file_location.read()
	episode_find = (int(episode_read[4::])) + 1
	file_location.seek(0)
	file_location.truncate()
	episode_read = 's03e'
	
	if episode_find < 10:
		episode_read = 's03e0'	
	
	episode_read += str(episode_find)
	file_location.write(episode_read)
	file_location.close()

	query = '/searchS?q=arrow+' + episode_read
	query = basic + query
	torrent_page = BeautifulSoup(construct_url(query))

	'''query = calc_hash_return_link(torrent_page)
	query = basic + query
	
	torrent_link = BeautifulSoup(construct_url(query))
	torrent_client = find_link(torrent_link)
	
	if (torrent_client != 'not_possible'):
		magnet_link = BeautifulSoup(construct_url(torrent_client))
		magnet_link = find_link_new(magnet_link)
		#os.startfile(magnet_link)'''

	while (1):
		query = calc_hash_return_link(torrent_page)
		query = basic + query
	
		torrent_link = BeautifulSoup(construct_url(query))
		torrent_client = find_link(torrent_link)
		
		if (torrent_client != 'not_possible'):
			magnet_link = BeautifulSoup(construct_url(torrent_client))
			magnet_link = find_link_new(magnet_link)
			os.startfile(magnet_link)
			break
	
except Exception as e:
	print (str(e))
