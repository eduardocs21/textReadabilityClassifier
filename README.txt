For the Grammar-Module to work, a Stanford Core NLP Server (Java) has to be started manually.
(Reason: Usage of POS-Tagger and Dependency Parser)


Tutorial for Windows PowerShell:
1. Open the directory of the classifier in Windows explorer (place of this README-file)
2. Shift + Right-Click on "stanford-corenlp-4.2.0"
3. Click "Open PowerShell Window here"
4. Copy and paste the following command
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000
5. Press Enter


Tutorial with alternative way to open PowerShell:
1. Open the directory of the classifier in Windows explorer (place of this README-file)
2. Double-Click on the directory "stanford-corenlp-4.2.0"
3. Type "powershell" in the address bar and press Enter
4. Copy and paste the following command
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000
5. Press Enter