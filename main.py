from ai import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    language = None
    if request.args.get('random') != None:
        language = generate_language()
    elif request.method == 'POST':
        language = request.form['language']
        language = [l for l in language.split(",") if len(l) != 0]

    data = None
    if language != None:
        model = load_model()
        data = {
            'input': str_list(language),
            'language': language,
            'precision': test_precision(model, 5000),
            'is_code_by_IA': bool(is_code_by_IA(model, language)),
            'is_code_by_sardinas': is_code_by_sardinas(language)
        }
        print(data)

    return render_template('index.html', result=data)

def main():
    generate_new_model(5000)

if __name__ == "__main__":
    main()
