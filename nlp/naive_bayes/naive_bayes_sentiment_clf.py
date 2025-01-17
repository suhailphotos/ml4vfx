import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv('/home/fpserver/development/DATASETS/nlp/combined_emotion.csv')

df['sentence'] = df['sentence'].str.lower()

X_train, X_test, y_train, y_test = train_test_split(df['sentence'],df['emotion'], test_size=0.2, random_state=42)

vectorizer = CountVectorizer(stop_words="english")
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_vectorized, y_train)

y_pred = nb_classifier.predict(X_test_vectorized)
print("Accuracy: ", accuracy_score(y_test,y_pred))
print("Classification report: ", classification_report(y_test,y_pred))

new_sentences = ["I'm so happy today!", "This is terrifying."]
new_sentences_vectorized = vectorizer.transform(new_sentences)
predictions = nb_classifier.predict(new_sentences_vectorized)
print(new_sentences)
print("Predictions: ", predictions)
