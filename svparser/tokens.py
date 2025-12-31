TOKENS = [
    ('MODULE',     r'\bmodule\b'),
    ('ENDMODULE',  r'\bendmodule\b'),
    ('INPUT',      r'\binput\b'),
    ('OUTPUT',     r'\boutput\b'),
    ('ASSIGN',     r'\bassign\b'),
    ('ALWAYS',     r'\balways\b'),
    ('BEGIN',      r'\bbegin\b'),
    ('END',        r'\bend\b'),

    ('EQUALFF',    r'<='),
    ('EQUAL',      r'='),
    ('RIPPLEADD', r'\+R'),
    ('CLAADD',    r'\+C'),
    ('RIPPLESUB', r'-R'),
    ('CLASUB',    r'-C'),

    ('AND',        r'&'),
    ('OR',         r'\|'),
    ('XOR',        r'\^'),
    ('NOT',        r'~'),

    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('LBRACK',     r'\['),
    ('RBRACK',     r'\]'),
    ('SEMICOL',    r';'),
    ('COMMA',      r','),
    ('COLON',      r':'),
    ('AT',         r'@'),

    ('POSEDGE',    r'\bposedge\b'),
    ('NEGEDGE',    r'\bnegedge\b'),

    ('LOGIC',      r'\b(0|1)\b'),
    ('NUMBER',     r'\d+'),
    ('IDENT',      r'[a-zA-Z_][a-zA-Z0-9_]*'),

    ('WS',         r'\s+'),
    ('COMMENT',    r'//.*?$'),
    ('MCOMMENT',   r'/\*.*?\*/'),
]
