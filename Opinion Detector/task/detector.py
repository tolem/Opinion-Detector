# write yor code here
import pandas as pd
from nltk import regexp_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import RandomOverSampler
from sklearn.svm import SVC

# nltk.download('stopwords')

english_stopwords = set(stopwords.words('english'))
opinion = {"Review": [], "Score": []}
file_name = input()
line_number = 0
lemmatizer = WordNetLemmatizer()
df = pd.DataFrame(data=opinion)
# # df.info()

with open('%s' % file_name, 'r', encoding="UTF-8") as file:
    while line_number < 150000:
        line = file.readline().strip()
        line_number = line_number + 1
        if len(line) > 0:
            score = line[-2:] if line[-2].isdigit() else line[-1:]
            last = -2 if line[-2].isdigit() else -1
            review = line[:last]
            opinion['Review'].append(review)
            opinion['Score'].append(int(score.rstrip()))

    else:
        def filter_word(text):
            ftext = regexp_tokenize(text, r'[A-z]+')
            ftext = " ".join(ftext).lower()
            ftext = lemmatizer.lemmatize(ftext, pos='n')
            filterd_review = [lemmatizer.lemmatize(word, pos='n') for word in ftext.split() if word not in english_stopwords]
            return filterd_review

        df = pd.DataFrame(data=opinion)
        df['Lemmas'] = df['Review'].apply(lambda x: filter_word(x))
        # print(df['Lemmas'].head(), df['Lemmas'].tail(), sep='\n')


        def sentiment_tag(mark):
            if 7 <= mark <= 10:
                return "Positive"

            if 1 <= mark <= 4:
                return "Negative"


        vectorizer = TfidfVectorizer()
        df['Lexicon-based sentiment'] = df['Score'].apply(lambda x: sentiment_tag(x))
        dataset = df['Lemmas'].tolist()
        dataset = [" ".join(li) for li in dataset]
        tfidf_matrix = vectorizer.fit_transform(dataset)
        X, y = tfidf_matrix, df['Lexicon-based sentiment']
        rS = RandomOverSampler()
        X, y = rS.fit_resample(X, y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=42)

        model = SGDClassifier(alpha=5e-6, fit_intercept=True, learning_rate='optimal')
        model.fit(X_train, y_train)
        y_predicts = model.predict(X_test)
        print(classification_report(y_test, y_predicts))
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import SGDClassifier
# from sklearn.metrics import classification_report
#
#
# def sentiment_process(sc):
#     if sc > 5:
#         return 1
#     return 0
#
#
# input_ = input()
# # path = "data.pkl"
# # data = pd.read_pickle(input_)
# data = pd.read_csv(input_, nrows=150000)


