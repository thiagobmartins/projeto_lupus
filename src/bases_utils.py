"""
Funções utilizadas na análise dos pacientes com cirurgia
e também para verificação da base do francisco 
"""
import pandas as pd
from  src import procedimentos

def pesquisa_paciente(id_paciente, df_lupus_cirurgia_idx, df_cirurgia):
    if id_paciente not in df_lupus_cirurgia_idx.index:
        print(' - Paciente não operou')
        return  {id_paciente:{}}

    df_paciente = df_lupus_cirurgia_idx.loc[id_paciente]
    if isinstance(df_paciente, pd.DataFrame):
        opt = set(df_paciente['co_procedimento_principal'])
    else:
        #ipdb.set_trace()
        df_res = df_paciente.to_frame().T
        return df_res[['data', 'sexo', 'idade','uf_paciente']]
        #ipdb.set_trace()
        #opt = set([df_paciente['co_procedimento_principal']]) # Quando o df vira uma série, a coluna vira int
        #return {id_paciente:{'eita':'eita'}}
        
    id_cirurgias_abs = opt.intersection(set(df_cirurgia['cod_procedimento']))
    

    # Pega o primeiro registro com código de procedimento relacionado às cirugias especificadas
    res = df_paciente[df_paciente['co_procedimento_principal'].isin(id_cirurgias_abs)] \
                    [['data', 'sexo', 'idade','uf_paciente']].sort_values('data')
    return res

def get_info_paciente(id_paciente, df_lupus_cirurgia_idx, df_cirurgia):
    df_paciente = pesquisa_paciente(id_paciente, df_lupus_cirurgia_idx, df_cirurgia)
    #print(df_paciente)
    if len(df_paciente) > 0:
        return {id_paciente: df_paciente.iloc[0].to_dict()}
    else:
        print(df_paciente)
        return {id_paciente:{}}
    
def junta_dfs_e_procedimentos(bpai, aih, apac):
    """
    Junta os dfs de bpai, aih e apac para fazer
    a análise de sexo, idade e região
    """
    
    bpai.rename(columns={'co_procedimento_realizado':'co_procedimento_principal',
                        'no_procedimento_realizado':'no_procedimento_principal'},
                        inplace=True)    
    bpai['co_procedimento_secundario'] = 1111
    bpai['no_procedimento_secundario'] = 'BPAI'
    bpai['co_cid_secundario'] = 'BPAI'
    
    aih.rename(columns={'desc_procedimento_secundario':'no_procedimento_secundario',
                        'procedimento_principal':'no_procedimento_principal'},
                        inplace=True)
    
    aih['co_procedimento_secundario'] = 9999
    
   
    cols = ['id_paciente', 'co_cid_principal', 'co_cid_secundario',
            'co_procedimento_principal', 'no_procedimento_principal',
            'co_procedimento_secundario', 'no_procedimento_secundario']
    
    all = pd.concat([bpai[cols], aih[cols], apac[cols]])

    return all 

def get_regiao(sigla: str):
    """
    Retorna a região brasileira dado a sigla do estado.
    
    Args:
        sigla (str): Sigla do estado brasileiro (ex: 'SP', 'RJ', 'AM').
    
    Returns:
        str: Região brasileira (Norte, Nordeste, Sudeste, Sul, Centro-Oeste).
    """
    
    regioes = {
        # Norte
        'AC': 'Norte', 'AM': 'Norte', 'AP': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
        
        # Nordeste
        'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
        
        # Sudeste
        'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
        
        # Sul
        'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul',
        
        # Centro-Oeste
        'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MS': 'Centro-Oeste', 'MT': 'Centro-Oeste'
    }
    
    return regioes.get(sigla.upper(), "Sigla inválida")

def get_categoria_idade(idade: int) -> str:
    """
    Retorna a categoria de idade dado um valor inteiro.

    Args:
        idade (int): Idade em anos.

    Returns:
        str: Categoria de idade.
    """
    if idade < 16:
        return "Idade inválida"
    elif idade <= 20:
        return "16-20"
    elif idade <= 25:
        return "21-25"
    elif idade <= 30:
        return "26-30"
    elif idade <= 35:
        return "31-35"
    elif idade <= 40:
        return "36-40"
    elif idade <= 45:
        return "41-45"
    elif idade <= 50:
        return "46-50"
    elif idade <= 55:
        return "51-55"
    else:
        return "55+"

def junta_dfs(bpai, aih, apac):
    """
    Junta os dfs de bpai, aih e apac para fazer
    a análise de sexo, idade e região
    """
    aih.rename(columns={'co_paciente_sexo':'sexo'}, inplace=True)
    aih.rename(columns={'vl_paciente_idade':'idade'}, inplace=True)
    aih.rename(columns={'sg_uf':'uf_paciente'}, inplace=True)
    apac.rename(columns={'uf_endereco':'uf_paciente'}, inplace=True)
    bpai.rename(columns={'co_procedimento_realizado':'co_procedimento_principal'}, inplace=True) 

    cols = ['id_paciente', 'sexo', 'idade', 'uf_paciente', 'data', 'co_procedimento_principal']
    all = pd.concat([bpai[cols], aih[cols], apac[cols]])

    all['sexo'] = all['sexo'].replace('F','FEMININO')
    all['sexo'] = all['sexo'].replace('M','MASCULINO')

    all['regiao'] = all['uf_paciente'].map(get_regiao)
    all['idade_categoria'] = all['idade'].map(get_categoria_idade)

    return all

def verifica_procedimentos_paciente(df_paciente: pd.DataFrame, cols_procedimentos):
    """ Recebe um df com os procedimentos de apenas um paciente
    e verifica quais procedimentos foram aprovados em quais etapas do algoritmo. 
    Assume que as cols_procedimentos são apenas duas: procedimento principal e secundário.
    """
    if df_paciente['id_paciente'].nunique() > 1:
        raise Exception(' - Mais de um paciente')
    
    id_paciente = int(df_paciente['id_paciente'].iloc[0]) # Pega o id do paciente
    
    dict_pacientes = {}
    proc_dict = {'p1':procedimentos.p1, 'p2':procedimentos.p2, 'p3':procedimentos.p3, 'p4':procedimentos.p4}
    
    for proc_name in proc_dict.keys():
        dict_pacientes[proc_name] = set()
    dict_pacientes['cid'] = set()

    for proc, proc_func in proc_dict.items():
        if proc_func(df_paciente, cols_procedimentos[0]) or \
            proc_func(df_paciente, cols_procedimentos[1]): # Aplica todos os procedimentos em cada coluna de procedimento
                dict_pacientes[proc].add(id_paciente) # Salva o id do paciente no conjunto do procedimento em que ele passou

    # Verifica os cids:
    if (df_paciente['cid_principal'].sum() > 0) or \
        (df_paciente['cid_secundario'].sum() > 0):
            dict_pacientes['cid'].add(id_paciente)


    for proced in ['p1', 'p2', 'p3', 'p4', 'cid']: # Adiciona uma coluna como True para cada procedimento em que o paciente foi aprovado
        df_paciente[f'procedimento_{proced}'] = df_paciente['id_paciente'].isin(dict_pacientes[proced])
    
    return df_paciente