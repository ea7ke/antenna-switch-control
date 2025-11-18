#!/bin/bash
echo "Content-type: application/json"
echo ""

# Cargar configuración
. /etc/gpio_config.sh

# Función para imprimir estado de un grupo
print_group() {
  local group=$1
  echo "\"$group\":{"
  local first=1
  for pin in ${!NAMES[@]}; do
    # Filtrar por grupo
    if [[ ${GROUP[$pin]} == "$group" ]]; then
      [[ $first -eq 0 ]] && echo ","
      first=0
      state=$(gpio read "$pin")   # o pigpio/pigs según uses
      name=${NAMES[$pin]}
      echo "\"$pin\":{\"state\":$state,\"name\":\"$name\"}"
    fi
  done
  echo "}"
}

# Construir JSON
echo "{"
print_group "R1"
echo ","
print_group "R2"
echo ","

# Clave PAIRS: mapeo R1->R2
echo "\"PAIRS\":{"
first=1
for pin in "${!PAIRS[@]}"; do
  [[ $first -eq 0 ]] && echo ","
  first=0
  echo "\"$pin\":${PAIRS[$pin]}"
done
echo "}"

echo "}"
