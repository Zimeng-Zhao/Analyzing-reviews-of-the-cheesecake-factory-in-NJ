import json
import re
from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelBinarizer
lb = LabelBinarizer()
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPooling1D, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


with open("data/labeled_sentense.json", "rb") as file:
    datalist = json.load(file)

with open("data/labeled_sentense2.json", "rb") as file:
    datalist+=json.load(file)

with open("data/labeled_sentense3.json","rb") as file:
    datalist+=json.load(file)

with open("data/labeled_sentense4.json","rb") as file:
    datalist+=json.load(file)

X=[]
y=[]
for data in datalist:
    sentense=data[0]
    label=re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', data[1]).lower()
    if label=="none" or label=="food" or label=="service" or label=="atmosphere" or label=="hygiene":
        X.append(sentense)
        y.append(label)
    elif label=="location" or label=="parking" or label=="transportation":
        X.append(sentense)
        y.append("location")
print(len(X))
print(len(y))
print(set(y))

mydict={}

for d in y:
    mydict.setdefault(d,0)
    mydict[d]=mydict[d]+1
print(mydict)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


def CNN_classificate(train_text, test_text, train_label, test_label):
    tfidf=TfidfVectorizer(stop_words="english", min_df=0.005,ngram_range=(1,1),lowercase=True)
    train_dtm=tfidf.fit_transform(train_text).toarray()
    dump(tfidf, 'data/tfidf_vectorizer.joblib')
    tfidf = load('data/tfidf_vectorizer.joblib')
    test_dtm=tfidf.transform(test_text).toarray()
    lb = LabelBinarizer()
    #sampling_strategy = {'food': 10000, 'atmosphere': 6000, 'location': 4000, 'service': 8000, 'none': 8000, 'hygiene': 8000}
    #sm = SMOTE(random_state=42,sampling_strategy=sampling_strategy)
    #train_dtm,train_label = sm.fit_resample(train_dtm, train_label)
    train_y=lb.fit_transform(train_label)
    dump(lb, 'data/my_lb.joblib')
    lb=load('data/my_lb.joblib')
    test_y=lb.transform(test_label)


    model = Sequential()

    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(train_dtm.shape[1],1)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())

    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(6, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    scaler = MinMaxScaler()
    X_train_scaled=scaler.fit_transform(train_dtm)

    dump(scaler,"data/my_scaler.joblib")
    scaler=load("data/my_scaler.joblib")
    X_test_scaled=scaler.fit_transform(test_dtm)

    model.fit(X_train_scaled, train_y, epochs=100, batch_size=64)

    y_pred=model.predict(X_test_scaled)

    y_pred_argmax = np.argmax(y_pred, axis=1)
    if y_pred[y_pred_argmax]>0.5
    y_pred_binary = np.zeros_like(y_pred)
    for i, class_index in enumerate(y_pred_argmax):
        y_pred_binary[i, class_index] = 1



    print(y_pred_binary.shape)
    report=classification_report(test_y,y_pred_binary)
    print(report)
    print("Accuracy:", accuracy_score(test_y, y_pred_binary))
    model.save("data/my_CNN_TOPIC.h5")

CNN_classificate(X_train, X_test, y_train, y_test)