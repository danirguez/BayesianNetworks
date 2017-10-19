'''
Created on 12 jun. 2017

@author: Alfonso
'''
import networkx
import pgmpy.factors as pgmf
from _functools import reduce


class EliminacionDeVariables(object):
    '''
    classdocs
    '''
    
padresDelNodo = []
variablesDescartadas = []
factorInicial = {}
variablesEliminadas = []
resultado = {}
multiplicacion = []

     
'''
    1.- Descarte de variables irrelevantes antes de comenzar.
            
            Deberemos descartar todas aquellas variables que se encuentren en el grafo por debajo de la consulta y las evidencias.
            Esto se hace porque no interferiran en nada a la hora de obtener la probabilidad.
            
            Primero sacamos de cada elemento entre la consulta y las evidencias, todos los nodos superiores, y los guardamos en un conjunto.
            Despues de esto, iremos variable por variable, mirando que no se encuentren ni dentro del conjunto, ni dentro de los nodos superiores,
            y estas variables, seran las que se metan al conjunto de variables descartadas.
'''
def descarteDeVariables(modelo, consultas, evidencias, variables):
    conjunto = consultas + evidencias
    for elemento in conjunto:
        subGrafo = modelo.subgraph(networkx.ancestors(modelo, elemento))
        for sub in subGrafo:
            padresDelNodo.append(sub)
     
    for variable in variables:
        if variable not in conjunto:
            if variable not in padresDelNodo:
                variablesDescartadas.append(variable)
    print(variablesDescartadas)
    
'''
    2.- Obtener factores iniciales a partir de la red 
    (ignorando variabes descartadas y teniendo en cuenta las evidencias)
    
            Primero introducimos en la variable creada factorInicial, la relacion entre variable y su respectivo factor obtenido del cpds.
    
            Depues miramos las variables y factores que han sido metidos a factorInicial, y se elimina la variable de la que depende otra, en caso de que
            se haya metido como evidencia o no.
    
            Por ultimo, se imprimen tanto las variables como las variables de las que depende
'''
def factoresIniciales(nuevasEvidencias,variables,modelo):
    cont = 0
    for variable in variables:
        if variable not in variablesDescartadas:
            factorInicial[variable] = modelo.cpds[cont].to_factor()
            
        cont = cont + 1
    for variable, valor in factorInicial.items():
        for scope in valor.scope():
            if scope in nuevasEvidencias and (valor != None):
                valor = valor.reduce([(scope, nuevasEvidencias[scope])])            
    for variable, valor in factorInicial.items():
        print(variable)
        print(valor.scope())
    return factorInicial
        
'''
    3.- Eliminacion de variables ocultas (a traves de las 
    correspondientes operaciones sobre los factores)
    
            Primero meter en un nuevo conjunto llamado variablesEliminadas las variables que no se encuentren ni en consulta ni en evidencias.
            
            Luego mirar dentro de este nuevo conjunto variable por variable al igual que mientras lo hacemos en el conjunto de factores iniciales,
            y en caso de que coincida la variable del conjunto de eliminadas, a la variable correscondiente al valor, se realizara el producto 
            y posteriormente la marginalizacion.
            
            Tras esto, se le asocia el valor del producto a la variable del factor con la que estabamos trabajando.
            
            Por ultimo, se recorrera de nuevo las variables con sus respectivos valores que se encuentran en el conjunto de factores inciales, pero esta
            vez ya actualizadas, a la vez que se recorreran las variables de las que dependen los valores de los factores iniciales.
            
            Mientras recorremos esto, en caso de que la variable de la que depende se encuentra dentro de la consulta, asociamos la variable del factor inicial
            con su respectivo valor, dentro de un nuevo conjunto que se usara pasa sacar ya el resultado final.
'''
def eliminacionVariablesOcultas(factor,consultas,evidencias):
    for variable, valor in factor.items():
        if variable not in consultas:
            if variable not in evidencias:
                variablesEliminadas.append(variable)
    for eliminada in variablesEliminadas:
        for variable, valor in factor.items():
            if eliminada in valor.scope():
                if len(valor.scope()) > 1:
                    producto = pgmf.factor_product(factor[eliminada],valor)
                    producto.marginalize([eliminada])
                    factor[variable] = producto
    for variable, valor in factor.items():
        for v in valor.scope():
            if v in consultas:
                resultado[variable] = valor
    for variable, valor in resultado.items():
        print(variable)
        print(valor.scope())
        print(valor.values)
        print("\n")
    return resultado
'''
   4.- Multiplicar los factores finales (en caso de que haya mas de uno)
           
           Recorremos las variables y valores de los factores actualizados con el ultimo metodo.
           
           En caso de que contenga la variable recorrida otra variable de la que dependa, se metera a un conjunto, que posteriormente sera
           multiplicado y finalmente normalizado.
'''
def multiplicacionNormalizacionFactores(factores):
    for variable, valor in factores.items():
        multiplicacion.append(valor)
    producto = reduce(lambda phi1, phi2: phi1 * phi2, multiplicacion)
    producto.normalize()
    print(producto.values)