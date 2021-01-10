# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# A
import re


def cargar_lineas(file, inicio, fin):
    if isinstance(inicio, int) == False:
        return 'Parametro inicio debe ser un int'
    if isinstance(fin, int) == False:
        return 'Parametro fin debe ser un int'
    if inicio > fin:
        return 'Parametro fin debe ser mayor que inicio'
    f = open(file, 'r')

    if inicio <= 0:
        inicio = 1

    formatedText = []

    for index, linea in enumerate(f):
        if index in range(inicio, fin+1):
            linea = linea.strip().split(";")
            linea[len(linea)-1] = int(linea[len(linea)-1].replace(".", ""))
            linea[len(linea)-2] = int(linea[len(linea)-2])
            formatedText.append(linea)
    f.close()
    return formatedText


# mis_datos = cargar_lineas("./ine_mortalidad_espanna.csv", 7, 10)
# for dato in mis_datos:
#     print(dato)


def romano_a_entero(valor):
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if len(valor) > 1:
        num = 0
        i = 0
        try:
            for letra in valor:
                i = i+1
                if i < len(valor):
                    if roman[letra] < roman[valor[i]]:
                        num = num + (roman[letra] * -1)
                    else:
                        num = num + roman[letra]
                else:
                    num = num + roman[letra]
            return num
        except:
            return num
    else:
        return roman[valor]


# print(romano_a_entero('MCDXCII'))

# print([(r, romano_a_entero(r))
#        for r in ["I", "IV", "XIV", "XXXIX-IX", "VL", "LXIV", "MCDXCII"]])


# Apartado B


def es_grupo_y_no_total(causa):
    incluye = re.search(
        "^[0-9][0-9][0-9]\-[0-9][0-9][0-9](?!.*(t|T)odas).*$", causa)
    return bool(incluye)


lista_de_causas = [
    "009-041  II.Tumores",
    "009  Tumor maligno del esófago",
    "001-102  I-XXII.Todas las causas",
    "077-080  XIV.Enfermedades del sistema genitourinario",
    "082  XVI.Afecciones originadas en el periodo perinatal",
    "050-052  VI-VIII.Enfermedades del sistema nervioso y de los órganos de los sentidos"
]

# for causa in lista_de_causas:
#     print(causa.ljust(60), "\t", es_grupo_y_no_total(causa))

# Apartado C


def cargar_datos(file):
    f = open(file, 'r')
    formatedText = []

    formatedFile = cargar_lineas(file, 0, len(f.readlines()))
    lineasDescartadas = 0
    for linea in formatedFile:
        if es_grupo_y_no_total(linea[0]):
            lineaFormateada = formatear_linea(linea)
            formatedText.append(lineaFormateada)
        else:
            lineasDescartadas = lineasDescartadas+1
    f.close()
    return formatedText, lineasDescartadas


def formatear_linea(linea):
    numeros = linea[0].split(".")[0]
    titulo = linea[0].split(".")[1]
    numRomano = numeros[9:len(numeros)].split("-")[0]
    return (numeros,
            numRomano,
            romano_a_entero(numRomano),
            titulo,
            linea[len(linea)-2],
            linea[len(linea)-1])


# datos, num_lin_descartadas = cargar_datos("ine_mortalidad_espanna.csv")
# print(len(datos), num_lin_descartadas)
# for i in [13000, 34, 1001, 20000, 25000]:
#     print(datos[i])
    # print(type(datos[i]))


# Las funciones anteriores están bien para inspeccionar los datos, pero ahora deseamos almacenar el resultado en un par de tablas
# para su procesamiento posterior. La primera de ellas será un diccionario con los nombres de los grupos de enfermedades:
# 1 : 	Enfermedades infecciosas y parasitarias
# 2 :	Tumores
# 3 : 	Enfermedades de la sangre y de los órganos hematopoyéticos, y ciertos trastornos que afectan al mecanismo de la inmunidad
# 	…:  Etcétera.


def get_diccionario(file):
    f = open(file, 'r')
    formatedText = []
    for linea in f:
        linea = linea.strip().split(";")
        cabecera = linea[0]

        if "." in cabecera:
            numCabecera = cabecera.split(".")[0]
            texto = cabecera.split(".")[1]
            incluyeTodas = bool(re.search("Todas", texto))
            numRomano = numCabecera.split(" ")
            for valor in numRomano:
                esNumeroRomano = bool(re.search("[IXV]", valor))
                if esNumeroRomano and len(texto) > 0:
                    if "-" in valor and not incluyeTodas:
                        inicioConjunto = romano_a_entero(valor.split("-")[0])
                        finConjunto = romano_a_entero(valor.split("-")[1])
                        for i in range(inicioConjunto, finConjunto+1):
                            numeroDescripcion = [i, texto]
                            if numeroDescripcion not in formatedText:
                                formatedText.append(numeroDescripcion)
                    else:
                        numeroDescripcion = [romano_a_entero(valor), texto]
                        if numeroDescripcion not in formatedText:
                            formatedText.append(numeroDescripcion)
    f.close()
    return formatedText


print(get_diccionario("ine_mortalidad_espanna.csv"))
