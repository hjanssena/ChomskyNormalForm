from nltk import CFG

#Parsea el input y devuelve una lista de las producciones conformada por listas en donde [0] es la variable y [1] es lo que produce
def parseLang(lenguaje):
    gramatica = CFG.fromstring(lenguaje)
    producciones = []
    for produccion in gramatica.productions():
        x = produccion.__str__().split(" -> ")
        producciones.append(x)
    return producciones

#Dada la lista de producciones, devuelve una lista de todas las constantes presentes en el lenguaje
def parseTerminales(producciones):
    terminales = []
    for produccion in producciones:
        term = ""
        inside = False
        for c in produccion[1]:
            if c == "'" and inside == False:
                inside = True
            elif c == "'" and inside == True:
                inside = False
                if "'" + term + "'" not in terminales:
                    terminales.append("'" + term + "'")
                term = ""
            elif inside == True:
                term += c
    return terminales

#Dada la lista de producciones, devuelve una lista de todas las variables
def parseVariables(producciones):
    variables = []
    for produccion in producciones:
        if produccion[0] not in variables:
            variables.append(produccion[0])
    return variables

#Devuelve una copia de la lista de producciones
def copiarProd(producciones):
    nuevo = []
    for produccion in producciones:
        nuevo.append(produccion.copy())
    return nuevo

#Paso 1 para convertir a forma normal de chomsky
def eliminarEpsilon(producciones):
    for produccion in producciones:
        ok = False
        while not ok:
            if produccion[1] == "'epsilon'" or produccion[1] == "":
                #Guardamos valor de variable que produce epsilon y eliminamos la produccion de la lista
                variable = produccion[0]
                index = producciones.index(produccion)
                producciones.remove(produccion)

                #Revisamos en cada produccion si se produce la variable que produce epsilon
                for prod in producciones:
                    x = prod[1]
                    #Cuando encuentra una que lo produce, se insertan las producciones de esa variable a la variable que la produce
                    while variable in x:
                        x = x.replace(variable, "", 1).strip().replace("  ", " ")
                        if [prod[0],x] not in producciones and x != "":
                            producciones.insert(producciones.index(prod) + 1, [prod[0],x])
                        if x == "":
                            print("No es posible llegar a la forma normal. Se puede generar epsilon desde la raiz del lenguaje.")
                produccion = producciones[index]
            else:
                ok = True
    return producciones

#Paso 2 para convertir a forma normal de chomsky
def eliminarUnitarios(producciones):
    for produccion in producciones:
        ok = False
        #Checamos todas las producciones que sean unitarias
        while not ok:
            if " " not in produccion[1] and "'" not in produccion[1]:
                #Guardamos la variable que la produce y la variable producida. Se elimina la produccion.
                ubicacion = produccion[0]
                variable = produccion[1]
                count = 0
                index = producciones.index(produccion)
                producciones.remove(produccion)

                for prod in producciones:
                    #Insertamos una nueva produccion a la lista de cada produccion de la variable unitara.
                    #Quedando: Variable que produce unitario -> produccion del unitario
                    if variable in prod[0]:
                        if [ubicacion, prod[1]] not in producciones:
                            producciones.insert(index + count, [ubicacion, prod[1]])
                            count += 1
                produccion = producciones[index]
            else:
                ok = True
    return producciones

#Paso 3 para convertir a forma normal de chomsky
def restringirTerminales(producciones, terminales):
    for produccion in producciones:
        for terminal in terminales:
            #Checo en cada produccion que produce terminal si esta sola o no
            if terminal in produccion[1] and len(produccion[1]) > len(terminal):
                #Si se produce mas que una terminal, esta se reemplaza por una variable formada por X mas la terminal. Por ejemplo 'a' = Xa
                #Posteriormente se crea la produccion de la nueva varuable a la terminal. 
                produccion[1] = produccion[1].replace(terminal, "X" + terminal.replace("'", "").replace(" ", ""))
                if ["X" + terminal.replace("'", "").replace(" ", ""), terminal] not in producciones:
                    producciones.append(["X" + terminal.replace("'", "").replace(" ", ""), terminal])
    return producciones

#Paso 4 para convertir a forma normal de chomsky
def reducirReglas(producciones):
    count = 'A'
    for produccion in producciones:
        varLen = 0
        primero = False
        segundo = False
        queda = "" #Aca guardo las primeras dos variables de la produccion
        nuevo = "" #Aca guardo lo que sobra para crear una nueva produccion
        for c in produccion[1]:
            if c == " " and not primero:
                primero = True
                queda += c
                varLen = 0
            elif c == " " and not segundo:
                segundo = True
                nuevo += queda[-varLen] + c
                count = chr(ord(count) + 1)
                queda = queda[:-varLen] + produccion[0] + str(count)
            elif not segundo:
                queda += c
                varLen += 1
            else:
                nuevo += c
        produccion[1] = queda 
        if len(nuevo) > 0:
            #Si hay algo en nuevo, se crea una nueva produccion
            while [produccion[0] + str(count), nuevo] in producciones:
                count = chr(ord(count) + 1)#Para que no se repitan las letras de las variables
            producciones.insert(producciones.index(produccion) + 1, [produccion[0] + str(count), nuevo])
    return producciones

lenguaje = """
 S -> A A C D 
 A -> 'a'A'b' | 'epsilon'
 C -> 'a'C | 'a' | 'epsilon'
 D -> 'a'D'a' | 'b'D'b' | 'epsilon'
 """

producciones = parseLang(lenguaje)
terminales = parseTerminales(producciones)
producciones = eliminarEpsilon(producciones)
producciones = eliminarUnitarios(producciones)
producciones = restringirTerminales(producciones, terminales)
producciones = reducirReglas(producciones)

