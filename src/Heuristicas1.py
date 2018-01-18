'''
Created on 17 jun. 2017

@author: Alfonso
'''

class Heuristicas(object):
    '''
    classdocs
    '''

variablesAcumuladas = []
'''
    Primero se inicializa c a -1, que es una variable de conexiones.
    
    Se mira todas las variables, y si esta perteneces a la consulta, se ignora y se continua.
    
    Se meten todas las variables en el conjunto de variables conectadas, que se encuentren en el mismo factor que la variable que estemos viendo actualmente.
    
    Luego se comparan y si estamos en la primera variable o el numero de conexiones es menor que el de la variable actual, 
    la conexion se actualiza al tamanyo de la lista de las variables conectadas y se mete en el resultado la variable.
'''
def minDegree(factor,consultas):
    variablesAcumuladas.clear()
    for variable, valor in factor.items():
        variablesAcumuladas.append(variable)
        
    res = []
    c = -1
    for variable in variablesAcumuladas:
        if variable == consultas:
            continue
        variablesConectadas = []
        for v, valor in factor.items():
            if variable in v[0]:
                variablesConectadas.append(v)
        if c == -1:
            c = len(variablesConectadas)
            res.append(variable)
        elif c > len(variablesConectadas):
            c = len(variablesConectadas)
            res.append(variable)
    return res
'''
    Este metodo no hemos sido capaces de sacarlo, y esto es hasta donde hemos llegado.
'''
def minFill(factor,consultas):
    variablesAcumuladas.clear()
    c = -1
    res = []
    variablesConectadas = {}
    for variable, valor in factor.items():
        variablesAcumuladas.append(variable)
    for variable in variablesAcumuladas:
        variablesConectadas[variable] = []
        for v, valor in factor.items():
            if variable in v[0]:
                variablesConectadas[variable] = variablesConectadas[variable] + v[0]
        variablesConectadas[variable] = list(set(variablesConectadas[variable]))
    for variable in variablesConectadas.keys():
        if variable == consultas:
            continue
        acum = 0
        variablesNuevas = variablesConectadas[variable]
        
        for variableNueva in variablesNuevas:
            if len(variablesNuevas) > 1:
                for variableNueva2 in variablesNuevas:
                    if variableNueva == variableNueva2:
                        continue
                    if variableNueva2 not in variablesConectadas[variableNueva]:
                        acum = acum + 1
            if c == -1:
                c = acum
                res.append(variable)
            elif c > acum:
                c = acum
                res.append(variable)
    return res
'''
    Se inicializa una variable como el tamanyo del factor.
    
    En caso de ser la variable una consulta, ignoramos esta.
    
    Recorremos todos los factores y variables, y si en el factor esta la variable, se meten las variables del factor en las variables finales.
    
    Seleccionamos si es la primera variable y si el tamanyo del factor es menor que el tamanyo del conjunto de las variables finales.
'''
def minFactor(factor,consultas):
    variablesAcumuladas.clear()
    t = -1
    res = []
    for variable, valor in factor.items():
        variablesAcumuladas.append(variable)
    for variable in variablesAcumuladas:
        if variable == consultas:
            continue
        finales = []
        for var,valor in factor.items():
            if variable in var[0]:
                finales.append(var)
        if t == -1:
            t = len(finales)
            res.append(variable)
        elif t > len(finales):
            t = len(finales)
            res.append(variable)
    return res