from readability import Readability
import nltk
# nltk.download('punkt')
import os

dirPath = 'test_data'

for file in os.listdir(dirPath):

    with open(dirPath + '/' + file, encoding='utf-8') as f:
        print(file)
        file_data = f.read()
        f.close()

    r = Readability(file_data)
    print(r.flesch_kincaid())
    print(r.flesch())
    print(r.gunning_fog())
    print(r.coleman_liau())
    print(r.dale_chall())
    print(r.ari())
    print(r.linsear_write())
    print(r.spache())


