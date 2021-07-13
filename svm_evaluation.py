import numpy
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, ShuffleSplit
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import make_scorer


def cross_validation(metrics, grades, n_splits):
    # evaluate the performance of the readability prediction model

    # validate with support vector machine
    clf = svm.SVC(kernel='linear', C=1)

    # shuffle split in case the samples are ordered
    cv = ShuffleSplit(n_splits=n_splits, test_size=0.3, random_state=5)

    # return the f1-score produced by cross-validation
    return cross_val_score(clf, metrics, grades, cv=cv, scoring='f1_micro')


def predict(trainingMetrics, trainingGrades, testMetrics):
    # predict the grade of the text by using the trained SVM

    clf = svm.SVC(kernel='linear').fit(trainingMetrics, trainingGrades)
    return clf.predict(testMetrics)


def calculate_baseline(data_grades):
    # calculate baseline to compare to cross-Validation f-Score by always picking majority class

    # count data sets and store in list and sort it ascending
    sample_size_list = [data_grades.count('5'), data_grades.count('6'), data_grades.count('7'), data_grades.count('9')]

    # calculate accuracy by dividing highest number by other numbers combined
    print("sample size = " + str(sample_size_list))
    sorted_list = sorted(sample_size_list)
    baseline = sorted_list[-1] / sum(sorted_list)

    return baseline

