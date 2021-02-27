import numpy
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import make_scorer


X = [[1, 1], [1, 2], [3, 3], [4, 3], [3, 5]]
y = [0, 1, 1, 0, 0]


def classify(metrics, grades):
    X_train, X_test, y_train, y_test = train_test_split(metrics, grades, test_size=0.3)
    # X_train, X_test, y_train, y_test = train_test_split(metrics, grades, test_size=0.2, random_state=0)


    # X_train.shape, y_train.shape((90, 4), (90,))
    # X_test.shape, y_test.shape((60, 4), (60,))

    clf = SVC(kernel='linear').fit(X_train, y_train)
    # clf.score(X_test, y_test)
    y_predict = clf.predict(X_test)
    print(X_test)
    print(y_predict)
    print(classification_report(y_test, y_predict))


def crossValidation(metrics, grades, numberOfFolds):

    clf = svm.SVC(kernel='linear', C=1000)
    return cross_val_score(clf, metrics, grades, cv=numberOfFolds, scoring='f1_macro')


def predict(trainingMetrics, trainingGrades, testMetrics):

    clf = svm.SVC(kernel='linear').fit(trainingMetrics, trainingGrades)
    return clf.predict(testMetrics)
