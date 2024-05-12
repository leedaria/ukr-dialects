from flask import Flask, render_template, request, redirect, url_for
import pymorphy3

app = Flask(__name__, template_folder='C:/pythonProject3')

morph = pymorphy3.MorphAnalyzer(lang='uk')

def read_dialects(file_path):
    dialects = []
    meanings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                dialect, meaning = line.strip().split(':', 1)
                dialects.append(dialect.strip())
                meanings.append(meaning.strip())
    return dialects, meanings

def to_infinitive(word):
    parsed_word = morph.parse(word)[0]
    return parsed_word.normal_form

def find_dialects(text, dialects, meanings):
    found_dialects = set()
    not_recognized = set()
    for word in text.split():
        word = word.strip('.,?!')
        if word and word.isalpha():
            parsed_word = morph.parse(word)
            recognized = False
            for variant in parsed_word:
                normal_form = variant.normal_form
                if normal_form in dialects:
                    index = dialects.index(normal_form)
                    found_dialects.add((normal_form, meanings[index]))
                    recognized = True
                for form in variant.lexeme:
                    if form in dialects:
                        index = dialects.index(form)
                        found_dialects.add((form, meanings[index]))
                        recognized = True
            if not recognized:
                not_recognized.add(word)
    print("Нераспознанные слова:", not_recognized)
    return list(found_dialects)


file_path = "C:\pythonProject3\prepared_corpus.txt"

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
