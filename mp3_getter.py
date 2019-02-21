import urllib
import time
import shutil
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# from http://accent.gmu.edu/browse_language.php, return list of languages
def get_languages():
    """ This will return all the languages present in website
        http://accent.gmu.edu"""

    url = "http://accent.gmu.edu/browse_language.php"
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    languages = []
    language_lists = soup.findAll('ul', attrs={'class': 'languagelist'})
    for ul in language_lists:
        for li in ul.findAll('li'):
            languages.append(li.text)
    return languages


# from list of languages, return urls of each language landing page
def lang_pages(lst):
    """ This will return all the landing pages for the list of languages obtained
        from the above function"""

    urls=[]
    for lang in lst:
        urls.append('http://accent.gmu.edu/browse_language.php?function=find&language={}'.format(lang))
    return urls

# from language, get the number of speakers of that language
def get_num(language):
    url = 'http://accent.gmu.edu/browse_language.php?function=find&language=' + language
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    test = soup.find_all('div', attrs={'class': 'content'})
    try:
        num = int(test[0].find('h5').text.split()[2])
    except AttributeError:
        num = 0
    return num
    
# from list of languages, return list of tuples (LANGUAGE, LANGUAGE_NUM_SPEAKERS) for mp3getter, ignoring languages
# with 0 speakers
def get_formatted_languages(languages):
    formatted_languages = []
    for language in languages:
        num = get_num(language)
        if num != 0:
            formatted_languages.append((language,num))
    return pd.DataFrame(formatted_languages, columns=["Language", "No. Of Speakers"]).sort_values(by="No. Of Speakers", ascending=False).reset_index(drop=True)

#For getting the speaker ids
def get_speaker_id(lang):
    speaker_id = []
    url = "http://accent.gmu.edu/browse_language.php?function=find&language=" + lang
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    for link in soup.find_all('a', href=re.compile("^browse_language")):
        href = link['href']
        url = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(url.query)
        if 'speakerid' in params:
            speaker_id.append((params['speakerid'][0], "http://chnm.gmu.edu/accent/soundtracks/" + link.contents[0].replace(",", "") + ".mp3"))
    return pd.DataFrame(speaker_id, columns=["Speaker ID", "MP3 URL"]).reset_index(drop=True)

def get_mp3(url):
    urllib.request.urlretrieve(url, "./file_name.mp3")

def convert_to_wav(path):
    sound = AudioSegment.from_mp3("C:\Users\arindmishra001\Desktop\GL_Capstone\my_codes")
    sound.export("/output/path/file.wav", format="wav")