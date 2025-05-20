import random, configs, nltk

from nltk.parse.corenlp import transform
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

def intent_classifier():
    X_text = ["Дратути", "Покедова", "Чё как", "Представься", "Салют", "Бывай", "Как дела", "Как твоё имя", "Да"]
    y = ['hello', 'goodbye', 'whatsup', 'name', 'hello', 'goodbye', 'whatsup', 'name', 'yes']
    for intent, intent_data in configs.INTENTS_DICTIONARY.items():
        for example in intent_data['examples']:
            X_text.append(example)
            y.append(intent)
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3))
    X = vectorizer.fit_transform(X_text)
    clf = LinearSVC()
    clf.fit(X, y)
    return clf, vectorizer

def answer_classifier(dialogs):
    X_text = []
    y = []
    for question, answer in dialogs:
        X_text.append(question)
        y.append(answer)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_text)
    clf = LogisticRegression()
    clf.fit(X, y)
    return clf, vectorizer

def clear_str(r):
    r = r.lower()
    alphabet = configs.ALPHABET
    r = [c for c in r if c in alphabet]
    return ''.join(r)

def load_dialogs():
    with open('dialogues.txt', encoding="utf-8") as f:
        content = f.read()
    blocks = content.split("\n")
    dialogs = []
    for b in blocks:
        dialog = b.split('\\')[:2]
        if len(dialog) == 2:
            pair = [clear_str(dialog[0]), dialog[1]]
            if pair[0] and pair[1]:
                dialogs.append(pair)
    return dialogs

def get_answer(replica, dialogs, clf, vectorizer):
    replica = clear_str(replica)
    replica_text = vectorizer.transform([replica]).toarray()[0]
    answer = clf.predict([replica_text])[0]
    for q, a in dialogs:
        if a == answer:
            q = clear_str(q)
            distance = nltk.edit_distance(replica, q)
            if distance / len (q) <= 0.7:
                return answer

def classify_intent(question, clf, vectorizer):
    question = clear_str(question)
    intent = clf.predict(vectorizer.transform([question]))[0]
    for example in configs.INTENTS_DICTIONARY[intent]["examples"]:
        example = clear_str(example)
        distance = nltk.edit_distance(question, example)
        if example and distance / len(example) <= 0.45:
            return intent

def answer_by_intent(intent):
    image = None
    if intent in configs.INTENTS_DICTIONARY:
        responses_vars = configs.INTENTS_DICTIONARY[intent]["answers"]
        if "theme_app" in configs.INTENTS_DICTIONARY[intent]:
            if configs.INTENTS_DICTIONARY[intent]["theme_app"][0] == 'furniture_q_demand_advert':
                image = f"images/{configs.INTENTS_DICTIONARY[intent]["theme_gen"]}.jpg"
        return random.choice(responses_vars), image

def failure():
    phrases = configs.FAILURE
    return random.choice(phrases)

def bot(question):
    dialogs = load_dialogs()
    clf, vectorizer = intent_classifier()
    clf1, vectorizer1 = answer_classifier(dialogs)
    intent = classify_intent(question, clf, vectorizer)
    if intent:
        return answer_by_intent(intent)
    answer = get_answer(question, dialogs, clf1, vectorizer1)
    if answer: return answer, ""
    else: return failure(), ""

def orders_record(articule_number, fio, contact_info, address_data, payment):
    f = open("orders.txt", "a")
    order = f"ФИО: {fio}\nАртикул: {articule_number}\nКонтакты: {contact_info}\nАдрес доставки: {address_data}\nОплата {payment.lower()}\n\n"
    f.writelines(order)
    f.close()