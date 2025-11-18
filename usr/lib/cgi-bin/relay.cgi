#!/bin/bash
echo "Content-type: application/json"
echo ""

. /etc/gpio_config.sh

# Construir un mapa inverso de PAIRS (R2 -> R1)
declare -A PAIRS_INV
for pin in "${!PAIRS[@]}"; do
  pair=${PAIRS[$pin]}
  PAIRS_INV[$pair]=$pin
done

# Procesar parámetros de la URL
QUERY="$QUERY_STRING"
PIN=$(echo "$QUERY" | sed -n 's/.*pin=\([0-9]\+\).*/\1/p')
VIEW=$(echo "$QUERY" | sed -n 's/.*view=\([^&]*\).*/\1/p')





# Lógica de mando: exclusión por panel
if [ -n "$PIN" ] && [ -n "$VIEW" ]; then
  if [ "$VIEW" = "R1" ]; then
    # Apagar todas las antenas de R1
    for p in "${R1[@]}"; do
      pigs w "$p" 0
    done
    # Encender solo la seleccionada
    pigs w "$PIN" 1
  elif [ "$VIEW" = "R2" ]; then
    # Apagar todas las antenas de R2
    for p in "${R2[@]}"; do
      pigs w "$p" 0
    done
    # Encender solo la seleccionada
    pigs w "$PIN" 1
  fi
fi

# Función para imprimir cada grupo
print_group() {
  local group=$1
  echo "\"$group\":{"
  local first=1
  if [[ $group == "R1" ]]; then
    for pin in "${R1[@]}"; do
      [[ $first -eq 0 ]] && echo ","
      first=0
      state=$(pigs r "$pin")
      name=${NAMES[$pin]}
      echo "\"$pin\":{\"state\":$state,\"name\":\"$name\"}"
    done
  elif [[ $group == "R2" ]]; then
    for pin in "${R2[@]}"; do
      [[ $first -eq 0 ]] && echo ","
      first=0
      state=$(pigs r "$pin")
      pair=${PAIRS_INV[$pin]}
      name=${NAMES[$pair]}
      echo "\"$pin\":{\"state\":$state,\"name\":\"$name\"}"
    done
  fi
  echo "}"
}

# Salida JSON
echo "{"
print_group "R1"
echo ","
print_group "R2"
echo ","
echo "\"PAIRS\":{"
first=1
for pin in "${R1[@]}"; do
  [[ $first -eq 0 ]] && echo ","
  first=0
  echo "\"$pin\":${PAIRS[$pin]}"
done
echo "}"
echo "}"
