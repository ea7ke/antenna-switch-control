#!/bin/bash
# Configuración de GPIOs para R1 y R2

R1=(2 3 4 5 6 7)
R2=(8 9 10 11 12 13)

declare -A GROUP=(
  [2]=R1 [3]=R1 [4]=R1 [5]=R1 [6]=R1 [7]=R1
  [8]=R2 [9]=R2 [10]=R2 [11]=R2 [12]=R2 [13]=R2
)

# Nombres definidos solo por pares (R1)
declare -A NAMES=(
  [2]="10m Yagi"
  [3]="15m Yagi"
  [4]="20m Yagi"
  [5]="40m Dipolo"
  [6]="80m Dipolo"
  [7]="160m L Inv"
)

# Mapeo de pares R1 -> R2
declare -A PAIRS=(
  [2]=8
  [3]=9
  [4]=10
  [5]=11
  [6]=12
  [7]=13
)
