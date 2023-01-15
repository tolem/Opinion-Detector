# write yor code here
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

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
            ftext = nltk.regexp_tokenize(text, r'[A-z]+')
            ftext = " ".join(ftext).lower()
            ftext = lemmatizer.lemmatize(ftext, pos='n')
            filterd_review = [lemmatizer.lemmatize(word, pos='n') for word in ftext.split() if word not in english_stopwords]
            return filterd_review

        df = pd.DataFrame(data=opinion)
        df['Lemmas'] = df['Review'].apply(lambda x: filter_word(x))
        # print(df['Lemmas'].head(), df['Lemmas'].tail(), sep='\n')


        def gen(w):
            for i in w:
                yield i

        def add_one(sent):
            with open('file/positive_words.txt', 'r') as positive:
                pos_file = set({w.strip() for w in positive.readlines()})
                # print(pd.Series(['sister goodwill']).isin(pos_file))
                count = sum([1 for s in sent if s in pos_file])
                # print(count, pos_file)
                # exit(1)
                return count

        def sub_one(sent):
            with open('file/negative_words.txt', 'r') as negative:
                neg_file = set({w.strip() for w in negative.readlines()})
                count = sum([1 for s in sent if s in neg_file])
                return count

        df['Score'] = df['Lemmas'].apply(lambda x: add_one(x))
        df['Score'] = df['Score'] - (df['Lemmas'].apply(lambda x: sub_one(x)))
        # print(df['Score'].head())

        def sentiment_tag(mark):
            if -3 <= mark <= 3:
                return "Neutral"

            if mark > 3:
                return "Positive"

            if mark < -3:
                return "Negative"


        df['Lexicon-based sentiment'] = df['Score'].apply(lambda x: sentiment_tag(x))
        explode = [0.0, 0.08, 0.0]
        colors = ['saddlebrown', 'wheat', 'crimson']
        df.groupby('Lexicon-based sentiment').size().plot( kind='pie', autopct='%.1f')
        plt.show()

        neutral = df['Lexicon-based sentiment'][df['Lexicon-based sentiment'] == 'Neutral'].count() / df['Lexicon-based sentiment'].count()
        positive = df['Lexicon-based sentiment'][df['Lexicon-based sentiment'] =='Positive'].count() / df['Lexicon-based sentiment'].count()
        negative = df['Lexicon-based sentiment'][df['Lexicon-based sentiment'] == 'Negative'].count() / df['Lexicon-based sentiment'].count()
        difference = (positive - negative) * 100
        val = {'Neutral': neutral, 'Positive': positive, 'Negative': negative}
        max_percent = max(val, key=val.get)
        min_percent = min(val, key=val.get)
        min_percent = val[min_percent] * 100

        print(f"The answer to the 1st question: {max_percent}")
        print(f"The answer to the 2nd question: {int(min_percent)}%")
        print(f"The answer to the 3rd question: {int(difference)}%")
