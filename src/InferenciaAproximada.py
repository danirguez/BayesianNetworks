'''
Created on 14 jun. 2017

@author: Alfonso
'''
import itertools
import random
import networkx


class InferenciaAproximada(object):
    '''
    classdocs
    '''


def seleccionarProbabilidad(cpd, valor, evidencia):
    padres = cpd.evidence if cpd.evidence else []
    valores_evidencia = tuple(evidencia[var] for var in padres)
    return cpd.values[valor][valores_evidencia]

def generarValorAleatorio(cardinalidad, probabilidades):
    p = random.random()
    acumuladas = 0
    for valor in range(cardinalidad):
        acumuladas += probabilidades[valor]
        if (p <= acumuladas).all():
            return valor
        
        
'''
    Con muestra aleatoria conseguimos una muestra aleatoria de los valores de nuestro grafo.
'''
def muestraAleatoria(red):
    variables = networkx.topological_sort(red)
    valores = {}
    for variable in variables:
        cpd = red.get_cpds(variable)
        cardinalidad = cpd.variable_card
        probabilidades = [seleccionarProbabilidad(cpd,valor,valores) 
                             for valor in range(cardinalidad)]
        valor = generarValorAleatorio(cardinalidad,probabilidades)
        valores[variable] = valor
    return valores


def muestraConsistente(muestra,evidencia):
    return all([muestra[var] == evidencia[var] for var in evidencia])

def muestreoConRechazo(Modelo,consulta,evidencias,N):
    muestras = [muestraAleatoria(Modelo) for i in range(N)]
    Validas = []
    for muestra in muestras:
        if muestraConsistente(muestra, evidencias):
            Validas.append(muestra)
    cardinalidades = [Modelo.get_cpds(variable).variable_card
                     for variable in consulta]
    combinaciones = itertools.product(*(range(i)
                                       for i in cardinalidades))
    frecuencias = {combinacion : 0
                  for combinacion in combinaciones}
    for muestra in Validas:
        combinacion = tuple(muestra[variable]
                            for variable in consulta)
        try:
            frecuencias[combinacion] += 1
        except:
            frecuencias
    return frecuencias
