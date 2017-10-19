'''
Created on 17 jun. 2017

@author: Alfonso
'''

class RecomendadorDeEvidencias(object):
    '''
    classdocs
    '''
    

posibleSolucion = []
evidenciaRecomendada = {}
numeroEvidencias = {}

'''
    RECOMENDADOR DE EVIDENCIAS
        
            Primero se busca las variables que no se encuentre ni en consulta ni en las evidencias, y se mete en un conjunto como posible solucion
            o candidatas.
            
            Posteriormente se realiza una busqueda por cada una de esas variables candidatas y se mira segun la inferencia (realizada con muestreo con rechazo)
            la probabilidad de si y de no, y se hace una suma y una normalizacion
            
            Luego se va guardando la variable que mayor normalizacion tenga, actualizando hasta acabar de recorrer todas las posibles soluciones.
            
'''

def RecomendarEvidencias(inferencia,Modelo, variables, consultas, evidencias):
    acumulador = 0
    evidenciasEnList = list(evidencias.keys())
    res = None
    evidenciaElegida = None

    for variable in variables:
        if(variable not in consultas) and (variable not in evidenciasEnList):
            posibleSolucion.append(variable)
    for posible in posibleSolucion:
        probabilidadNo = inferencia[(0,)]
        probabilidadSi = inferencia[(1,)]
        sumatorio = probabilidadNo + probabilidadSi
        normalizacion = abs((probabilidadNo/sumatorio) - (probabilidadSi/sumatorio))
        if acumulador < normalizacion:
            res = 0
            evidenciaElegida = posible
            acumulador = normalizacion
            evidenciaRecomendada[evidenciaElegida] = res
        
    return evidenciaRecomendada