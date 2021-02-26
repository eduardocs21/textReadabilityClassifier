from readability import Readability
import nltk
# nltk.download('punkt')


with open('test.txt') as f:
    test_data = f.read()
    f.close()

r = Readability(test_data)
print(r.flesch_kincaid())
print(r.flesch())
print(r.gunning_fog())
print(r.coleman_liau())
print(r.dale_chall())
print(r.ari())
print(r.linsear_write())
print(r.spache())