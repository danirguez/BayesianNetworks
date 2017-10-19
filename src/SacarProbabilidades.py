'''
Created on 13 jun. 2017

@author: Alfonso
'''
import pgmpy.factors as pgmf

class SacarProbabilidades(object):
    '''
    classdocs
    '''
tabular_cpds = []      

def sacarProb(XML,modelo,variables):
    
    '''
    Sacamos las tablas de probabilidades
    '''
    for variable in variables:
        print("Tabla de " + variable)
        tabla = modelo.get_cpds(variable)
        evidencias = XML.variable_parents[variable]
        for evidencia in evidencias:
            print("Con respecto a " + evidencia)
        print(tabla.values)
        print("\n") 
