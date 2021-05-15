"""
Web Scraping with Beautiful Soup

Objective:
In order to study the highly recommended book titles and contents for future use,  
this script is to extract the Top 50 recommended books and their summaries from a reputable book summary blog, in this case the blog is "James Clear .com"
url: https://jamesclear.com/book-summaries?utm_source=designepiclife](https://jamesclear.com/book-summaries?utm_source=designepiclife

"""

# Import modules
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

# Using James Clear Book Summary website
path = "https://jamesclear.com/book-summaries?utm_source=designepiclife"

# Create Beautiful Soup Object with URL path
source = requests.get(path).text
soup = bs(source, 'html.parser')

""" 
# Alternatives: Using HTML file to import 
with open('bookSummary.html') as html_file:
 	soup = BeautifulSoup(html_file, 'lxml')
"""

# Inspect on the html
# print(soup.prettify())

# Get the book titles and authors
titles = []
authors = []
for count, book in enumerate(soup.find_all('div', class_='sale-book')):
	if re.search("Bird", book.h3.text):
		title = "by ".join(book.h3.text.split("by ", 2)[:2]) #[0].strip()
		author = book.h3.text.split("by ", 2)[2].strip()

	else:
	 	title = book.h3.text.split("by ")[0].strip()
	 	author = book.h3.text.split("by ")[1].strip()
	titles.append(title)
	authors.append(author)


print(f"Number of books: {len(titles)} and Number of authors: {len(authors)}")
print()


# Scraping the 3 sentences summaries of each book
summaryTexts = []
for counter, summary in enumerate(soup.find_all('p')):
	# On James Clear's website, the summary text appear in the 4th appearance of paragraph
	if counter >= 3:
		if re.search(r":", summary.text):
			summaryText = summary.text.split(":")[1].strip() 
			summaryTexts.append(summaryText)
		
print(f"Number of Summaries: {len(summaryTexts)}")
print()

# Get the URLs of the detailed book summaries 
counter = 0
urls = []
for url in soup.find_all("a", href=True):
	if re.search("book-summaries", url['href']) and re.search("https:", url['href']):
		counter += 1
		urls.append(url['href'])
print(f"Number of URLs: {counter}")


# Create Data Frame 
books = {"Title": titles, "Authors": authors, "URL": urls}
df = pd.DataFrame(books)

# Export to excel 
import os
export_directory = # Create your directory path where you want to save your final excel. e.g. "/User/Desktop"
filename = # Create your excel name. e.g. "books_summaries"
file_suffix = ".xslx"
df.to_excel(os.path.join(export_directory, filename + file_suffix), index=False)

