import os
import pandas as pd
import openpyxl
import ast
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns


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

    
    idade=int(input("Informe sua idade: "))
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


      if isinstance(dado.get("percentual_de_saude_do_sono"), tuple):
            percentual, classificacao = dado["percentual_de_saude_do_sono"]
            dado["percentual_de_saude_do_sono"] = percentual
            dado["classificacao"] = classificacao

       
      if isinstance(dado.get("atividade_fisica"), list):
            atividades = dado["atividade_fisica"]
            dado["atividade_fisica"] = "; ".join([f"Dia {a['dia']}: {a['minutos']} min" for a in atividades])

      lista_registros.append(dado)

    df = pd.DataFrame(lista_registros)
    df.to_excel(caminho_excel, index=False)
    print(f"Dados salvos com sucesso em: {caminho_excel}")



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

def processar_atividade(atividade_str):
    try:
        atividade = ast.literal_eval(atividade_str)
        if isinstance(atividade, list):
            dias = len(atividade)
            media = sum([d['minutos'] for d in atividade]) / dias if dias > 0 else 0
            return dias, media
    except:
        pass
    return 0, 0

arquivo[['dias_atividade', 'media_minutos']] = arquivo['atividade_fisica'].apply(
    lambda x: pd.Series(processar_atividade(x))
)

arquivo = arquivo.drop(columns=['atividade_fisica'])

arquivo.head()

arquivo['classificacao'] = arquivo['classificacao'].replace('Boa',1)

arquivo['classificacao'] = arquivo['classificacao'].replace('Ruim',-1)

arquivo['classificacao'] = arquivo['classificacao'].replace('Regular',0)

arquivo

y = arquivo['classificacao']
x = arquivo.drop('classificacao',axis =1)

x 
#verifique a quantidade de informação
y.shape

from sklearn.model_selection import train_test_split

x_treino, x_teste, y_treino, y_teste =train_test_split(x,y, test_size =0.3)


y_teste.shape


from sklearn.ensemble import ExtraTreesClassifier #arma de decisão
modelo = ExtraTreesClassifier()
modelo.fit(x_treino, y_treino)


resultado = modelo.score(x_teste, y_teste) 
print("Acuarácia:",resultado)

x_teste

y_teste[10:13]

x_teste[10:13]

previsoes =modelo.predict(x_teste[10:13])

previsoes


cores = arquivo['classificacao'].map({1: 'green', 0: 'orange', -1: 'red'})

plt.figure(figsize=(10, 6))
plt.scatter(arquivo['idade'], arquivo['duracao_do_sono_em_horas'], c=cores)
plt.title('Duração do Sono por Idade (Cor por Classificação)')
plt.xlabel('Idade')
plt.ylabel('Duração do Sono (horas)')
plt.grid(True)
plt.tight_layout()
plt.show()


arquivo['IMC'] = arquivo['peso'] / (arquivo['altura'] ** 2)
dados_ordenados = arquivo.sort_values(by='IMC')
plt.figure(figsize=(10, 6))
plt.plot(dados_ordenados['IMC'], dados_ordenados['duracao_do_sono_em_horas'], marker='o', linestyle='-')
plt.title('Duração do Sono em Função do IMC')
plt.xlabel('IMC')
plt.ylabel('Duração do Sono (horas)')
plt.grid(True)
plt.tight_layout()
plt.show()

media_sono_idade = arquivo.groupby('idade')['duracao_do_sono_em_horas'].mean()

plt.figure(figsize=(10, 6))
media_sono_idade.plot(kind='bar', color='skyblue')
plt.title('Média da Duração do Sono por Idade')
plt.xlabel('Idade')
plt.ylabel('Duração Média do Sono (horas)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

sns.set(style="whitegrid")


plt.figure(figsize=(12, 5))
sns.countplot(data=arquivo, x='idade', hue='classificacao', palette='Set2')
plt.title('Qualidade do Sono por Idade')
plt.xlabel('Idade')
plt.ylabel('Quantidade de Pessoas')
plt.legend(title='Classificação')
plt.show()
