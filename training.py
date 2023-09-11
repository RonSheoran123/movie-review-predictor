from nltk import NaiveBayesClassifier

classifier=NaiveBayesClassifier.train(training_data)
nltk.classify.accuracy(classifier,testing_data)
classifier.show_most_informative_features(15)
