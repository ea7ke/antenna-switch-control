#!/bin/bash
# Apagar todas las antenas al arranque

. /etc/antenna/gpio_config.sh

for p in "${R2[@]}"; do
  pigs w "$p" 0
done
