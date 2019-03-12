import urllib
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from pydub import AudioSegment

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
def lang_page_urls(lst):
    """ This will return all the landing pages for the list of languages obtained
        from the above function"""

    urls=[]
    for lang in lst:
        urls.append('http://accent.gmu.edu/browse_language.php?function=find&language={}'.format(lang))
    return urls

# from language, get the number of speakers of that language
def get_num(language):
    url = 'http://accent.gmu.edu/browse_language.php?function=find&language={}'.format(language)
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
            speaker_id.append((lang, params['speakerid'][0], "http://chnm.gmu.edu/accent/soundtracks/" + link.contents[0].replace(",", "") + ".mp3"))
    return pd.DataFrame(speaker_id, columns=["language", "id", "url"]).reset_index(drop=True)

def download_mp3(folder, x):
  try:
    urllib.request.urlretrieve(x[2], "./{}/{}_{}.mp3".format(folder, x[0], x[1]))
  except urllib.error.HTTPError as err:
    print('URL:{} is giving an {} code'.format(x[2], err.code))
    pass

    
def get_mp3(folder, df):
    df.apply(lambda x: download_mp3(folder, x), axis=1)

def get_speaker_info(num):
    '''
    Inputs: two integers, corresponding to min and max speaker id number per language
    Outputs: Pandas Dataframe containing speaker filename, birthplace, native_language, age, sex, age_onset of English
    '''
    info = {'speakerid': num, 'filename': 0, 'birthplace':1, 'native_language': 2, 'age':3, 'sex':4, 'age_onset':5}
    url = "http://accent.gmu.edu/browse_language.php?function=detail&speakerid={}".format(num)
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    body = soup.find_all('div', attrs={'class': 'content'})
    try:
        info['filename']=str(body[0].find('h5').text.split()[0])
        bio_bar = soup.find_all('ul', attrs={'class':'bio'})
        info['birthplace'] = str(bio_bar[0].find_all('li')[0].text)[13:-6]
        info['native_language'] = str(bio_bar[0].find_all('li')[1].text.split()[2])
        info['age'] = float(bio_bar[0].find_all('li')[3].text.split()[2].strip(','))
        info['sex'] = str(bio_bar[0].find_all('li')[3].text.split()[3].strip())
        info['age_onset'] = float(bio_bar[0].find_all('li')[4].text.split()[4].strip())
    except:
        info['filename'] = ''
        info['birthplace'] = ''
        info['native_language'] = ''
        info['age'] = ''
        info['sex'] = ''
        info['age_onset'] = ''
#         df.to_csv('speaker_info_{}.csv'.format(stop))
    return list(info.values())