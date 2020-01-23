import shutil
import os
import re
import string
import sqlite3
import logging
from lxml import etree as ET
import xml.etree.ElementTree as ET
from pathlib import Path
mypath = Path().absolute()
os.chdir(mypath/'input')
source = os.listdir(mypath/'input')
destination = mypath/'incorrect_input'
for files in source:
    if not files.endswith(".fb2"):
        shutil.move(files, destination)
    elif files.endswith(".fb2"):
        tree = ET.parse(os.path.join(mypath/'input', files))
        root = tree.getroot()



book_name = []
number_of_paragraph = []
for files in source:
    if files.endswith(".fb2"):
        for event, elem1 in ET.iterparse(files):
            elem1.tag = elem1.tag.partition('}')[-1]
            if elem1.tag == "book-name":
                book_name.append( elem1.text)
print(book_name)

number_of_paragraph = []
num_p = []
a = []
for files in source:
    if files.endswith(".fb2"):
        for event, elem2 in ET.iterparse(files):
            if elem2.tag.partition('}')[-1] == "p":
                paragraphs = tree.findall('*/p')
                num_p.append(len(paragraphs))
                a.append(len(num_p))
number_of_paragraph.append(len(a))
# print(number_of_paragraph)


for files in source:
    if files.endswith(".fb2"):
        with open(files, 'r', encoding='utf8') as file:
            text = file.read()
book_text_pattern = r"<body>(.*?)<\/body>"
text_of_book = re.findall(book_text_pattern, text, flags=re.DOTALL)
clean_pattern = re.compile('[^а-яА-ЯёЁ]')
book_text = re.sub(clean_pattern, ' ', str(text_of_book))
extra_symbols = string.punctuation.join('«»…—№\\n’' + string.digits)
clean_text = ''.join(word for word in book_text if word not in extra_symbols)


number_of_words = []
text = re.findall(r'\w+', clean_text)
number_of_words.append(len(text))
print(text)
print (number_of_words)
#
number_of_letters =[]
letters = re.findall(r'\w', clean_text)
number_of_letters.append(len(letters))


word_Upper =0
word_lower = 0
for word in text:
    if word == word.lower():
        word_lower +=1
    else:
        word_Upper += 1


words = {}
for word in clean_text.split():
    if word.capitalize() not in words and word == word.lower():
        words[word.capitalize()] = [1,0]
    elif word.capitalize() not in words and word != word.lower():
        words[word.capitalize()] = [1, 1]
    elif word.capitalize() in words and word == word.lower():
        words[word.capitalize()][0] += 1
    else:
        words[word.capitalize()][0] += 1
        words[word.capitalize()][1] += 1


temp = []
dictlist = []
for key, (value1, value2) in words.items():
    temp = [key, value1, value2]
    dictlist.append(temp)




from sqlite3 import Error
def sql_connection():
    logging.basicConfig(filename="Makarava_log.log", level=logging.INFO)
    try:
        con = sqlite3.connect('Makarava_task.db')
        logging.info("Connection is established: Database is created")
        return con
    except Error:
        print(Error)

def sql_table(con):
     cursorObj = con.cursor()
     cursorObj.execute("CREATE TABLE book_stat(book_name text, number_of_paragraph number, number_of_words number,"
                       "number_of_letters number, words_with_capital_letters number, words_in_lowercase number)")
     cursorObj.execute("CREATE TABLE input_file_stat(word text, count number, count_uppercase number)")
     cursorObj.execute("INSERT INTO book_stat VALUES (?, ?, ?, ?, ?, ?)", (book_name[0], number_of_paragraph[0], number_of_words [0], number_of_letters [0], word_Upper, word_lower))
     cursorObj.executemany("INSERT INTO input_file_stat VALUES (?, ?, ?)", dictlist)
     con.commit()
con = sql_connection()
sql_table(con)


