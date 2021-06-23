import readability_comparison
import nltk
# nltk.download('punkt')
import os
import svm_evaluation
import grammar
import vocabulary

# CONFIG / USER INPUT
training_dirPath = 'training_data'
test_dirPath = 'test_data'
path_additional_vocabulary = 'vocabulary_data'
numberOfFoldsForCrossVal = 10
grade = 6



# TRAINING
print("Training the algorithm for grade " + str(grade) + "...")
# readability
data_metrics, data_grades = readability_comparison.training_readability(training_dirPath)
# vocabulary
training_vocabulary = {"."}  # defined as a set
training_vocabulary = vocabulary.add_training_vocabulary(training_dirPath, grade, training_vocabulary)
training_vocabulary = vocabulary.add_additional_vocabulary(path_additional_vocabulary, training_vocabulary)


# cross-validation //TODO uncomment
scores = svm_evaluation.crossValidation(data_metrics, data_grades, numberOfFoldsForCrossVal)
accuracy = sum(scores) / numberOfFoldsForCrossVal
print('f1-score = ' + str(accuracy))


# EVALUATION
print("Finished")

# prediction of texts in test data directory
for file in os.listdir(test_dirPath):
    with open(test_dirPath + '/' + file, encoding='utf-8') as f:
        text = f.read()
        f.close()

    print()
    print('Evaluation of file: ' + file)
    print('---------')

    # READABILITY: compare readability of test text to training data
    print('Readability:')
    print('size of used data set: ' + str(len(data_metrics)))
    readability_comparison.compare(text, grade)
    print('--------- \n')

    # GRAMMAR: grammar checking of new data
    print('Grammar: ')
    grammar.check_grammar(text, grade)
    print('\n---------')

    # VOCABULARY: check for unknown words
    print('Vocabulary: ')
    vocabulary.print_unknown_words(text, training_vocabulary)
    print('---------' + '\n' + '\n' + '\n' + '\n' + '\n')
