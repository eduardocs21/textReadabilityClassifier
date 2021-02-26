from readability import Readability
import nltk
# nltk.download('punkt')
import os
import svm_evaluation

dirPath = 'test_data'

dataMetrics = []
dataGrade = []

# train/test with files in the directory
for file in os.listdir(dirPath):
    with open(dirPath + '/' + file, encoding='utf-8') as f:
        text = f.read()
        f.close()

    r = Readability(text)

    # calculate readability scores and save as data
    dataMetrics.append([r.flesch_kincaid().score, r.flesch().score, r.gunning_fog().score, r.coleman_liau().score,
                        r.dale_chall().score, r.ari().score, r.linsear_write().score, r.spache().score])

    # get Meta-Data through file name: ID (arbitrary), Grade (as set by the textbook authors),
    # Format (read/listen), Type (plain/blog/song/dialog/...)
    textId, textGrade, textFormat, textType = file.split("_")
    dataGrade.append(textGrade)

print(dataMetrics)
print(dataGrade)

svm_evaluation.classify(dataMetrics, dataGrade)



