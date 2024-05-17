from flask import Flask, render_template, request, jsonify
from ply import lex
app = Flask(__name__)

# Lista de palabras reservadas válidas
reserved_keywords = {'programa', 'int', 'read', 'printf', 'end'}
# Lista de palabras reservadas
reserved = {
    'programa': 'RESERVADA',
    'int': 'RESERVADA',
    'read': 'RESERVADA',
    'printf': 'RESERVADA',
    'end': 'RESERVADA'
}


def is_similar_to_reserved(word):
    for keyword in reserved_keywords:
        if keyword.startswith(word):
            return True
    return False


# Lista de tokens
tokens = [
    'ID',  # Identificador
    'LPAREN',  # (
    'RPAREN',  # )
    'SIM',
    'ERROR'
] + list(reserved.values())

# Expresiones regulares para tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SIM = r'[;+\-/*=]'


def t_ID(t):
    r'[a-zA-Z]+'
    # Verificar si es una palabra reservada similar a una válida
    if t.value in reserved:
        t.type = reserved[t.value]
    elif is_similar_to_reserved(t.value):
        t.type = 'ERROR'
    else:
        t.type = 'ID'
    return t


# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Manejo de errores léxicos


def t_error(t):
    print(f'Carácter ilegal: {t.value[0]}')
    t.lexer.skip(1)


# Crear un objeto lexer
lexer = lex.lex()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analizar', methods=['POST'])
def analizar():
    datos_recibidos = request.json
    tokens_analizados = []

    # Configurar el lexer con los datos recibidos
    lexer.input(datos_recibidos)

    # Iterar sobre los tokens analizados
    for token in lexer:
        tokens_analizados.append({'valor': token.value, 'tipo': token.type})

    return jsonify(tokens_analizados)


if __name__ == '__main__':
    app.run(debug=True, port=8081)
