#pip install pdfplumber
#pip install pandas

#%%

import os
import pandas as pd
import pdfplumber
from tqdm import tqdm

#%%

# Função para extrair a linha que começa com a palavra-chave
def extrair_linha(texto, palavras_chave):
    linhas = texto.split("\n")  # Divide o texto em linhas
    for linha in linhas:
        for palavra in palavras_chave:  # Verifica cada palavra-chave
            if linha.startswith(palavra):  # Se a linha começa com a palavra-chave
                return linha  # Retorna a linha
    return None  # Retorna None se nenhuma linha for encontrada

#%%

# Carregar as palavras-chave
palavras_chave = pd.read_csv("valores_unicos_provas.csv")['Provas'].tolist()

# Criar DataFrame final
final = pd.DataFrame(columns= ['Pos', 'Raia', 'Série', 'Atleta', 'Classe', 'Dt Nascimento', 'Clube', 'UF', 'Marca', 'Vento', 'R', 'ITC', 'JSTF', 'distancia', 'sexo', 'classe', 'idade'])

errors = 0

# Carregar PDFs
pdfs = os.listdir()
pdfs = [pdf for pdf in pdfs if pdf.endswith(".pdf")]

#%%

# Processar cada PDF
for file in pdfs:
    print('Analyzing', file)
    with pdfplumber.open(file) as pdf:
        err_page = 0
        total = len(pdf.pages)
        
        for i in tqdm(range(1, len(pdf.pages))):
        #for i in tqdm(range(9, 13)):
            try:
                # Selecionar a página
                page = pdf.pages[i]
                texto = page.extract_text()
                
                # Extrair a linha que começa com uma palavra-chave
                linha_extraida = extrair_linha(texto, palavras_chave)
                
                if linha_extraida:
                    categoria = linha_extraida.split(" - ")
                    
                    # Extrair as tabelas da página
                    tables = page.extract_tables()
                    if len(tables) > 0:  # Verifica se há tabelas
                        tabela = tables[len(tables) - 1]
                        
                        # Verifica se a tabela tem o número mínimo de linhas
                        if len(tabela) > 1:  # Se a tabela tiver pelo menos uma linha de dados
                            df = pd.DataFrame(tabela[1:], columns=tabela[0])
                            max_len = max(len(col) for col in df.columns)
                            if max_len < 30:
                                df["distancia"] = categoria[0]
                                df["sexo"] = categoria[1]
                                df["classe"] = categoria[2]
                                df["idade"] = categoria[3]
                                #df["data_oficial"] = categoria[4]
                                
                                # Acumular os dados
                                if "" in list(df.columns):
                                    del df['']
                                    
                                #print(df.columns)
                                #print("debug")
                                df = df.reset_index(drop=True)
                                final = final.reset_index(drop=True)
                                final = pd.concat([final, df], ignore_index=True)
                            else:
                                print(f"\n Erro decoficando tabela na página {i} do arquivo {file}")
                                errors += 1
                                err_page += 1
                        else:
                            print(f"\n Tabela vazia ou sem dados suficientes na página {i} do arquivo {file}")
                    else:
                        print(f"\n Nenhuma tabela encontrada na página {i} do arquivo {file}")
                else:
                    print(f"\n Não encontrou a linha com as palavras-chave na página {i} do arquivo {file}")
                    
            except Exception as e:
                print(f'ERROR | File: {file} | Page: {i} | Error: {e}')
                errors += 1
                err_page += 1
        
        print('Success rate = ', (1 - (err_page / total)) * 100, "%")

print('Done')
print(f'Pages with error: {errors}')



#%%

final['Dt Nascimento'] = final['Dt Nascimento'].fillna('')+final['Dt. Nasc'].fillna('')
del final['Dt. Nasc']
del final['Dt Nasc']
print(final.columns)

#%%
final.to_csv('final.csv')
final.info()
