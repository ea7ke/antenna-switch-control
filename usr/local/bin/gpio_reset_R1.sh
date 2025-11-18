#!/bin/bash
# Apagar todas las antenas al arranque

. /etc/gpio_config.sh

# Apagar todos los pines de R1 y R2
for p in "${R1[@]}"; do
  pigs w "$p" 0
done
