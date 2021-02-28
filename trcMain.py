from readability import Readability
import nltk
# nltk.download('punkt')
import os
import svm_evaluation
import grammar

training_dirPath = 'training_data'
test_dirPath = 'test_data'
numberOfFoldsForCrossVal = 10

data_metrics = []
data_grades = []

# train/test with files in the directory
for file in os.listdir(training_dirPath):
    with open(training_dirPath + '/' + file, encoding='utf-8') as f:
        text = f.read()
        f.close()

    # get Meta-Data through file name: ID (arbitrary), Grade (as set by the textbook authors),
    # Format (read/listen), Type (plain/blog/song/dialog/...)
    textGrade, textID, textFormat, textType = file.split("_")
    textType = textType.split(".")[0]

    # filter text types that arent suitable for this analysis
    if textType == "song" or textType == "dialog" or textType == "cloze":
        continue

    r = Readability(text)

    # calculate readability scores and save as data
    data_metrics.append([r.flesch_kincaid().score, r.flesch().score, r.gunning_fog().score, r.coleman_liau().score,
                         r.dale_chall().score, r.ari().score, r.linsear_write().score, r.spache().score])

    data_grades.append(textGrade)

print(data_metrics)
print(data_grades)
print('size of data set: ' + str(len(data_metrics)))

# cross-validation
scores = svm_evaluation.crossValidation(data_metrics, data_grades, numberOfFoldsForCrossVal)
accuracy = sum(scores) / numberOfFoldsForCrossVal
print('f1-score = ' + str(accuracy))


# prediction of new data
for file in os.listdir(test_dirPath):
    with open(test_dirPath + '/' + file, encoding='utf-8') as f:
        text = f.read()
        f.close()

    r = Readability(text)

    test_metrics = [[r.flesch_kincaid().score, r.flesch().score, r.gunning_fog().score, r.coleman_liau().score,
                     r.dale_chall().score, r.ari().score, r.linsear_write().score, r.spache().score]]

    print(test_metrics)
    print(svm_evaluation.predict(data_metrics, data_grades, test_metrics))

    # grammar checking of new data
    grammar.checkGrammar_KLP7(text)
