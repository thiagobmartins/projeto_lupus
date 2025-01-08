# pac_aih.sample().T
columns_aih = ['id_paciente', 'co_cid_principal', 'no_cid_principal',
               'co_procedimento_principal',
               'co_cid_secundario', 'no_cid_secundario',
               'procedimento_principal', 'desc_procedimento_secundario']

columns_apac = ['id_paciente', 'co_cid_principal', 'no_cid_principal',
                'co_cid_secundario', 'co_procedimento_principal',
                'no_procedimento_principal', 'co_procedimento_secundario',
                'no_procedimento_secundario']

columns_bpai = ['id_paciente', 'co_cid_principal', 'no_cid_principal',
                'co_procedimento_realizado', 'no_procedimento_realizado', ]


import pandas as pd

# Lê os arquivos dos datasets
path = 'data/HD/'
pac_apac = pd.read_parquet(path+'APAC_Lupus_L93M32N08_todos_cids.parquet', columns=columns_apac)
pac_aih = pd.read_parquet(path+'AIH_Lupus_L93M32N08_todos_cids.parquet', columns=columns_aih)
pac_bpai = pd.read_parquet(path+'BPAI_Lupus_L93M32N08_todos_cids.parquet', columns=columns_bpai)

# Pequena análise
print(f' - APAC: Registros: {pac_apac.shape[0]} Pacientes únicos: {pac_apac['id_paciente'].nunique()}')
print(f' - AIH: Registros: {pac_aih.shape[0]} Pacientes únicos: {pac_aih['id_paciente'].nunique()}')
print(f' - BPAI: Registros: {pac_bpai.shape[0]} Pacientes únicos: {pac_bpai['id_paciente'].nunique()}')
print(f' - Total: Registros: {pac_bpai.shape[0]+pac_aih.shape[0]+pac_apac.shape[0]} \
      Pacientes únicos: {pac_bpai['id_paciente'].nunique() + \
                         pac_aih['id_paciente'].nunique() + \
                         pac_apac['id_paciente'].nunique()}')


# Conjunto dos pacientes únicos em cada dataset
set_bpai = set(pac_bpai['id_paciente'])
set_apac = set(pac_apac['id_paciente'])
set_aih = set(pac_aih['id_paciente'])


from tqdm import tqdm

# Verifica os cids (M32, L932 e N08) de cada um dos datasets (AIH, BPAI, APAC)
def verifica_cid(row):
    for cod in ['M32', 'L93', 'N08']:
        if (cod in row):
            return True    
    return False

for df in tqdm([pac_aih, pac_bpai, pac_apac]):
    df['filtro_cid_principal'] = df['co_cid_principal'].apply(verifica_cid)
    if 'co_cid_secundario' in df.columns:
        df['filtro_cid_secundario'] = df['co_cid_secundario'].apply(verifica_cid)



# Classificando os pacientes

## Função
import importlib
from  src import procedimentos
importlib.reload(procedimentos)

def verifica_procedimentos(df_pacientes, col_procedimento):
    df_pacientes = df_pacientes.copy()
    pacientes_list = list(df_pacientes.id_paciente.unique())
    dict_pacientes = {}
    proc_dict = {'p1':procedimentos.p1, 'p2':procedimentos.p2,
                 'p3':procedimentos.p3, 'p4':procedimentos.p4}
    
    for proc_name in proc_dict.keys():
        dict_pacientes[proc_name] = set()

    for id_paciente in tqdm(pacientes_list, desc=f'Classificando Pacientes'):
        id_paciente = int(id_paciente)
        # Pega apenas os procedimentos no paciente em questão
        df_paciente = df_pacientes[df_pacientes.id_paciente==id_paciente].copy()

        # Se o paciente passou no filtro dos cids, agora aplica o filtro dos procedimentos
        for proc, proc_func in proc_dict.items():
            if proc_func(df_paciente, col_procedimento): # Aplica todos os procedimentos em cada cliente
                # Salva o id do paciente no conjunto do procedimento em que ele passou
                dict_pacientes[proc].add(id_paciente)

    # Adiciona uma coluna como True para cada procedimento em que o paciente foi aprovado
    for proced in ['p1', 'p2', 'p3', 'p4']:
        df_pacientes[f'procedimento_{proced}'] = df_pacientes['id_paciente'].isin(dict_pacientes[proced])
    
    return df_pacientes

## Aplicando a função
df_apac = verifica_procedimentos(pac_apac, col_procedimento='no_procedimento_principal')
df_aih = verifica_procedimentos(pac_aih, col_procedimento='desc_procedimento_secundario')
df_bpai = verifica_procedimentos(pac_bpai, col_procedimento='no_procedimento_realizado')


# Aplicando os algoritmos
# Juntando as bases (por enquanto BPAI, APAC e AIH)
cols_union = ['id_paciente', 'procedimento_p1', 'procedimento_p2',
              'procedimento_p3', 'procedimento_p4', 'filtro_cid_principal']
df_union = pd.concat([df_bpai[cols_union],
                      df_apac[cols_union+['filtro_cid_secundario']],
                      df_aih[cols_union+['filtro_cid_secundario']]])
df_union.fillna(False, inplace=True)



# Aplicando filtros antes para diminuir o número de registros
# df_cid contém apenas os registros que passaram no filtro de cids
df_cid = df_union[df_union['filtro_cid_principal'] | df_union['filtro_cid_secundario']].copy()

