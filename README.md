O código foi feito no Jupyter notebook

#é necessario a instalação

import os<br/>
import pandas as pd <br/>
import openpyxl<br/>
import ast<br/>
import matplotlib.pyplot as plt<br/>
%matplotlib inline<br/>
import seaborn as sns


#utilizar o caminho a ser utilizado do seu computador 

arquivo=pd.read_excel(r'C:\Users\Windows\Documents\estudo larissa\Criando projeto\Relação entre saude e sono\Relacao_saude_sono_v1.xlsx')

#verifica a quantidade de informações\
y.shape

#verifica a quantidade de informações que vai ser testado\
y_teste.shape

#O algoritmo vai rodar em cima dos dados de treino<br/>
from sklearn.ensemble import ExtraTreesClassifier #arma de decisão<br/>
#criação do modelo:<br/>
modelo = ExtraTreesClassifier()#algoritmo de classificação

#vai aplicar nos dados\
modelo.fit(x_treino, y_treino)


resultado = modelo.score(x_teste, y_teste) #o y tem os dados real o x ele verificar conforme os dados do y<br/>
#a função score vai pegar a coluna de dados de teste vai comparar x_teste com o y_teste,que a classificação real<br/>
#vai usar a coluna de teste vai passar pelo algoritmo e o algoritmo como ele ja aprendeu, ele vai<br/>
#tentar prever qual é a classe e verificar e esta certo ou não
print("Acuarácia:",resultado)


#ele vai pegar dentro do numero que sera testado aleatoriamente 3 informações \
e vai colocar -1,0 ou 1 para as classificação
y_teste[10:13]

#por exemplo:<br/>
#26 -1<br/>
#45  0<br/>
#15  0

A previsão vai verificar se a classificação foi correta com as informações acima\
previsoes =modelo.predict(x_teste[10:13])

#esta chamando
previsoes

#o resultado nesse caso

#array([-1,0,0])\
#deu certo, porque bate com as informações acima

1)Grafico<br/>
cores = arquivo['classificacao'].map({1: 'green', 0: 'orange', -1: 'red'})<br/>

plt.figure(figsize=(10, 6))<br/>
plt.scatter(arquivo['idade'], arquivo['duracao_do_sono_em_horas'], c=cores)<br/>
plt.title('Duração do Sono por Idade (Cor por Classificação)')<br/>
plt.xlabel('Idade')
plt.ylabel('Duração do Sono (horas)')<br/>
plt.grid(True)<br/>
plt.tight_layout()
plt.show()

2)grafico<br/>
Calcular o IMC
arquivo['IMC'] = arquivo['peso'] / (arquivo['altura'] ** 2)

Ordenar por IMC para o gráfico ficar mais claro
dados_ordenados = arquivo.sort_values(by='IMC')<br/>

plt.figure(figsize=(10, 6))<br/>
plt.plot(dados_ordenados['IMC'], dados_ordenados['duracao_do_sono_em_horas'], marker='o', linestyle='-')<br/>
plt.title('Duração do Sono em Função do IMC')<br/>
plt.xlabel('IMC')<br/>
plt.ylabel('Duração do Sono (horas)')<br/>
plt.grid(True)
plt.tight_layout()
plt.show()

3)grafico<br/>
media_sono_idade = arquivo.groupby('idade')['duracao_do_sono_em_horas'].mean()<br/>

plt.figure(figsize=(10, 6))<br>
media_sono_idade.plot(kind='bar', color='skyblue')<br/>
plt.title('Média da Duração do Sono por Idade')<br/>
plt.xlabel('Idade')<br/>
plt.ylabel('Duração Média do Sono (horas)')<br/>
plt.grid(axis='y')
plt.tight_layout()
plt.show()

4)grafico\
sns.set(style="whitegrid")<br/>

Qualidade do sono por idade (contagem)<br/>
plt.figure(figsize=(12, 5))<br/>
sns.countplot(data=arquivo, x='idade', hue='classificacao', palette='Set2')<br/>
plt.title('Qualidade do Sono por Idade')<br/>
plt.xlabel('Idade')
plt.ylabel('Quantidade de Pessoas')
plt.legend(title='Classificação')<br/>
plt.show()<br/>

