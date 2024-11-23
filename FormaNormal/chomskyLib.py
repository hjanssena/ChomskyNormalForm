from nltk import CFG

def parseLang(lenguaje):
    gramatica = CFG.fromstring(lenguaje)
    producciones = []
    for produccion in gramatica.productions():
        x = produccion.__str__().split(" -> ")
        producciones.append(x)
    return producciones

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

def parseVariables(producciones):
    variables = []
    for produccion in producciones:
        if produccion[0] not in variables:
            variables.append(produccion[0])
    return variables

def copiarProd(producciones):
    nuevo = []
    for produccion in producciones:
        nuevo.append(produccion.copy())
    return nuevo

def eliminarEpsilon(producciones):
    for produccion in producciones:
        if produccion[1] == "'epsilon'":
            variable = produccion[0]
            producciones.remove(produccion)

            for prod in producciones:
                x = prod[1]
                while variable in x:
                    x = x.replace(variable, "", 1).strip().replace("  ", " ")
                    if [prod[0],x] not in producciones:
                        producciones.insert(producciones.index(prod) + 1, [prod[0],x])
    return producciones

def eliminarUnitarios(producciones):
    for produccion in producciones:
        if " " not in produccion[1] and "'" not in produccion[1]:
            ubicacion = produccion[0]
            variable = produccion[1]
            count = 1
            index = producciones.index(produccion)
            producciones.remove(produccion)
            for prod in producciones:
                if variable in prod[0]:
                    if [ubicacion, prod[1]] not in producciones:
                        producciones.insert(index + count, [ubicacion, prod[1]])
                        count += 1
    return producciones

def restringirTerminales(producciones, terminales):
    for produccion in producciones:
        for terminal in terminales:
            if terminal in produccion[1] and len(produccion[1]) > len(terminal):
                produccion[1] = produccion[1].replace(terminal, "X" + terminal.replace("'", "").replace(" ", ""))
                if ["X" + terminal.replace("'", "").replace(" ", ""), terminal] not in producciones:
                    producciones.append(["X" + terminal.replace("'", "").replace(" ", ""), terminal])
    return producciones

def reducirReglas(producciones):
    count = 'A'
    for produccion in producciones:
        varLen = 0
        primero = False
        segundo = False
        queda = ""
        nuevo = ""
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
            while [produccion[0] + str(count), nuevo] in producciones:
                count = chr(ord(count) + 1)
            producciones.insert(producciones.index(produccion) + 1, [produccion[0] + str(count), nuevo])
    return producciones


lenguaje = '''
 S -> A A C D
 A -> 'a'A'b' | 'epsilon'
 C -> 'a'C | 'a'
 D -> 'a'D'a' | 'b'D'b' | 'epsilon'
 '''

print(repr(lenguaje))

producciones = parseLang(lenguaje)
terminales = parseTerminales(producciones)
producciones = eliminarEpsilon(producciones)
producciones = eliminarUnitarios(producciones)
producciones = restringirTerminales(producciones, terminales)
producciones = reducirReglas(producciones)

