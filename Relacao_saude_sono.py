import os
import pandas as pd
import openpyxl


def calcular_percentual_sono(peso, altura, duracao_sono, lista_atividade,nivel_de_estresse):
    imc = peso / (altura ** 2)
    imc_ok = 18.5 <= imc <= 24.9
    sono_ok = 7 <= duracao_sono <= 9
    vezes_semana = len(lista_atividade)
    minutos_por_dia = [dia["minutos"] for dia in lista_atividade]
    media_minutos = sum(minutos_por_dia) / vezes_semana if vezes_semana > 0 else 0
    atividade_ok = vezes_semana >= 3 and media_minutos >= 30
    estresse_ok = nivel_de_estresse <=60

    pontos = sum([imc_ok, sono_ok, atividade_ok, estresse_ok])
    percentual= (pontos / 4) * 100


    if percentual < 40:
      classificacao ="Ruim"
    elif percentual <70:
      classificacao ="Regular"
    else:
      classificacao ="Boa"


    return round(percentual, 2), classificacao

def cadastro(dados,proximo_id):

  qtd= int(input("Quantas pessoas você deseja cadastrar? "))

  for i in range(qtd):

    #nome=input("Informe seu nome: ")
    idade=int(input("Informe sua idade: "))
    #genero=str(input("Informe seu genero: "))
    altura=float(input("Informe sua altura: "))
    peso=float(input("Informe seu peso: "))

    duracao_do_sono=float(input(f"Informe a quantidade de duração do seu sono em horas:  "))
    nivel_de_estresse=int(input("Informe o nivel de estresse na escala de 0 a 100: "))

    lista_atividade_fisica=[]
    qtd_atividade=(input("Quantos registros de atividade física deseja inserir? "))
    for i in range(int(qtd_atividade)):
        dia = int(input("Dia da semana (1-7): "))
        minutos = int(input("Minutos de exercício nesse dia: "))
        lista_atividade_fisica.append({"dia": dia, "minutos": minutos})


    percentual, classificacao=calcular_percentual_sono(peso, altura, duracao_do_sono, lista_atividade_fisica, nivel_de_estresse)

    dados[str(proximo_id)]={
                  "id": proximo_id,
                  "idade": idade,
                  "altura": altura,
                  "peso": peso,
                  "duracao_do_sono_em_horas": duracao_do_sono,
                  "nivel_de_estrese_0_a_100": nivel_de_estresse,
                  "atividade_fisica": lista_atividade_fisica,
                  "percentual_de_saude_do_sono": percentual,
                  "classificacao": classificacao


              }
    print(f"Percentual de saúde do sono para : {percentual}%")

    proximo_id +=1
  return proximo_id, dados #<--RETORNANDO contadores



def verificar_dados(dados):
  print("\n Todos os  dados cadastrados: \n ")
  for id_, info in dados.items():
    print(f"\n--- ID: {id_} ---")
    for chave, valor in info.items():
      print(f"{chave}: {valor}")



def salvar_dados_em_txt(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as f:
        for id_, info in dados.items():
            f.write(f"{id_}\n")
            for chave, valor in info.items():
                f.write(f"{chave}:{valor}\n")
            f.write("---\n")



def ler_arquivo(caminho):
    dados = {}
    if not os.path.exists(caminho):
        return dados

    with open(caminho, "r", encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    i = 0
    while i < len(linhas):
        proximo_id = linhas[i].strip()
        i += 1
        info = {}
        while i < len(linhas) and linhas[i].strip() != "---":
            linha = linhas[i].strip()
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                valor = valor.strip()
                if valor.replace('.', '', 1).isdigit():
                    valor = float(valor) if '.' in valor else int(valor)
                info[chave] = valor
            i += 1
        i += 1  # pular o separador "---"
        dados[proximo_id] = info
    return dados


def salvar_dados_em_excel(caminho_excel, dados):
    lista_registros=[]

    for registro in dados.values():
      dado =registro.copy()

 # Se o percentual vem como tupla (ex: (85.0, 'Boa')), separa em dois campos
      if isinstance(dado.get("percentual_de_saude_do_sono"), tuple):
            percentual, classificacao = dado["percentual_de_saude_do_sono"]
            dado["percentual_de_saude_do_sono"] = percentual
            dado["classificacao"] = classificacao

        # Converte lista de atividades físicas para string
      if isinstance(dado.get("atividade_fisica"), list):
            atividades = dado["atividade_fisica"]
            dado["atividade_fisica"] = "; ".join([f"Dia {a['dia']}: {a['minutos']} min" for a in atividades])

      lista_registros.append(dado)

    df = pd.DataFrame(lista_registros)
    df.to_excel(caminho_excel, index=False)
    print(f"Dados salvos com sucesso em: {caminho_excel}")



# Variáveis do caminho dos arquivos
CAMINHO_TXT = "Relacao_saude_sono.txt"
CAMINHO_EXCEL = "Relacao_saude_sono.xlsx"

def rodar_cadastro():
    dados = ler_arquivo(CAMINHO_TXT)
    proximo_id = max([int(k) for k in dados.keys()], default=0) + 1
    proximo_id, dados = cadastro(dados, proximo_id)
    salvar_dados_em_txt(CAMINHO_TXT, dados)
    salvar_dados_em_excel(CAMINHO_EXCEL, dados)
    print("Cadastro concluído.")

def mostrar_dados():
    dados = ler_arquivo(CAMINHO_TXT)
    verificar_dados(dados)


rodar_cadastro()
mostrar_dados()


arquivo=pd.read_excel(r'C:\Users\Windows\Documents\estudo larissa\Criando projeto\Relação entre saude e sono\Relacao_saude_sono.xlsx')

arquivo.head()

arquivo['classificacao'] = arquivo['classificacao'].replace('Boa',1)

arquivo['classificacao'] = arquivo['classificacao'].replace('Ruim',-1)

arquivo['classificacao'] = arquivo['classificacao'].replace('Regular',0)

y = arquivo['classificacao']
x = arquivo.drop('classificacao',axis =1)

x = pd.get_dummies(x)

from sklearn.model_selection import train_test_split

x_treino, x_teste, y_treino, y_teste =train_test_split(x,y, test_size =0.3)


#vai rodar o algoritmo vai rodar em cima dos dados de treino
from sklearn.ensemble import ExtraTreesClassifier #arma de decisão
#criação do modelo:
modelo = ExtraTreesClassifier()#algoritmo de classificação
#vai aplicar nos dados
modelo.fit(x_treino, y_treino)


resultado = modelo.score(x_teste, y_teste) #o y tem os dados real o x ele verificar conforme os dados do y
#a função score vai pegar a coluna de dados de teste vai comparar x_teste com o y_teste,que a classificação real
#vai usar a coluna de teste vai passar pelo algoritmo e o algoritmo como ele ja aprendeu, ele vai
#tentar prever qual é a classe e verificar e esta certo ou não
print("Acuarácia:",resultado)

x_teste

y_teste[10:13]

x_teste[10:13]

previsoes =modelo.predict(x_teste[10:13])

previsoes
    

