#!/bin/bash

# Definición de limites

UMBRALCPU="80"
UMBRALRAM="80"
UMBRALDISCO="85"

# Fecha de la consulta
echo "[$(date '+%Y/%m/%d %H:%M:%S')] Consulta estado del servidor"

# Definición del uso de la RAM
USORAM=$(free | grep Mem | awk '{print int (($3 / $2)*100)}')

# Respuesta que se debe imprimir

if [ "$USORAM" -ge "$UMBRALRAM" ]; then
	echo "WARNING, USO ELEVADO DE RAM. Uso actual: $USORAM%"
fi	
if [ "$USORAM" -le "$UMBRALRAM" ]; then
	echo "USO DE RAM NORMAL. Uso actual: $USORAM%"
fi

# Definición del uso del disco

USODISCO=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')

# Respuesta que imprime el disco
if [ "$USODISCO" -ge "$UMBRALDISCO" ]; then
	echo "WARNING, DISCO CASI LLENO. Uso actual: $USODISCO"
fi
if [ "$USODISCO" -le "$UMBRALDISCO" ]; then
	echo "ESPACIO DISPONIBLE: $USODISCO"
fi

# Definición del uso de la CPU

USOCPU=$(top -b -d 0.5 -n 5 | grep Cpu | tail -1 | awk '{print int(100-$8)}')

# Respuesta que se imprime del uso del CPU
if [ "$USOCPU" -ge "$UMBRALCPU" ]; then
	echo "WARNING, uso alto de CPU. Uso actual: $USOCPU%"
fi
if [ "$USOCPU" -le "$UMBRALCPU" ]; then
	echo "Uso de CPU actual: $USOCPU%"
fi
