import tkinter as tk
import numpy as np
from tkinter import filedialog

def open_file_dialog():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename()
    
    if file_path:
        print("Arquivo selecionado:", file_path)
        return file_path
    else:
        raise ValueError("Nenhum arquivo selecionado.")
        

def get_tokens(lex):
    if lex in dicionario.values():
        for key, value in dicionario.items():
            if lex == value:
                #tokens.append(key)
                return key
                break
    elif lex.startswith("'") and lex.endswith("'"):
        # tokens.append(23)#token vstring
        return 23
    elif lex.startswith('"') and lex.endswith('"'):
        # tokens.append(13)#token literal
        return 13
    elif lex.isnumeric():
        # tokens.append(12)#token nint
        return 12
    elif "." in lex:
        plex = lex.split(".")
        if plex[0].isnumeric() and plex[1].isnumeric():
            # tokens.append(11)
            return 11
    else:
        # tokens.append(16)#token ident
        return 16        

if __name__ == "__main__":
    try:
        file_path = open_file_dialog()
    except ValueError as e:
        print(e)
        exit(-1)
try:
    with open(file_path, 'r') as arquivo:
        #palavras = arquivo.read().split(" ")
        linhas = arquivo.readlines()
        conteudo = arquivo.read().strip()
        conteudo = " ".join(conteudo.split())
except FileNotFoundError:
    print("O arquivo não foi encontrado.")
    exit(-1)
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    exit(-1)


#--------------------------------------------------------------
#                   COMEÇA CODIGO LEXICO
#--------------------------------------------------------------


lexema = ''

tokens = []

dicionario = {}

dicionario[1] = 'while'
dicionario[2] = 'var'
dicionario[3] = 'to'
dicionario[4] = 'then'
dicionario[5] = 'string'
dicionario[6] = 'real'
dicionario[7] = 'read'
dicionario[8] = 'program'
dicionario[9] = 'procedure'
dicionario[10] = 'print'
dicionario[14] = 'integer'
dicionario[15] = 'if'
dicionario[17] = 'for'
dicionario[18] = 'end'
dicionario[19] = 'else'
dicionario[20] = 'do'
dicionario[21] = 'const'
dicionario[22] = 'begin'
dicionario[24] = '>='
dicionario[25] = '>'
dicionario[26] = '='
dicionario[27] = '<>'
dicionario[28] = '<='
dicionario[29] = '<'
dicionario[30] = '+'
dicionario[31] = ';'
dicionario[32] = ':='
dicionario[33] = ':'
dicionario[34] = '/'
dicionario[35] = '.'
dicionario[36] = ','
dicionario[37] = '*'
dicionario[38] = ')'
dicionario[39] = '('
dicionario[40] = '{'
dicionario[41] = '}'
dicionario[42] = '-'
dicionario[45] = '//'

#futuramente usar uma dataclass, isso aqui ta muito feio
# from dataclasses import dataclass

# @dataclass(frozen=True)
# class Word:
#     string: str
#     line: int
#     token: int

collec = [("",1,2)]#teste

# erros = []

lista_operadores = ('=','+','-','/','*','(',')',':','<','>','{','}',';')
lista_operadores_duplos = ('>=','<>','<=',':=')

is_comment = False
is_line_comment = False
comment_len = 0
is_string = False
is_literal = False
is_error = False
is_real = False


for j in range(0,len(linhas)):
    linha_atual = j+1
    conteudo = linhas[j].strip()
    #conteudo = " ".join(conteudo.split())
    collec.append((lexema, get_tokens(lexema), linha_atual))
    lexema = ""
    if is_line_comment:
        is_comment = False
        is_line_comment = False
    for i in range(0,len(conteudo)):
        if is_error and conteudo[i] !=" ":
            lexema = lexema + conteudo[i]
        elif is_error and conteudo[i] == " ":
            # erros.append(lexema)
            collec.append((lexema, get_tokens(lexema), linha_atual))
            lexema = ""
        elif is_comment and (conteudo[i] != '/' or is_line_comment):
            comment_len +=1
            continue
        elif is_comment and conteudo[i] == '/' and conteudo[i-1] == '/' and not is_line_comment and comment_len > 1:
            is_comment = False
            continue
        elif is_comment and conteudo[i] == '/' and conteudo[i-1] != '/':
            comment_len +=1
            continue
        elif is_string and conteudo[i] != "'":
            lexema = lexema+conteudo[i]
            continue
        elif is_string and conteudo[i] == "'":
            is_string = False
            lexema = lexema+conteudo[i]
            collec.append((lexema, get_tokens(lexema), linha_atual))
            lexema = ""
            continue
        elif is_literal and conteudo[i] != '"':
            lexema = lexema+conteudo[i]
            continue
        elif is_literal and conteudo[i] == '"':
            is_literal = False
            lexema = lexema+conteudo[i]
            collec.append((lexema, get_tokens(lexema), linha_atual))
            lexema = ""
            continue
        elif conteudo[i] == '"':
            collec.append((lexema, get_tokens(lexema), linha_atual))
            lexema = conteudo[i]
            is_literal = True
        elif conteudo[i] == "'":
            collec.append((lexema, get_tokens(lexema), linha_atual))
            lexema = conteudo[i]
            is_string = True    
        elif conteudo[i].isdigit():
            try:
                if conteudo[i+1].isdigit() or conteudo[i+1] == " ":
                    lexema = lexema+conteudo[i]
                elif conteudo[i+1] == '.':
                    if not is_real:
                        is_real = True
                        lexema = lexema+conteudo[i]
                    else:
                        is_error = True
                elif conteudo[i+1] in lista_operadores:
                    lexema = lexema + conteudo[i]
                    collec.append((lexema, get_tokens(lexema), linha_atual))
                    lexema = ""
            except IndexError:
                lexema = lexema+conteudo[i]
        elif conteudo[i] == '.':
            if conteudo[i-1].isdigit():
                lexema = lexema+conteudo[i]
            else:
                collec.append((lexema, get_tokens(lexema), linha_atual))
                lexema = conteudo[i]
                collec.append((lexema, get_tokens(lexema), linha_atual))
                lexema = ""
        elif conteudo[i] == '/':
            try:
                if conteudo[i+1] == '/':
                    is_comment = True
                    comment_len = 0;
                    try:
                        if conteudo[i+2] == '/':
                            is_line_comment = True
                    except IndexError:
                        continue
                else:
                    raise IndexError
            except IndexError:
                collec.append((lexema, get_tokens(lexema), linha_atual))
                lexema = conteudo[i]
        elif conteudo[i] == ":":
            collec.append((lexema, get_tokens(lexema), linha_atual))
            lexema = conteudo[i] # lexema = ":"
            if conteudo[i+1] != "=":
                collec.append((lexema, get_tokens(lexema), linha_atual))
                lexema = ""
        elif conteudo[i] in lista_operadores:
            if (conteudo[i-1]+conteudo[i]) in lista_operadores_duplos:
                lexema = lexema + conteudo[i]
                collec.append((lexema, get_tokens(lexema), linha_atual))
                lexema=""
            else:
                try:
                    if (conteudo[i]+conteudo[i+1]) in lista_operadores_duplos:
                        collec.append((lexema, get_tokens(lexema), linha_atual))
                        lexema = conteudo[i]
                    else:
                        raise IndexError
                except IndexError:
                    collec.append((lexema, get_tokens(lexema), linha_atual))
                    lexema = conteudo[i]
                    collec.append((lexema, get_tokens(lexema), linha_atual))
                    lexema=""
        elif conteudo[i] == ' ':
            collec.append((lexema, get_tokens(lexema), linha_atual))
            lexema = ""
        elif conteudo[i].isalpha():
            lexema = lexema+conteudo[i]
    

        
#print(linhas)

print(len(collec))

collec = [x for x in collec if x[0] != ""]

print(len(collec))
         
lexemas = [item[0] for item in collec]
tokens = [item[1] for item in collec]
        
#Entrega do lexico - token - lexema - linha
for i in range(0,len(collec)):
    # print(f"Token: '{str(collec[i][1])}' - Lexema: '{str(collec[i][0])}' - Linha: {str(collec[i][2])}" )
    print(f'{str(collec[i][1])}, ')


#import numpy as np
#import lexical as lex

class TabParsing:
    def __init__(self):
        self.tabParsing = [[0 for _ in range(1,46)] for _ in range(1,75)]
        self.producoes = [[0 for _ in range(1,10)] for _ in range(1,67)]

    def inicializarTab(self):
        self.tabParsing = [[0 for _ in range(45)] for _ in range(73)]

        self.tabParsing[45][8]=1
        self.tabParsing[46][2]=2
        self.tabParsing[46][21]=2
        self.tabParsing[47][22]=20
        self.tabParsing[48][2]=4
        self.tabParsing[48][21]=3
        self.tabParsing[49][2]=5
        self.tabParsing[50][9]=14
        self.tabParsing[50][22]=15
        self.tabParsing[51][1]=21
        self.tabParsing[51][7]=21
        self.tabParsing[51][10]=21
        self.tabParsing[51][15]=21
        self.tabParsing[51][16]=21
        self.tabParsing[51][17]=21
        self.tabParsing[51][18]=22
        self.tabParsing[52][16]=6
        self.tabParsing[53][5]=13
        self.tabParsing[53][6]=12
        self.tabParsing[53][14]=11
        self.tabParsing[54][9]=10
        self.tabParsing[54][16]=9
        self.tabParsing[54][22]=10
        self.tabParsing[55][33]=7
        self.tabParsing[55][36]=8
        self.tabParsing[56][31]=17
        self.tabParsing[56][39]=16
        self.tabParsing[57][36]=18
        self.tabParsing[57][38]=19
        self.tabParsing[58][1]=63
        self.tabParsing[58][7]=64
        self.tabParsing[58][10]=23
        self.tabParsing[58][15]=41
        self.tabParsing[58][16]=51
        self.tabParsing[58][17]=52
        self.tabParsing[59][11]=24
        self.tabParsing[59][12]=24
        self.tabParsing[59][13]=24
        self.tabParsing[59][16]=24
        self.tabParsing[59][23]=24
        self.tabParsing[59][39]=24
        self.tabParsing[60][36]=26
        self.tabParsing[60][41]=25
        self.tabParsing[61][11]=27
        self.tabParsing[61][12]=27
        self.tabParsing[61][13]=27
        self.tabParsing[61][16]=27
        self.tabParsing[61][23]=27
        self.tabParsing[61][39]=27
        self.tabParsing[62][11]=31
        self.tabParsing[62][12]=31
        self.tabParsing[62][13]=31
        self.tabParsing[62][16]=31
        self.tabParsing[62][23]=31
        self.tabParsing[62][39]=31
        self.tabParsing[63][3]=30
        self.tabParsing[63][4]=30
        self.tabParsing[63][20]=30
        self.tabParsing[63][24]=30
        self.tabParsing[63][25]=30
        self.tabParsing[63][26]=30
        self.tabParsing[63][27]=30
        self.tabParsing[63][28]=30
        self.tabParsing[63][29]=30
        self.tabParsing[63][30]=28
        self.tabParsing[63][31]=30
        self.tabParsing[63][36]=30
        self.tabParsing[63][38]=30
        self.tabParsing[63][41]=30
        self.tabParsing[63][42]=29
        self.tabParsing[64][11]=38
        self.tabParsing[64][12]=37
        self.tabParsing[64][13]=39
        self.tabParsing[64][16]=36
        self.tabParsing[64][23]=40
        self.tabParsing[64][39]=35
        self.tabParsing[65][3]=34
        self.tabParsing[65][4]=34
        self.tabParsing[65][20]=34
        self.tabParsing[65][24]=34
        self.tabParsing[65][25]=34
        self.tabParsing[65][26]=34
        self.tabParsing[65][27]=34
        self.tabParsing[65][28]=34
        self.tabParsing[65][29]=34
        self.tabParsing[65][30]=34
        self.tabParsing[65][31]=34
        self.tabParsing[65][34]=33
        self.tabParsing[65][36]=34
        self.tabParsing[65][37]=32
        self.tabParsing[65][38]=34
        self.tabParsing[65][41]=34
        self.tabParsing[65][42]=34
        self.tabParsing[66][11]=42
        self.tabParsing[66][12]=42
        self.tabParsing[66][13]=42
        self.tabParsing[66][16]=42
        self.tabParsing[66][23]=42
        self.tabParsing[66][39]=42
        self.tabParsing[67][19]=49
        self.tabParsing[67][31]=50
        self.tabParsing[68][24]=48
        self.tabParsing[68][25]=46
        self.tabParsing[68][26]=43
        self.tabParsing[68][27]=44
        self.tabParsing[68][28]=47
        self.tabParsing[68][29]=45
        self.tabParsing[69][31]=53
        self.tabParsing[69][32]=54
        self.tabParsing[69][39]=53
        self.tabParsing[70][31]=56
        self.tabParsing[70][39]=55
        self.tabParsing[71][11]=59
        self.tabParsing[71][12]=58
        self.tabParsing[71][13]=65
        self.tabParsing[71][16]=57
        self.tabParsing[71][23]=60
        self.tabParsing[72][36]=61
        self.tabParsing[72][38]=62


    def inicializarProdu(self):
        self.producoes[1][1] = 8
        self.producoes[1][2] = 16
        self.producoes[1][3] = 31
        self.producoes[1][4] = 46
        self.producoes[1][5] = 47
        self.producoes[1][6] = 35
        self.producoes[1][7] = 0
        self.producoes[1][8] = 0
        self.producoes[2][1] = 48
        self.producoes[2][2] = 49
        self.producoes[2][3] = 50
        self.producoes[2][4] = 0
        self.producoes[2][5] = 0
        self.producoes[2][6] = 0
        self.producoes[2][7] = 0
        self.producoes[2][8] = 0
        self.producoes[3][1] = 21
        self.producoes[3][2] = 16
        self.producoes[3][3] = 26
        self.producoes[3][4] = 12
        self.producoes[3][5] = 31
        self.producoes[3][6] = 48
        self.producoes[3][7] = 0
        self.producoes[3][8] = 0
        self.producoes[4][1] = 44
        self.producoes[4][2] = 0
        self.producoes[4][3] = 0
        self.producoes[4][4] = 0
        self.producoes[4][5] = 0
        self.producoes[4][6] = 0
        self.producoes[4][7] = 0
        self.producoes[4][8] = 0
        self.producoes[5][1] = 2
        self.producoes[5][2] = 52
        self.producoes[5][3] = 33
        self.producoes[5][4] = 53
        self.producoes[5][5] = 31
        self.producoes[5][6] = 54
        self.producoes[5][7] = 0
        self.producoes[5][8] = 0
        self.producoes[6][1] = 16
        self.producoes[6][2] = 55
        self.producoes[6][3] = 0
        self.producoes[6][4] = 0
        self.producoes[6][5] = 0
        self.producoes[6][6] = 0
        self.producoes[6][7] = 0
        self.producoes[6][8] = 0
        self.producoes[7][1] = 44
        self.producoes[7][2] = 0
        self.producoes[7][3] = 0
        self.producoes[7][4] = 0
        self.producoes[7][5] = 0
        self.producoes[7][6] = 0
        self.producoes[7][7] = 0
        self.producoes[7][8] = 0
        self.producoes[8][1] = 36
        self.producoes[8][2] = 16
        self.producoes[8][3] = 55
        self.producoes[8][4] = 0
        self.producoes[8][5] = 0
        self.producoes[8][6] = 0
        self.producoes[8][7] = 0
        self.producoes[8][8] = 0
        self.producoes[9][1] = 52
        self.producoes[9][2] = 33
        self.producoes[9][3] = 53
        self.producoes[9][4] = 31
        self.producoes[9][5] = 54
        self.producoes[9][6] = 0
        self.producoes[9][7] = 0
        self.producoes[9][8] = 0
        self.producoes[10][1] = 44
        self.producoes[10][2] = 0
        self.producoes[10][3] = 0
        self.producoes[10][4] = 0
        self.producoes[10][5] = 0
        self.producoes[10][6] = 0
        self.producoes[10][7] = 0
        self.producoes[10][8] = 0
        self.producoes[11][1] = 14
        self.producoes[11][2] = 0
        self.producoes[11][3] = 0
        self.producoes[11][4] = 0
        self.producoes[11][5] = 0
        self.producoes[11][6] = 0
        self.producoes[11][7] = 0
        self.producoes[11][8] = 0
        self.producoes[12][1] = 6
        self.producoes[12][2] = 0
        self.producoes[12][3] = 0
        self.producoes[12][4] = 0
        self.producoes[12][5] = 0
        self.producoes[12][6] = 0
        self.producoes[12][7] = 0
        self.producoes[12][8] = 0
        self.producoes[13][1] = 5
        self.producoes[13][2] = 0
        self.producoes[13][3] = 0
        self.producoes[13][4] = 0
        self.producoes[13][5] = 0
        self.producoes[13][6] = 0
        self.producoes[13][7] = 0
        self.producoes[13][8] = 0
        self.producoes[14][1] = 9
        self.producoes[14][2] = 16
        self.producoes[14][3] = 56
        self.producoes[14][4] = 31
        self.producoes[14][5] = 47
        self.producoes[14][6] = 31
        self.producoes[14][7] = 50
        self.producoes[14][8] = 0
        self.producoes[15][1] = 44
        self.producoes[15][2] = 0
        self.producoes[15][3] = 0
        self.producoes[15][4] = 0
        self.producoes[15][5] = 0
        self.producoes[15][6] = 0
        self.producoes[15][7] = 0
        self.producoes[15][8] = 0
        self.producoes[16][1] = 39
        self.producoes[16][2] = 52
        self.producoes[16][3] = 33
        self.producoes[16][4] = 53
        self.producoes[16][5] = 57
        self.producoes[16][6] = 38
        self.producoes[16][7] = 0
        self.producoes[16][8] = 0
        self.producoes[17][1] = 44
        self.producoes[17][2] = 0
        self.producoes[17][3] = 0
        self.producoes[17][4] = 0
        self.producoes[17][5] = 0
        self.producoes[17][6] = 0
        self.producoes[17][7] = 0
        self.producoes[17][8] = 0
        self.producoes[18][1] = 36
        self.producoes[18][2] = 52
        self.producoes[18][3] = 33
        self.producoes[18][4] = 53
        self.producoes[18][5] = 57
        self.producoes[18][6] = 0
        self.producoes[18][7] = 0
        self.producoes[18][8] = 0
        self.producoes[19][1] = 44
        self.producoes[19][2] = 0
        self.producoes[19][3] = 0
        self.producoes[19][4] = 0
        self.producoes[19][5] = 0
        self.producoes[19][6] = 0
        self.producoes[19][7] = 0
        self.producoes[19][8] = 0
        self.producoes[20][1] = 22
        self.producoes[20][2] = 51
        self.producoes[20][3] = 18
        self.producoes[20][4] = 0
        self.producoes[20][5] = 0
        self.producoes[20][6] = 0
        self.producoes[20][7] = 0
        self.producoes[20][8] = 0
        self.producoes[21][1] = 58
        self.producoes[21][2] = 31
        self.producoes[21][3] = 51
        self.producoes[21][4] = 0
        self.producoes[21][5] = 0
        self.producoes[21][6] = 0
        self.producoes[21][7] = 0
        self.producoes[21][8] = 0
        self.producoes[22][1] = 44
        self.producoes[22][2] = 0
        self.producoes[22][3] = 0
        self.producoes[22][4] = 0
        self.producoes[22][5] = 0
        self.producoes[22][6] = 0
        self.producoes[22][7] = 0
        self.producoes[22][8] = 0
        self.producoes[23][1] = 10
        self.producoes[23][2] = 40
        self.producoes[23][3] = 59
        self.producoes[23][4] = 60
        self.producoes[23][5] = 41
        self.producoes[23][6] = 0
        self.producoes[23][7] = 0
        self.producoes[23][8] = 0
        self.producoes[24][1] = 61
        self.producoes[24][2] = 0
        self.producoes[24][3] = 0
        self.producoes[24][4] = 0
        self.producoes[24][5] = 0
        self.producoes[24][6] = 0
        self.producoes[24][7] = 0
        self.producoes[24][8] = 0
        self.producoes[25][1] = 44
        self.producoes[25][2] = 0
        self.producoes[25][3] = 0
        self.producoes[25][4] = 0
        self.producoes[25][5] = 0
        self.producoes[25][6] = 0
        self.producoes[25][7] = 0
        self.producoes[25][8] = 0
        self.producoes[26][1] = 36
        self.producoes[26][2] = 59
        self.producoes[26][3] = 60
        self.producoes[26][4] = 0
        self.producoes[26][5] = 0
        self.producoes[26][6] = 0
        self.producoes[26][7] = 0
        self.producoes[26][8] = 0
        self.producoes[27][1] = 62
        self.producoes[27][2] = 63
        self.producoes[27][3] = 0
        self.producoes[27][4] = 0
        self.producoes[27][5] = 0
        self.producoes[27][6] = 0
        self.producoes[27][7] = 0
        self.producoes[27][8] = 0
        self.producoes[28][1] = 30
        self.producoes[28][2] = 62
        self.producoes[28][3] = 63
        self.producoes[28][4] = 0
        self.producoes[28][5] = 0
        self.producoes[28][6] = 0
        self.producoes[28][7] = 0
        self.producoes[28][8] = 0
        self.producoes[29][1] = 42
        self.producoes[29][2] = 62
        self.producoes[29][3] = 63
        self.producoes[29][4] = 0
        self.producoes[29][5] = 0
        self.producoes[29][6] = 0
        self.producoes[29][7] = 0
        self.producoes[29][8] = 0
        self.producoes[30][1] = 44
        self.producoes[30][2] = 0
        self.producoes[30][3] = 0
        self.producoes[30][4] = 0
        self.producoes[30][5] = 0
        self.producoes[30][6] = 0
        self.producoes[30][7] = 0
        self.producoes[30][8] = 0
        self.producoes[31][1] = 64
        self.producoes[31][2] = 65
        self.producoes[31][3] = 0
        self.producoes[31][4] = 0
        self.producoes[31][5] = 0
        self.producoes[31][6] = 0
        self.producoes[31][7] = 0
        self.producoes[31][8] = 0
        self.producoes[32][1] = 37
        self.producoes[32][2] = 64
        self.producoes[32][3] = 65
        self.producoes[32][4] = 0
        self.producoes[32][5] = 0
        self.producoes[32][6] = 0
        self.producoes[32][7] = 0
        self.producoes[32][8] = 0
        self.producoes[33][1] = 34
        self.producoes[33][2] = 64
        self.producoes[33][3] = 65
        self.producoes[33][4] = 0
        self.producoes[33][5] = 0
        self.producoes[33][6] = 0
        self.producoes[33][7] = 0
        self.producoes[33][8] = 0
        self.producoes[34][1] = 44
        self.producoes[34][2] = 0
        self.producoes[34][3] = 0
        self.producoes[34][4] = 0
        self.producoes[34][5] = 0
        self.producoes[34][6] = 0
        self.producoes[34][7] = 0
        self.producoes[34][8] = 0
        self.producoes[35][1] = 39
        self.producoes[35][2] = 61
        self.producoes[35][3] = 38
        self.producoes[35][4] = 0
        self.producoes[35][5] = 0
        self.producoes[35][6] = 0
        self.producoes[35][7] = 0
        self.producoes[35][8] = 0
        self.producoes[36][1] = 16
        self.producoes[36][2] = 0
        self.producoes[36][3] = 0
        self.producoes[36][4] = 0
        self.producoes[36][5] = 0
        self.producoes[36][6] = 0
        self.producoes[36][7] = 0
        self.producoes[36][8] = 0
        self.producoes[37][1] = 12
        self.producoes[37][2] = 0
        self.producoes[37][3] = 0
        self.producoes[37][4] = 0
        self.producoes[37][5] = 0
        self.producoes[37][6] = 0
        self.producoes[37][7] = 0
        self.producoes[37][8] = 0
        self.producoes[38][1] = 11
        self.producoes[38][2] = 0
        self.producoes[38][3] = 0
        self.producoes[38][4] = 0
        self.producoes[38][5] = 0
        self.producoes[38][6] = 0
        self.producoes[38][7] = 0
        self.producoes[38][8] = 0
        self.producoes[39][1] = 13
        self.producoes[39][2] = 0
        self.producoes[39][3] = 0
        self.producoes[39][4] = 0
        self.producoes[39][5] = 0
        self.producoes[39][6] = 0
        self.producoes[39][7] = 0
        self.producoes[39][8] = 0
        self.producoes[40][1] = 23
        self.producoes[40][2] = 0
        self.producoes[40][3] = 0
        self.producoes[40][4] = 0
        self.producoes[40][5] = 0
        self.producoes[40][6] = 0
        self.producoes[40][7] = 0
        self.producoes[40][8] = 0
        self.producoes[41][1] = 15
        self.producoes[41][2] = 66
        self.producoes[41][3] = 4
        self.producoes[41][4] = 47
        self.producoes[41][5] = 67
        self.producoes[41][6] = 0
        self.producoes[41][7] = 0
        self.producoes[41][8] = 0
        self.producoes[42][1] = 61
        self.producoes[42][2] = 68
        self.producoes[42][3] = 61
        self.producoes[42][4] = 0
        self.producoes[42][5] = 0
        self.producoes[42][6] = 0
        self.producoes[42][7] = 0
        self.producoes[42][8] = 0
        self.producoes[43][1] = 26
        self.producoes[43][2] = 0
        self.producoes[43][3] = 0
        self.producoes[43][4] = 0
        self.producoes[43][5] = 0
        self.producoes[43][6] = 0
        self.producoes[43][7] = 0
        self.producoes[43][8] = 0
        self.producoes[44][1] = 27
        self.producoes[44][2] = 0
        self.producoes[44][3] = 0
        self.producoes[44][4] = 0
        self.producoes[44][5] = 0
        self.producoes[44][6] = 0
        self.producoes[44][7] = 0
        self.producoes[44][8] = 0
        self.producoes[45][1] = 29
        self.producoes[45][2] = 0
        self.producoes[45][3] = 0
        self.producoes[45][4] = 0
        self.producoes[45][5] = 0
        self.producoes[45][6] = 0
        self.producoes[45][7] = 0
        self.producoes[45][8] = 0
        self.producoes[46][1] = 25
        self.producoes[46][2] = 0
        self.producoes[46][3] = 0
        self.producoes[46][4] = 0
        self.producoes[46][5] = 0
        self.producoes[46][6] = 0
        self.producoes[46][7] = 0
        self.producoes[46][8] = 0
        self.producoes[47][1] = 28
        self.producoes[47][2] = 0
        self.producoes[47][3] = 0
        self.producoes[47][4] = 0
        self.producoes[47][5] = 0
        self.producoes[47][6] = 0
        self.producoes[47][7] = 0
        self.producoes[47][8] = 0
        self.producoes[48][1] = 24
        self.producoes[48][2] = 0
        self.producoes[48][3] = 0
        self.producoes[48][4] = 0
        self.producoes[48][5] = 0
        self.producoes[48][6] = 0
        self.producoes[48][7] = 0
        self.producoes[48][8] = 0
        self.producoes[49][1] = 19
        self.producoes[49][2] = 47
        self.producoes[49][3] = 0
        self.producoes[49][4] = 0
        self.producoes[49][5] = 0
        self.producoes[49][6] = 0
        self.producoes[49][7] = 0
        self.producoes[49][8] = 0
        self.producoes[50][1] = 44
        self.producoes[50][2] = 0
        self.producoes[50][3] = 0
        self.producoes[50][4] = 0
        self.producoes[50][5] = 0
        self.producoes[50][6] = 0
        self.producoes[50][7] = 0
        self.producoes[50][8] = 0
        self.producoes[51][1] = 16
        self.producoes[51][2] = 69
        self.producoes[51][3] = 0
        self.producoes[51][4] = 0
        self.producoes[51][5] = 0
        self.producoes[51][6] = 0
        self.producoes[51][7] = 0
        self.producoes[51][8] = 0
        self.producoes[52][1] = 17
        self.producoes[52][2] = 16
        self.producoes[52][3] = 32
        self.producoes[52][4] = 61
        self.producoes[52][5] = 3
        self.producoes[52][6] = 61
        self.producoes[52][7] = 20
        self.producoes[52][8] = 47
        self.producoes[53][1] = 70
        self.producoes[53][2] = 0
        self.producoes[53][3] = 0
        self.producoes[53][4] = 0
        self.producoes[53][5] = 0
        self.producoes[53][6] = 0
        self.producoes[53][7] = 0
        self.producoes[53][8] = 0
        self.producoes[54][1] = 61
        self.producoes[54][2] = 0
        self.producoes[54][3] = 0
        self.producoes[54][4] = 0
        self.producoes[54][5] = 0
        self.producoes[54][6] = 0
        self.producoes[54][7] = 0
        self.producoes[54][8] = 0
        self.producoes[55][1] = 39
        self.producoes[55][2] = 71
        self.producoes[55][3] = 72
        self.producoes[55][4] = 38
        self.producoes[55][5] = 0
        self.producoes[55][6] = 0
        self.producoes[55][7] = 0
        self.producoes[55][8] = 0
        self.producoes[56][1] = 44
        self.producoes[56][2] = 0
        self.producoes[56][3] = 0
        self.producoes[56][4] = 0
        self.producoes[56][5] = 0
        self.producoes[56][6] = 0
        self.producoes[56][7] = 0
        self.producoes[56][8] = 0
        self.producoes[57][1] = 16
        self.producoes[57][2] = 0
        self.producoes[57][3] = 0
        self.producoes[57][4] = 0
        self.producoes[57][5] = 0
        self.producoes[57][6] = 0
        self.producoes[57][7] = 0
        self.producoes[57][8] = 0
        self.producoes[58][1] = 12
        self.producoes[58][2] = 0
        self.producoes[58][3] = 0
        self.producoes[58][4] = 0
        self.producoes[58][5] = 0
        self.producoes[58][6] = 0
        self.producoes[58][7] = 0
        self.producoes[58][8] = 0
        self.producoes[59][1] = 11
        self.producoes[59][2] = 0
        self.producoes[59][3] = 0
        self.producoes[59][4] = 0
        self.producoes[59][5] = 0
        self.producoes[59][6] = 0
        self.producoes[59][7] = 0
        self.producoes[59][8] = 0
        self.producoes[60][1] = 23
        self.producoes[60][2] = 0
        self.producoes[60][3] = 0
        self.producoes[60][4] = 0
        self.producoes[60][5] = 0
        self.producoes[60][6] = 0
        self.producoes[60][7] = 0
        self.producoes[60][8] = 0
        self.producoes[61][1] = 36
        self.producoes[61][2] = 71
        self.producoes[61][3] = 72
        self.producoes[61][4] = 0
        self.producoes[61][5] = 0
        self.producoes[61][6] = 0
        self.producoes[61][7] = 0
        self.producoes[61][8] = 0
        self.producoes[62][1] = 44
        self.producoes[62][2] = 0
        self.producoes[62][3] = 0
        self.producoes[62][4] = 0
        self.producoes[62][5] = 0
        self.producoes[62][6] = 0
        self.producoes[62][7] = 0
        self.producoes[62][8] = 0
        self.producoes[63][1] = 1
        self.producoes[63][2] = 66
        self.producoes[63][3] = 20
        self.producoes[63][4] = 47
        self.producoes[63][5] = 0
        self.producoes[63][6] = 0
        self.producoes[63][7] = 0
        self.producoes[63][8] = 0
        self.producoes[64][1] = 7
        self.producoes[64][2] = 39
        self.producoes[64][3] = 16
        self.producoes[64][4] = 38
        self.producoes[64][5] = 0
        self.producoes[64][6] = 0
        self.producoes[64][7] = 0
        self.producoes[64][8] = 0
        self.producoes[65][1] = 13
        self.producoes[65][2] = 0
        self.producoes[65][3] = 0
        self.producoes[65][4] = 0
        self.producoes[65][5] = 0
        self.producoes[65][6] = 0
        self.producoes[65][7] = 0
        self.producoes[65][8] = 0
        

    def imprimirTabela(self):
        for i in range(73):
            for j in range(45):
                if self.tabParsing[i][j] != 0:
                    print(f"({i}, {j}): {self.tabParsing[i][j]}")

    def imprimirProducoes(self):
        for i in range(1, 66):
            for j in range(1, 7):
                if self.producoes[i][j] != 0:
                    print(f"({i}, {j}): {self.producoes[i][j]}")

tab_parsing = TabParsing()
tab_parsing.inicializarTab()
tab_parsing.inicializarProdu()


producoes = tab_parsing.producoes
tabParsing = tab_parsing.tabParsing


pilha = [43] #$ topo da pilha

pilha = np.hstack([producoes[1][:], pilha])

pilha = pilha[pilha != 0]

# print(f'pilha 1{pilha}')



X = pilha[0]
a = tokens[0]
l = lexemas[0]

while X != 43: #enquanto pilha nao estiver vazia
    print(X)
    print(a)
    print(pilha)
    if X == 44: #se o topo da pilha for vazio
        pilha = np.delete(pilha,[0])
        X = pilha[0]
    else:
        if X <= 44: #topo da pilha eh um terminal
            if X == a: #deu match :D
                pilha = np.delete(pilha,[0])
                tokens = np.delete(tokens,[0])
                lexemas = np.delete(lexemas,[0])
                X = pilha[0]
                if len(tokens) != 0:
                    a = tokens[0]
                    l = lexemas[0]
            else:
                print('Erro sintático')
                break
        else:
            # temp = [int(tabParsing[X][a])]

            topo = np.hstack([producoes[int(tabParsing[X][a])][:], pilha]) #empilha as producoes correspondentes
            
            topo = topo[topo!=0]

            if topo[0] == 44: # se topo vazio X recebe o novo topo da pilha
                X = topo[0] #
            else:

                if topo[0] != 0: # se topo nao vazio atualiza a pilha
                    pilha = np.delete(pilha,[0])
                    pilha = np.hstack([producoes[int(tabParsing[X][a])][:], pilha])
                    pilha = pilha[pilha != 0]
                    X = pilha[0]
                else:
                    print('Error')
                    break
#print('Pilha: ')                
#print(pilha)
#print('Entrada: ')
#print(tokens)
#print('Reconhecida com sucesso')


lexemas = [item[0] for item in collec]
tokens = [item[1] for item in collec]
linhas = [item[2] for item in collec]

pilha = [43] #$ topo da pilha
pilha = np.hstack([producoes[1][:], pilha])
pilha = pilha[pilha != 0]

#semantico
tabela_simbolos = []

X = pilha[0]
a = tokens[0]
l = lexemas[0]
linha = linhas[0]
nivel = 0
dentro_begin = False
dentro_procedure = False
primeiro_ident = False

try:
    while X != 43:
        if X == 44: #se o topo da pilha for vazio
            pilha = np.delete(pilha,[0])
            X = pilha[0]
        else:
            if X <= 44: #topo da pilha eh um terminal
                if X == a: #deu match :D
                    print(f'tabela de simbolos: {tabela_simbolos}')
                    # print(f'semantico x = {X} a = {a}')
                    inicio_var = 1
                    tipo = ''
                    # print(f'a = {a}')
                    if a == 2:
                        while tokens[inicio_var] == 16:
                            i = inicio_var
                            while (tokens[i] != 33):
                                # print(f'tokens[i] = {tokens[i]}')
                                simbolo = {"nome":lexemas[i],
                                        "tipo":'undef',
                                        "categ":'var',
                                        "nivel":nivel}
                                # print(simbolo)
                                if (simbolo['nome'] not in [s['nome'] for s in tabela_simbolos]):
                                    tabela_simbolos.append(simbolo)
                                else:
                                    for simb in tabela_simbolos:
                                        if simbolo['nome'] == simb['nome']:
                                            print(f'Erro Semântico (linha: {linhas[i]}): criar variável com o mesmo nome ({simbolo["nome"]}) de uma variável já declarada.')
                                            raise Exception
                                i+=1
                            if tokens[i] == 33:
                                tipo = lexemas[i+1]
                            # print(tipo)
                            i = inicio_var
                            while(tokens[i] != 33):
                                for simb in tabela_simbolos:
                                    if (simb['nome'] == lexemas[i]) and simb['nivel'] == nivel and simb['categ'] == 'var' and simb['tipo'] == 'undef':
                                        simb['tipo'] = tipo
                                    # print(f'simb= {simb}')
                                i+=1
                            # print(tabela_simbolos)
                            if tokens[i+2] == 31:
                                inicio_var = i+3

                    if a == 9:
                        simbolo = {
                            "nome":lexemas[1],
                            "tipo":'procedure',
                            "categ":'procedure',
                            "nivel":nivel
                        }
                        # print(simbolo)
                        if (simbolo['nome'] not in [s['nome'] for s in tabela_simbolos]):
                            tabela_simbolos.append(simbolo)
                            dentro_procedure = True
                            primeiro_ident = True
                            nivel+=1
                        else:
                            print(f'Erro Semântico (linha: {linhas[i]}): criar procedure com o  mesmo nome ({simbolo["nome"]}) de uma variável ou procedure já declarada.')
                            raise Exception
                        # print(tabela_simbolos)
                        
                    if a == 22:
                        dentro_begin = True
                        
                    if a == 16 and dentro_procedure:
                        if not primeiro_ident:
                            inicio_var=0
                            while tokens[inicio_var] == 16:
                                i = inicio_var
                                while (tokens[i] != 33):
                                    # print(f'tokens[i] = {tokens[i]}')
                                    simbolo = {"nome":lexemas[i],
                                            "tipo":'undef',
                                            "categ":'var',
                                            "nivel":nivel}
                                    # print(simbolo)
                                    if (simbolo['nome'] not in [s['nome'] for s in tabela_simbolos]):
                                        tabela_simbolos.append(simbolo)
                                    else:
                                        for simb in tabela_simbolos:
                                            if simbolo['nome'] == simb['nome']:
                                                print(f'Erro Semântico (linha: {linhas[i]}): criar variável com o mesmo nome ({simbolo["nome"]}) de uma variável já declarada.')
                                                raise Exception
                                    i+=1
                                if tokens[i] == 33:
                                    tipo = lexemas[i+1]
                                # print(tipo)
                                i = inicio_var
                                while(tokens[i] != 33):
                                    for simb in tabela_simbolos:
                                        if (simb['nome'] == lexemas[i]) and simb['nivel'] == nivel and simb['categ'] == 'var' and simb['tipo'] == 'undef':
                                            simb['tipo'] = tipo
                                        # print(f'simb= {simb}')
                                    i+=1
                                # print(tabela_simbolos)
                                if tokens[i+2] == 38:
                                    dentro_procedure = False
                                    inicio_var = 1
                        else:
                            primeiro_ident = False

                    if a == 16 and dentro_begin and not dentro_procedure:
                        existe = False
                        categ = ''
                        for s in tabela_simbolos:
                            if s['nome'] == lexemas[0]:
                                # print(lexemas[0])
                                categ = s['categ']
                                existe = True
                        if existe:
                            if tokens[1] == 39 and categ != 'procedure':
                                print(f'Erro Semãntico(linha: {linhas[i]}): procedure com este nome ({lexemas[0]}) não declarada.')
                                raise Exception
                        else:
                            print(f'Erro Semãntico(linha: {linhas[i]}): variável ou procedure com este nome ({lexemas[0]}) não declarada.')
                            raise Exception


                    pilha = np.delete(pilha,[0])
                    tokens = np.delete(tokens,[0])
                    lexemas = np.delete(lexemas,[0])
                    linhas = np.delete(linhas,[0])
                    X = pilha[0]
                    if len(tokens) != 0:
                        a = tokens[0]
                        l = lexemas[0]
                        linha = linhas[0]
                else:
                    print('Erro sintático')
                    break
            else:
                topo = np.hstack([producoes[int(tabParsing[X][a])][:], pilha]) #empilha as producoes correspondentes
                
                topo = topo[topo!=0]

                if topo[0] == 44: # se topo vazio X recebe o novo topo da pilha
                    X = topo[0] #
                else:

                    if topo[0] != 0: # se topo nao vazio atualiza a pilha
                        pilha = np.delete(pilha,[0])
                        pilha = np.hstack([producoes[int(tabParsing[X][a])][:], pilha])
                        pilha = pilha[pilha != 0]
                        X = pilha[0]
                    else:
                        print('Erro sintático')
                        break
except Exception:
    print('Compilação abortada.')
    exit(0)