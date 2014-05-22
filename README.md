
 arkolect.py 1.0.0.
 Copyright (c) 2014 Ángel Coto <codiasw@gmail.com>.

 Genera inventario de archivos con sus respectivos hash (sha256).
 Puede especificar opcionalmente hash crc32, md5 ó sha1.

 Uso: python arkolect.py ?
                        -da [crc32|md5|sha1]
                        -de <directorio> [crc32|md5|sha1]
                        -der <directorio> [crc32|md5|sha1]

      Opciones:
                 ?: Muestra esta ayuda. La ayuda también se muestra cuando se 
                    ejecuta el programa sin argumento de entrada.
               -da: Genera inventario de los archivos del directorio actual.
               -de: Genera inventario de los archivos de <directorio>.
              -der: Genera inventario de <directorio> y subdirectorios.

 Este programa es software libre bajo licencia GPLv3.

