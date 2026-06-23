#!/bin/bash

UMBRALCPU="80"
UMBRALRAM="80"
UMBRALDISCO="85"

echo "[$(date '+%Y/%m/%d %H:%M:%S')] Consulta estado del servidor"

USORAM=$(free | grep Mem | awk '{print int (($3 / $2)*100)}')

if [ "$USORAM" -ge "$UMBRALRAM" ]; then
	echo "WARNING, USO ELEVADO DE RAM. Uso actual: $USORAM%"
fi	
if [ "$USORAM" -le "$UMBRALRAM" ]; then
	echo "USO DE RAM NORMAL. Uso actual: $USORAM%"
fi

USODISCO=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')

if [ "$USODISCO" -ge "$UMBRALDISCO" ]; then
	echo "WARNING, DISCO CASI LLENO. Uso actual: $USODISCO"
fi
if [ "$USODISCO" -le "$UMBRALDISCO" ]; then
	echo "ESPACIO DISPONIBLE: $USODISCO"
fi

USOCPU=$(top -b -d 0.5 -n 5 | grep Cpu | tail -1 | awk '{print int(100-$8)}')

if [ "$USOCPU" -ge "$UMBRALCPU" ]; then
	echo "WARNING, uso alto de CPU. Uso actual: $USOCPU%"
fi
if [ "$USOCPU" -le "$UMBRALCPU" ]; then
	echo "Uso de CPU actual: $USOCPU%"
fi
