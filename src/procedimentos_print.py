"""
Neste arquivo estão as principais funções utilizadas
pelos algoritmos 1 e 2 para a classificação dos pacientes.

Estas funções correspondem aos procedimentos 1, 2, 3 e 4
listados na descrição dos algoritmos.
"""

import unidecode

def filtro_p1(row):
    """
    Verifica se a linha recebida por parâmetro está no
    conjunto de procedimentos listados no procedimento 1.
    """
    row = unidecode.unidecode(row).upper() # remove acentos e deixa tudo em maiúsculo

    if row in ['HEMOGRAMA COMPLETO', 'CONTAGEM DE RETICULOCITOS',
                'TESTE DE HAM (HEMOLISE ACIDA)', 'ANEMIA HEMOLITICA',
                'PROVA DE COMPATIBILIDADE PRE-TRANSFUSIONAL (MEIOS SALINOS, ALBUMINOSO E COOMBS)']:
        return True
    else:
        return False
    
def p1(df_procedimentos, col_procedimento):
    """
    Para satisfazer os critérios do procedimento 1, o paciente
    precisa ter os 3 procedimentos listados no procedimento 1.
    """
    if df_procedimentos.id_paciente.nunique() > 1:
        raise Exception(' - Mais de um paciente no df_procedimentos')
    
    # Conjunto com os procedimentos relacionado ao COOMBS
    coombs_set = set(['TESTE DE HAM (HEMOLISE ACIDA)', 'ANEMIA HEMOLITICA',
                    'PROVA DE COMPATIBILIDADE PRE-TRANSFUSIONAL (MEIOS SALINOS, ALBUMINOSO E COOMBS)'])
    # Após garantir que existe apenas um paciente no df_procedimentos
    procedimentos_list = df_procedimentos[col_procedimento].unique()    
    if 'HEMOGRAMA COMPLETO' in procedimentos_list:
        if 'CONTAGEM DE RETICULOCITOS' in procedimentos_list:
            if set(procedimentos_list) & set(coombs_set)
                return True
            
    # Se não caiu em nenhuma das condições
    return False
        

def filtro_p2(row):
    """
    Verifica se a linha recebida por parâmetro está no
    conjunto de procedimentos listados no procedimento 2.
    """
    row = unidecode.unidecode(row).upper() # remove acentos e deixa tudo em maiúsculo

    if row in ['DOSAGEM DE UREIA', 'CLEARANCE DE UREIA',
                'DOSAGEM DE CREATININA', 'DOSAGEM DE CREATININA NO LIQUIDO AMNIOTICO', 'CLEARANCE DE CREATININA',
                'ANALISE DE CARACTERES FISICOS, ELEMENTOS E SEDIMENTO DA URINA',
                'PESQUISA DE ANTICORPOS ANTI-DNA',
                'DOSAGEM DE PROTEINAS (URINA DE 24 HORAS)'
                ]:
        return True
    else:
        return False
    
def p2(df_paciente, col_procedimento):
    """
    Verifica se o paciente satisfaz as condições do procedimento 2.
    """
    if df_paciente.id_paciente.nunique() > 1:
        raise Exception(' - Mais de um paciente no df_paciente')
    
    # Após garantir que existe apenas um paciente no df_paciente
    procedimentos_do_paciente = df_paciente[col_procedimento].unique()

    if 'PESQUISA DE ANTICORPOS ANTI-DNA' in procedimentos_do_paciente:
        return True
    
    if 'DOSAGEM DE PROTEINAS (URINA DE 24 HORAS)' in procedimentos_do_paciente:
        return True
    
    # Verifica estes 3 procedimentos: UREIA, CREATINA, URINA QUALITATIVA
    if ('DOSAGEM DE UREIA' in procedimentos_do_paciente) or ('CLEARANCE DE UREIA' in procedimentos_do_paciente):
        if ('DOSAGEM DE CREATININA' in procedimentos_do_paciente) or \
        ('DOSAGEM DE CREATININA NO LIQUIDO AMNIOTICO' in procedimentos_do_paciente) or \
        ('CLEARANCE DE CREATININA' in procedimentos_do_paciente):
            if 'ANALISE DE CARACTERES FISICOS, ELEMENTOS E SEDIMENTO DA URINA' in procedimentos_do_paciente:
                return True
            
    # Se não caiu em nenhuma das condições
    return False

def procedimentos_p3():
    """
    Conjunto de procedimentos listados no procedimento 3.
    """
    return set(['DETERMINAÇÃO DE COMPLEMENTO (CH50)', 'DOSAGEM DE COMPLEMENTO C3', 'DOSAGEM DE COMPLEMENTO C4',
               'PESQUISA DE ANTICORPOS ANTINUCLEO'
               'PESQUISA DE ANTICORPOS ANTI-DNA',
               'PESQUISA DE ANTICORPOS ANTI-SM',
               'PESQUISA DE ANTICORPO IGG ANTICARDIOLIPINA', 'PESQUISA DE ANTICORPO IGM ANTICARDIOLIPINA',
               'DOSAGEM DE ANTICOAGULANTE CIRCULANTE',
               'PESQUISA DE ANTICORPOS ANTI-SS-B (LA)',
               'PESQUISA DE ANTICORPOS ANTI-SS-A (RO)', 'PESQUISA DE ANTICORPOS ANTI-RIBONUCLEOPROTEINA (RNP)']
                )

def filtro_p3(row):
    """
    Verifica se a linha recebida por parâmetro está no
    conjunto de procedimentos listados no procedimento 3.
    """

    if row in procedimentos_p3():
        return True
    else:
        return False
    
def p3(df_paciente, col_procedimento):
    """ Como só precisa ter 1 dos itens, é só ver se ter interseção 
    entre os procedimentos do paciente e a lista dos procedimentos do p3 """
    
    procedimentos_do_paciente = set(df_paciente[col_procedimento].unique())
    set_p3 = procedimentos_p3()

    if procedimentos_do_paciente & set_p3: # Se tem interseção entre os dois conjuntos
        return True
    else:
        return False
    
    
def procedimentos_p4():
    """ 
    Conjunto de procedimentos listados no procedimento 4.
    """
    return set(['CLOROQUINA 150 MG (POR COMPRIMIDO)',
                'CLOROQUINA (E) 150 MG (POR COMPRIMIDO)',
                'HIDROXICLOROQUINA 400 MG (POR COMPRIMIDO)',
                'HIDROXICLOROQUINA (E) 400 MG (POR COMPRIMIDO)',
                'METILPREDNISOLONA 500 MG INJETAVEL (POR AMPOLA)',
                'AZATIOPRINA 50 MG (POR COMPRIMIDO)',
                'CICLOSPORINA 25 MG (POR CAPSULA)',
                'CICLOSPORINA 50 MG (POR CAPSULA)',
                'CICLOSPORINA 100 MG (POR CAPSULA)', 
                'CICLOSPORINA 100 MG/ML SOLUCAO ORAL (POR FRASCO DE 50 ML)'
                'METOTREXATO 2,5 MG (POR COMPRIMIDO)',
                'METOTREXATO 25 MG/ML INJETAVEL (POR AMPOLA DE 2 ML)',
                'METOTREXATO 25 MG/ML INJETAVEL (POR AMPOLA DE 20 ML)'
                ])

def filtro_p4(row):
    """
    Verifica se a linha recebida por parâmetro está no
    conjunto de procedimentos listados no procedimento 4.
    """
    if row in procedimentos_p4():
        return True
    else:
        return False
    
def p4(df_paciente, col_procedimento):
    """ Como só precisa ter 1 dos itens, é só ver se ter interseção 
    entre os procedimentos do paciente e a lista dos procedimentos do p4 """
    
    procedimentos_do_paciente = set(df_paciente[col_procedimento].unique())
    set_p4 = procedimentos_p4()

    if procedimentos_do_paciente & set_p4: # Se tem interseção entre os dois conjuntos
        return True
    else:
        return False