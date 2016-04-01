import urllib
import re
import os 
import string
import regex
try:
	from bs4 import BeautifulSoup
except ImportError:
	from BeautifulSoup import BeautifulSoup
def write_text(col1,target):

	col1=re.sub("\d+", "#", col1)
	col1=col1.split('#')
	no_sentences=0
	for l in range(len(col1)):
				line=col1[l].strip()
				#print line.encode('utf-8')
				if line!="":
					target.write(line.encode('utf-8'))
					target.write("\n")
					no_sentences+=1
	return no_sentences

def scrap_doc(url_chapter,name,book_name):	
	
	html = urllib.urlopen(url_chapter)
	soup = BeautifulSoup(html)
	

	#to remove <a></a>
	for tag in soup.find_all('a'):
		tag.replaceWith('')
	
	
	tds = soup.find_all('td')
	col1=tds[0].text
	col2=tds[1].text
	folder=book_name[:-4]
	target_r = open("dataset/Mahabharata/"+folder+"/"+name+"_roman.txt", 'w')
	target_s = open("dataset/Mahabharata/"+folder+"/"+name+"_sans.txt", 'w')

	if (write_text(col1,target_s) != write_text(col2,target_r)):
		print name
	
def get_chapter_links(link):

	directory="dataset/Mahabharata/"+link[:-4]
	if not os.path.exists(directory):
			os.makedirs(directory)
	print directory		
	url="http://sacred-texts.com/hin/mbs/"+link
	book_name=link
	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)

	h_tag=soup.find('hr')
	for br in h_tag.find_next_siblings():
		link=br.get('href')
		if link!=None:
			scrap_doc("http://sacred-texts.com/hin/mbs/"+link,link,book_name)

def get_links_books():

	directory="dataset/Mahabharata/"
	if not os.path.exists(directory):
			os.makedirs(directory)
	url="http://sacred-texts.com/hin/mbs/index.htm"
	
	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)


	h_tag=soup.find('hr')
	for br in h_tag.find_next_siblings():
		link=br.get('href')
		if link!=None:
			get_chapter_links(link)

if __name__ == "__main__":
	get_links_books()