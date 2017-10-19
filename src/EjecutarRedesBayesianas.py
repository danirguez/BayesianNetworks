'''
Created on 12 jun. 2017

@author: Alfonso
'''

from EliminacionDeVariables import descarteDeVariables, factoresIniciales, \
    eliminacionVariablesOcultas, multiplicacionNormalizacionFactores
from Heuristicas import minDegree, minFill, minFactor
from InferenciaAproximada import muestraAleatoria, muestreoConRechazo
from RecomendadorDeEvidencias import RecomendarEvidencias
from SacarProbabilidades import sacarProb
import pgmpy.factors as pgmf
import pgmpy.models as pgmn
import pgmpy.readwrite.XMLBIF as pgmr


class EjecutarRedesBayesianas(object):
    '''
    classdocs
    '''
'''
    Variables para creacion del modelo
'''
variables = []
edges = []
tabular_cpds = [] 

''' 
    Variables para eliminacion de variables
'''
consultas = []
evidencias = []

print("LECTURA DEL XMLBIF\n\n")
XML = pgmr.XMLBIFReader("GrafoActividadFisica.xml")

print("Variables:\n")

'''
    Guardamos las variables.
'''
for variable in XML.get_variables():
    variables.append(variable)
    
print(variables)

print("\n--------------------------------------------------------\n")
print("Aristas:\n")

'''
    Guardamos las aristas
'''
for edge in XML.get_edges():
    edges.append(edge)
    
print(edges)

print("\n========================================================\n")
print("Impresion del Modelo Bayesiano\n")


'''
    Creamos el modelo
'''
Modelo = pgmn.BayesianModel()
Modelo.add_nodes_from(variables)
Modelo.add_edges_from(edges)

print("Variables o nodos:")
print(Modelo.nodes())
print("\n")
print("Aristas:")
print(Modelo.edges())
print("\n")

'''
    Metemos los tabular_cpds al modelo, que luego nos serviran para sacar las tablas de propiedades
'''
for variable, valores in XML.variable_CPD.items():
    cpd = pgmf.TabularCPD(variable,
                          len(XML.variable_states[variable]),
                          valores,
                          evidence = XML.variable_parents[variable],
                          evidence_card = [len(XML.variable_states[evidence_var])
                                           for evidence_var in XML.variable_parents[variable]])
    tabular_cpds.append(cpd)   
Modelo.add_cpds(*tabular_cpds)

print("CPDs:")
print(Modelo.cpds)

print("\n========================================================\n")

'''
    Mostramos tabla de probabilidad
'''

print("Probabilidades de cada variable:\n")
sacarProb(XML,Modelo,variables)

'''
    Elegimos la consulta y las evidencias para realizar el proceso de eliminacion de variables
    
    Proceso para aplicar EV:
        1.- Meter en consultas, la variable que se desee consultar.
        2.- Meter en evidencias, la variable o variables que se tengan en cuenta como tales.
        3.- Introducir en nuevasEvidencias las evidencias anteriormente introducidas, dandole el valor de 1 o 0, 
            en caso de que se quiera afirmar o negar respectivamente.
'''
#consultas.append('resistencia pulmonar')
#evidencias.append('ejercicio')
#evidencias.append('cuerpo atletico')

#consultas.append('salud mental')
#evidencias.append('autoestima')

#consultas.append('deportista profesional')
#evidencias.append('ejercicio')
#evidencias.append('obesidad')

consultas.append('esperanza de vida alta')
evidencias.append('obesidad')
evidencias.append('buena alimentacion')

print("\n========================================================\n")
print("ALGORITMO DE EV")
print("\n========================================================\n")

print("1.- Variables descartadas:\n")
descarteDeVariables(Modelo, consultas, evidencias, variables)

print("\n2.- Factores iniciales:\n")
#nuevasEvidencias = {'ejercicio':1,'cuerpo atletico':1}

#nuevasEvidencias = {'autoestima':0}

#nuevasEvidencias = {'ejercicio': 0, 'obesidad':1}

nuevasEvidencias = {'obesidad':0,'buena alimentacion':1}

factor = factoresIniciales(nuevasEvidencias,variables,Modelo)


print("\n3.- Resultado de eliminacion de variables ocultas:\n")
eliminacionVariablesOcultas(factor, consultas,evidencias)

print("\n4.- Multiplicacion de factores finales:\n")
multiplicacionNormalizacionFactores(eliminacionVariablesOcultas(factor,consultas, evidencias))


'''
    Muestras aleatorias de evidencias
'''

print("\n========================================================\n")
print("ALGORITMO DE MUESTREO CON RECHAZO")
print("\n========================================================\n")

print("\nMuestra aleatoria de evidencias:\n")
print(muestraAleatoria(Modelo))

'''
    Muestreo con rechazo
    
    Para aplicar este algoritmo de inferencia aproximada, se debera seguir los siguientes pasos:
    
        1.- Meter como segundo parametro de muestreoConRechazo la consulta
        2.- Meter como tercer parametro de muestreoConRechazo las evidencias, con sus respectivos valores (0 o 1)
'''

print("\nMuestreo con rechazo:\n")
muestreoRechazo = muestreoConRechazo(Modelo,consultas,nuevasEvidencias,10000)
print(muestreoRechazo)


'''
    Recomendador de evidencias
    
    Para poder aplicar este metodo:
    
        1.- Introducir como cuarto parametro la consulta.
        2.- Introducir como quinto parametro las evidencias, con sus respectivos valores (0 o 1)
'''

print("\n========================================================\n")
print("RECOMENDADOR DE EVIDENCIAS")
print("\n========================================================\n")

print("\nRecomendador de evidencias:\n")
print(RecomendarEvidencias(muestreoRechazo,Modelo,variables,consultas,nuevasEvidencias))


print("\nUso de heuristicas\n")
print("\nMIN DEGREE\n")
print(minDegree(factor,consultas))

print("\nMIN FILL\n")
print(minFill(factor,consultas))

print("\nMIN FACTOR\n")
print(minFactor(factor,consultas))