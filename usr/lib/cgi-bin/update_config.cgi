#!/bin/bash
echo "Content-type: text/html"
echo ""

read POST_DATA

declare -A NEW_NAMES
for entry in $(echo "$POST_DATA" | tr '&' ' '); do
  key=$(echo "$entry" | cut -d'=' -f1)
  val=$(echo "$entry" | cut -d'=' -f2 | sed 's/%20/ /g')
  if [[ $key =~ NAMES

\[[0-9]+\]

 ]]; then
    pin=$(echo $key | sed 's/NAMES

\[\([0-9]\+\)\]

/\1/')
    NEW_NAMES[$pin]="$val"
  fi
done

cp /etc/gpio_config.sh /etc/gpio_config.sh.bak

{
cat <<'EOF'
#!/bin/bash
R1=(2 3 4 5 6 7)
R2=(8 9 10 11 12 13)

declare -A GROUP=(
  [2]=R1 [3]=R1 [4]=R1 [5]=R1 [6]=R1 [7]=R1
  [8]=R2 [9]=R2 [10]=R2 [11]=R2 [12]=R2 [13]=R2
)

declare -A NAMES=(
EOF

for pin in "${!NEW_NAMES[@]}"; do
  echo "  [$pin]=\"${NEW_NAMES[$pin]}\""
done

cat <<'EOF'
)

declare -A PAIRS=(
  [2]=8 [3]=9 [4]=10 [5]=11 [6]=12 [7]=13
)
EOF
} > /etc/gpio_config.sh

echo "<h1>Configuración actualizada</h1>"
