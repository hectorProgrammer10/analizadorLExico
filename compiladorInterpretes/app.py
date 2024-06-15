from flask import Flask, render_template, request, jsonify
from ply import lex, yacc

app = Flask(__name__)

# Lista de palabras reservadas
reserved = {
    'if': 'RESERVADA',
    'else': 'RESERVADA',
    'elif': 'RESERVADA',
    'while': 'RESERVADA',
    'for': 'RESERVADA',
    'in': 'RESERVADA',
    'break': 'RESERVADA',
    'continue': 'RESERVADA',
    'def': 'RESERVADA',
    'return': 'RESERVADA',
    'import': 'RESERVADA',
    'from': 'RESERVADA',
    'as': 'RESERVADA',
    'class': 'RESERVADA',
    'try': 'RESERVADA',
    'except': 'RESERVADA',
    'finally': 'RESERVADA',
    'with': 'RESERVADA',
    'lambda': 'RESERVADA',
    'yield': 'RESERVADA',
    'int': 'RESERVADA',
    'system': 'RESERVADA',
    'out': 'RESERVADA',
    'println': 'RESERVADA',
    'char': 'RESERVADA',
    'float': 'RESERVADA'
}

# Lista de tokens
tokens = [
    'LPAREN',  # (
    'RPAREN',  # )
    'LBRACE',  # {
    'RBRACE',  # }
    'SEMICOLON',  # ;
    'PLUS',  # ++
    'EQ',  # =
    'LEQ',  # <=
    'DOT',  # .
    'STRING',  # "..."
    'ID',  # Identificadores
    'DIGITO'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_PLUS = r'\+\+'
t_EQ = r'='
t_LEQ = r'<='
t_DOT = r'\.'
t_STRING = r'\".*?\"'


def t_DIGITO(t):
    r'\d+'
    t.type = 'DIGITO'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
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

# Definir la gramática para el analizador sintáctico


def p_program(p):
    '''program : declaration for_loop
               | for_loop'''
    p[0] = "Correcto"


def p_declaration(p):
    '''declaration : tipo ID SEMICOLON'''
    p[0] = p[1]


def p_for_loop(p):
    '''for_loop : RESERVADA LPAREN for_initialization SEMICOLON for_condition SEMICOLON for_increment RPAREN LBRACE statement RBRACE'''
    p[0] = "Correcto"


def p_for_initialization(p):
    '''for_initialization : tipo ID EQ DIGITO
                          | ID EQ DIGITO'''
    p[0] = p[1]


def p_for_condition(p):
    '''for_condition : ID LEQ DIGITO'''
    p[0] = p[1]


def p_for_increment(p):
    '''for_increment : ID PLUS'''
    p[0] = p[1]


def p_tipo(p):
    '''tipo : RESERVADA'''
    p[0] = p[1]


def p_statement(p):
    '''statement : RESERVADA DOT RESERVADA DOT RESERVADA LPAREN ID RPAREN SEMICOLON'''
    p[0] = "Correcto"


# Variable para almacenar el token donde ocurre el error
syntax_error_token = None


def p_error(p):
    global syntax_error_token
    syntax_error_token = p
    if p:
        print(f'Error de sintaxis en {p.value} en la posición {p.lexpos}')
    else:
        print('Error de sintaxis en EOF')


# Crear un objeto parser
parser = yacc.yacc()

# Función para realizar el análisis semántico


def analizar_semantico(codigo):
    lexer.input(codigo)
    tipo_declarado = None
    variable_declarada = None
    tokens = []

    for token in lexer:
        tokens.append(token)
        if token.type in ['char', 'int', 'float'] and not tipo_declarado:
            tipo_declarado = token.type
        if token.type == 'ID' and not variable_declarada:
            variable_declarada = token.value

    if tipo_declarado and variable_declarada:
        return "Análisis semántico correcto"
    else:
        return "Análisis semántico incorrecto"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analizar', methods=['POST'])
def analizar():
    datos_recibidos = request.json['codigo']
    tokens_analizados = []

    # Configurar el lexer con los datos recibidos
    lexer.input(datos_recibidos)

    # Iterar sobre los tokens analizados
    for token in lexer:
        tokens_analizados.append({'valor': token.value, 'tipo': token.type})

    return jsonify(tokens_analizados)


@app.route('/analizarSintactico', methods=['POST'])
def analizar_sintactico():
    global syntax_error_token
    syntax_error_token = None

    datos_recibidos = request.json['codigo']
    result = parser.parse(datos_recibidos)

    if result == "Correcto":
        return jsonify({'resultado': 'La estructura for es correcta'})
    else:
        error_info = {
            'resultado': 'Error en la estructura for',
            'token': syntax_error_token.value if syntax_error_token else None,
            'posicion': syntax_error_token.lexpos if syntax_error_token else None
        }
        return jsonify(error_info)


@app.route('/analizarSemantico', methods=['POST'])
def analizar_semantico_route():
    datos_recibidos = request.json['codigo']
    resultado = analizar_semantico(datos_recibidos)
    return jsonify({'resultado': resultado})


if __name__ == '__main__':
    app.run(debug=True, port=8081)
