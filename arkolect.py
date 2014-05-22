#!/usr/bin/python
# -*- coding: utf-8 -*-

# arkolect.py
#       
#  Copyright 2014 Ángel Coto <codiasw@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details (http://www.gnu.org/licenses/gpl.txt)
#  

# Descripción:
# Este programa recorre directorios para contruír un inventario de archivos.

# Historial de versión
# 1.0.0: * Se hace un fork de artamiz 2.0.1.
#        * Se hacen las modificaciones para que la herramienta genere el inventario 
#          en formato csv separado por tabs.
#        * La salida incluye el tamaño de cada archivo en bytes y la fecha de modificación.

import hashlib, zlib, os
from sys import argv
from getpass import getuser
from time import localtime, strftime

### Define la versión del programa
ver = '1.0.0'

### Función que imprime en pantalla ayuda sobre el uso del programa
def hintdeuso():
	programa = os.path.basename(argv[0]) #Extrae el nombre del programa (tiene utilidad en Windows)
	print('\n {0} {1}.'.format(programa,ver))
	print(' Copyright (c) 2014 Ángel Coto <codiasw@gmail.com>.\n')
	print(' Genera inventario de archivos con sus respectivos hash (sha256).')
	print(' Puede especificar opcionalmente hash crc32, md5 ó sha1.\n')
	print(' Uso: python {0} ?'.format(programa))
	print('                        -da [crc32|md5|sha1]')
	print( '                        -de <directorio> [crc32|md5|sha1]')
	print('                        -der <directorio> [crc32|md5|sha1]\n')
	print('      Opciones:')
	print('''                 ?: Muestra esta ayuda. La ayuda también se muestra cuando se 
                    ejecuta el programa sin argumento de entrada.''')
	print('               -da: Genera inventario de los archivos del directorio actual.')
	print('               -de: Genera inventario de los archivos de <directorio>.')
	print('              -der: Genera inventario de <directorio> y subdirectorios.\n')
	print(' Este programa es software libre bajo licencia GPLv3.\n')

### Inicializa mensajes de error
error1 = "* Error 1: '{0}' no existe."
error2 = "* Error 2: '{0}' no es opción reconocida."
error3 = "* Error 3: '{0}' es un directorio. No se puede calcular hash a un directorio."
error4 = "* Error 4: No se tiene permisos para leer el archivo '{0}'."
error5 = "* Error 5: '{0}' no es un directorio."
error6 = "* Error 6: '{0}' no es un archivo."
error7 = "* Error 7: '{0}' no es un argumento esperado."
error8 = "* Error 8: Debe especificar un directorio."
error9 = "* Error 9: Debe especificar los dos archivos a comparar."
error10 = '''* Error 10: Debe especificar el archivo que contiene los valores hash
            y el directorio que contiene los archivos a verificar.'''
error11 = "* Error 11: '{0}' no tiene líneas con estructura de tabla hash."
error12 = "* Error 12: '{0}' está siendo usado por otro proceso en forma exclusiva o ha sido removido."
error13 = "* Error 13: Debe especificar archivo de tabla hash."
error14 = "* Error 14: Debe especificar cadena de texto."
error15 = "* Error 15: No se puede abrir el directorio {0}."

### Función para generar la hora en formato estándar
def fechahora(hora):
	return strftime('%Y-%m-%d %H:%M:%S', hora)
	
### Función para imprimir encabezado de tabla hash
def encabezadotablahash(directorio, algoritmo):
	print('Inventario (' + algoritmo + ') generado por: ' + getuser())
	print('Para: ' + directorio)
	print('Inicio: ' + fechahora(localtime()))
	print('----------------------------------------------------------------')
	print('HASH\tBYTES\tFECHA_MODIFICADO\tARCHIVO')

### Función para imprimir el pie de informe
def piedeinforme():
	print('----------------------------------------------------------------')
	print('Fin: ' + fechahora(localtime()))

### Función que verifica si una cadena es hexadecimal
#  
#  name: eshex
#  @param: cadena caracter a analizar
#  @return: True si es hexadecimal, False si no lo es
def eshex(valor):
	try:
		entero = int(valor,16)
		conversion = True
	except:
		conversion = False
	return conversion

### Función que detecta si un archivo está bloqueado por otro proceso
#
#  name: enllavado
#  @param: nombre del archivo a verificar
#  @return: True si está bloqueado, False si no lo está
def enllavado(archivo):
	try:
		f = open(archivo,'rb')
		data = f.read(8192)
		f.close()
		return(False)
	except:
		return(True)

def algoritmousado(valor):
	longitud = len(valor)
	if longitud == 64:
		algoritmo = 'sha256'
	elif longitud == 40:
		algoritmo = 'sha1'
	elif longitud == 32:
		algoritmo = 'md5'
	else:
		algoritmo = 'crc32'
	return algoritmo


### Función que calcula el hash para el archivo de entrada
#  
#  nombre: calcsum
#  @param: nombre del objeto a calcular el hash
#          tipo de objeto al cual se calculará hash ('t': texto; 'f': archivo)
#          algorito que se utilizará para calcular el hash
#  @return: hash calculado con algoritmo seleccionado
def calcsum(objeto,tipoobjeto,algoritmo):
	valorhash = 0
	
	if algoritmo == 'crc32':
		if tipoobjeto == 't':
			valorhash = zlib.crc32(objeto)
		else:
			fh = open(objeto,'rb') # Abre lectura en modo binario
			for linea in fh:
				valorhash = zlib.crc32(linea, valorhash)
		valorhash = "%X"%(valorhash & 0xFFFFFFFF) #Almacena el valor hash en hexadecimal

	else:
		if algoritmo == 'sha256':
			m = hashlib.sha256()
		elif algoritmo == 'sha1':
			m = hashlib.sha1()
		else:
			m = hashlib.md5()
		if tipoobjeto == 't':
			m.update(objeto)
		else:
			fh = open(objeto, 'rb') #Abre lectura en modo binario
			while True:
				data = fh.read(8192) #Lee el archivo en bloques de 8Kb
				if not data:
					break
				m.update(data)
			fh.close
		valorhash = m.hexdigest()
		
	return valorhash #Devuelve el valor hash en hexadecimal

### Función que calcula e imprime los hashes para los archivos del directorio especificado    
#  
#  nombre: calcsumdir
#  @param: directorio en el cual están los archivos a los cuale se les calculará hash
#  @return: ninguno
def calcsumdir(ruta,algoritmo):
	errores = []
	error = False
	try:
		listado = os.listdir(ruta) #Extrae el listado de archivos del directorio
	except:
		errores.append(error15.format(ruta))
		error = True
	
	if not error:
	
		listado.sort() #Ordena los elementos de la lista para mejor lectura de la salida
		
		for archivo in listado: #Recorre el listado de elementos en el directorio
			if os.path.isfile(archivo): #Verifica si el elemento es un archivo
				if os.access(archivo,os.R_OK):
					if not enllavado(archivo):
						horamodificado = fechahora(localtime(os.path.getmtime(archivo)))
						print(calcsum(archivo,'f',algoritmo) + '\t' + str(os.path.getsize(archivo))) \
						+ '\t' + horamodificado + '\t' + archivo
					else:
						print(error12.format(archivo))
				else:
					 errores.append(error4.format(archivo)) #Incorpora el mensaje de error al listado de errores
			else:
				errores.append(error3.format(archivo))  #Si es directorio solo lo informa
			
	for mensaje in errores:
		print(mensaje)

### Función que calcula e calcula los hashes para los archivos del directorio especificado y de sus subdirectorios
#  
#  nombre: calcsumdirrec
#  @param: directorio en el cual están los archivos a los cuale se les calculará hash
#  @return: ninguno
def calcsumdirrec(ruta, algoritmo):
	
	if os.path.isdir(ruta):
		error = False
		try:
			os.chdir(ruta) # Cambia al directorio
		except:
			print(error15.format(ruta))
			error = True
		
		if not error:
			directorio = os.getcwd()
			try:
				listado = os.listdir(directorio) #Obtiene los elementos del directorio
			except:
				print(error15.format(ruta))
				error = True
				
			if not error:
				for nombre in listado: #Para cada nombre en el listado
					elemento = os.path.join(directorio,nombre) #Construye la ruta completa
					calcsumdirrec(elemento,algoritmo)

	else:
		if os.access(ruta,os.R_OK):
			if not enllavado(ruta):
				horamodificado = fechahora(localtime(os.path.getmtime(ruta)))
				linea = calcsum(ruta,'f',algoritmo) + '\t'+str(os.path.getsize(ruta)) + '\t' + horamodificado + '\t' + ruta
			else:
				linea = error12.format(ruta)
		else:
			 linea = (error4.format(ruta)) 
		print(linea)
#		listasalida.append(linea) #Lo agrega en la lista de salida
	return 0


def main():
	### Inicia el programa leyendo el argumento y validándolo
	#
	try: #Verifica si hay al menos un argumento
		ar1 = argv[1]
	except: #Salida por no existir argumento
		hintdeuso()
		exit()

	### Se evalúa el argumento1 para determinar la opción elegida
	if ar1 == '?': #Imprime la ayuda
		hintdeuso()

	elif ar1 == '-da': #Entra si calculará hash para el directorio de trabajo
		error = False
		try: # Busca determianr si hay algoritmo especificado
			ar2 = argv[2] #Si hay un segundo argumento, es un error
			if ar2 <> 'crc32' and ar2 <> 'sha1' and ar2 <> 'md5':
				error = True
				print(error7.format(ar2))
			
		except: # Si no se especificó entonces asigna el algoritmo por defecto
			ar2 = 'sha256'
		
		if not error:
			directorio = os.getcwd() #Captura del directorio de trabajo
			encabezadotablahash(directorio,ar2) #Imprime el encabezado de la salida
			calcsumdir(directorio,ar2) #Calcula los hashes del directorio de trabajo
			piedeinforme()
		
	elif ar1 == '-de' or ar1 == '-der': #Entra si calculará hash para directorio especificado o generación recursiva
		try:
			ar2 = argv[2]
		except: 
			print(error8)
			exit()
			
		if os.path.exists(ar2): #Verifica si el directorio existe
			if os.path.isdir(ar2): #Si el directorio es válido
			
				error = False
				try: # Busca determinar si hay algoritmo especificado
					ar3 = argv[3]
					if ar3 <> 'crc32' and ar3 <> 'sha1' and ar3 <> 'md5':
						error = True
						print(error7.format(ar3))
					
				except: # Si no se especificó entonces asigna el algoritmo por defecto
					ar3 = 'sha256'
				
				if not error:
					os.chdir(ar2)
					directorio = os.getcwd()
					encabezadotablahash(directorio,ar3)
					
					if ar1 == '-de': #Si es generación solo a directorio específico
						calcsumdir(directorio,ar3) #Calcula los hashes del directorio especificado

					else: #Es generación recursiva
						calcsumdirrec(directorio,ar3) # Llama la función de cálculo de hash para directorios recursivos
						
					piedeinforme()
				
			else:
				print(error5.format(ar2))
				
		else: #El directorio no existe
				print(error1.format(ar2))

	else: #Entra si no se especificó argumento.  Calcula hash si es un archivo
		print(error2.format(ar1))

if __name__ == '__main__':
	main()
else:
	None
