O código foi feito no Jupyter notebook

é necessario a instalação
import os
import pandas as pd
import openpyxl
import ast
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns


utilizar o caminho a ser utilizado do seu computador 
arquivo=pd.read_excel(r'C:\Users\Windows\Documents\estudo larissa\Criando projeto\Relação entre saude e sono\Relacao_saude_sono_v1.xlsx')

#verifica a quantidade de informações
y.shape

#verifica a quantidade de informações que vai ser testado
y_teste.shape

# O algoritmo vai rodar em cima dos dados de treino
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


#ele vai pegar dentro do numero que sera testado aleatoriamente 3 informações 
# e vai colocar -1,0 ou 1 para as classificação
y_teste[10:13]

#por exemplo dentro das informações que serão testado tirou 3 informações aleatoriamente
#26 -1
#45  0
#15  0

# A previsão vai verificar se a classificação foi correta com as informações acima
previsoes =modelo.predict(x_teste[10:13])

#esta chamando
previsoes

#o resultado nesse caso

#array([-1,0,0])
#deu certo, porque bate com as informações acima

1) grafico
cores = arquivo['classificacao'].map({1: 'green', 0: 'orange', -1: 'red'})

plt.figure(figsize=(10, 6))
plt.scatter(arquivo['idade'], arquivo['duracao_do_sono_em_horas'], c=cores)
plt.title('Duração do Sono por Idade (Cor por Classificação)')
plt.xlabel('Idade')
plt.ylabel('Duração do Sono (horas)')
plt.grid(True)
plt.tight_layout()
plt.show()

2)grafico
# Calcular o IMC
arquivo['IMC'] = arquivo['peso'] / (arquivo['altura'] ** 2)

# Ordenar por IMC para o gráfico ficar mais claro
dados_ordenados = arquivo.sort_values(by='IMC')

plt.figure(figsize=(10, 6))
plt.plot(dados_ordenados['IMC'], dados_ordenados['duracao_do_sono_em_horas'], marker='o', linestyle='-')
plt.title('Duração do Sono em Função do IMC')
plt.xlabel('IMC')
plt.ylabel('Duração do Sono (horas)')
plt.grid(True)
plt.tight_layout()
plt.show()

3)grafico
media_sono_idade = arquivo.groupby('idade')['duracao_do_sono_em_horas'].mean()

plt.figure(figsize=(10, 6))
media_sono_idade.plot(kind='bar', color='skyblue')
plt.title('Média da Duração do Sono por Idade')
plt.xlabel('Idade')
plt.ylabel('Duração Média do Sono (horas)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

4)grafico
sns.set(style="whitegrid")

# 1. Qualidade do sono por idade (contagem)
plt.figure(figsize=(12, 5))
sns.countplot(data=arquivo, x='idade', hue='classificacao', palette='Set2')
plt.title('Qualidade do Sono por Idade')
plt.xlabel('Idade')
plt.ylabel('Quantidade de Pessoas')
plt.legend(title='Classificação')
plt.show()

