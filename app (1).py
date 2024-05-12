from flask import Flask, render_template, request
import pymorphy3

app = Flask(__name__)

morph = pymorphy3.MorphAnalyzer(lang='uk')


def read_dialects(file):
    dialects_dict = []
    meanings_dict = []
    with open(file, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                dialect, meaning = line.strip().split(':', 1)
                dialects_dict.append(dialect.strip())
                meanings_dict.append(meaning.strip())
    return dialects_dict, meanings_dict


def to_infinitive(word):
    parsed_word = morph.parse(word)[0]
    return parsed_word.normal_form


def find_dialects(text, dialects1, meanings1):
    found_dialects = set()
    not_recognized = set()
    for word in text.split():
        word = word.strip('.,?!')
        if word and word.isalpha():
            parsed_word = morph.parse(word)
            recognized = False
            for variant in parsed_word:
                normal_form = variant.normal_form
                if normal_form in dialects1:
                    i = dialects1.index(normal_form)
                    found_dialects.add((normal_form, meanings1[i]))
                    recognized = True
                for form in variant.lexeme:
                    if form in dialects1:
                        i = dialects1.index(form)
                        found_dialects.add((form, meanings1[i]))
                        recognized = True
            if not recognized:
                not_recognized.add(word)
    print("Нераспознанные слова:", not_recognized)
    return list(found_dialects)


file_path = "./prepared_corpus.txt"

dialects, meanings = read_dialects(file_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        user_text = request.form['text']
        found_dialects = find_dialects(user_text, dialects, meanings)
        return render_template('index.html', found_dialects=found_dialects)


if __name__ == '__main__':
    app.run(debug=True)
