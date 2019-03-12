from pydub import AudioSegment
import pandas as pd
import os
import errno
import mp3_getter
import wav_processing
import re

if __name__ == '__main__':
    main()


def main():
    # Download mp3 file of selected languages
    try:
        os.mkdir('mp3')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
     
    langs = mp3_getter.get_languages()
    # get the top 5 language with most speakers
    top5_lang = mp3_getter.get_formatted_languages(langs)[:4]
    for lang in top5_lang['Language']:
        speaker_urls = mp3_getter.get_speaker_id(lang)
        mp3_getter.get_mp3('mp3', speaker_urls)

    # Convert mp3 file to 'wav' format
    try:
        os.mkdir('wav')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    for filename in os.listdir('mp3'):
        AudioSegment.from_mp3('./mp3/'+filename).export('./wav/' + filename.split('.')[0] + '.wav', format="wav")

    lst = []
    for filename in os.listdir('wav'):
        get_id = re.findall(r'\d+', filename)[0]
        mfcc = wav_processing.make_mfcc(filename)
        speaker_info = mp3_getter.get_speaker_info(get_id)
        lst.append(speaker_info + mfcc)

    mfcc_df = pd.DataFrame(lst)
    mfcc_df.to_csv('df_mfcc.csv')







