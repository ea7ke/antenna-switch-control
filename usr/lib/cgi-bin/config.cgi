#!/bin/bash
# /usr/lib/cgi-bin/config.cgi
# Configuración de GPIOs con edición de nombres/pares y trazas de depuración

echo "Content-type: text/html"
echo ""

LOG="/tmp/config_debug.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') | REQUEST_METHOD=$REQUEST_METHOD CONTENT_LENGTH=$CONTENT_LENGTH" >> "$LOG"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$LOG"; }

log "=== Nueva petición a config.cgi ==="
log "REQUEST_METHOD=$REQUEST_METHOD CONTENT_LENGTH=$CONTENT_LENGTH"

if ! source /etc/gpio_config.sh 2>>"$LOG"; then
  log "ERROR: No se pudo cargar /etc/gpio_config.sh"
  echo "<p style='color:red'><b>Error:</b> no se pudo cargar /etc/gpio_config.sh</p>"
fi

urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }

if [ "$REQUEST_METHOD" = "POST" ]; then
  if [ -n "$CONTENT_LENGTH" ]; then
    read -n "$CONTENT_LENGTH" POST_DATA
    log "POST_DATA(raw)=$POST_DATA"

    TMP="/tmp/gpio_config_new.sh"
    {
      echo "#!/bin/bash"
      echo "R1=(${R1[@]})"
      echo "R2=(${R2[@]})"

      echo "declare -A PAIRS=("
      for P in "${R1[@]}"; do
        PAIR_RAW=$(echo "$POST_DATA" | sed -n "s/.*pair$P=\([^&]*\).*/\1/p")
        PAIR=$(urldecode "$PAIR_RAW")
        echo "  [$P]=$PAIR"
        log "PAIR[$P]=$PAIR"
      done
      echo ")"

      echo "declare -A NAMES=("
      for P in "${R1[@]}"; do
        NAME_RAW=$(echo "$POST_DATA" | sed -n "s/.*name$P=\([^&]*\).*/\1/p")
        NAME=$(urldecode "$NAME_RAW")
        [ -z "$NAME" ] && NAME="${NAMES[$P]}"
        NAME_ESCAPED=$(printf "%s" "$NAME" | sed 's/"/\\"/g')
        echo "  [$P]=\"$NAME_ESCAPED\""
        log "NAME[$P]='$NAME_ESCAPED'"
      done
      echo ")"

      echo "for P in \"\${R1[@]}\"; do PAR=\${PAIRS[\$P]}; NAMES[\$PAR]=\"\${NAMES[\$P]} (R2)\"; done"
    } > "$TMP"

    if mv "$TMP" /etc/gpio_config.sh 2>>"$LOG"; then
      log "OK: /etc/gpio_config.sh actualizado"
      echo "<p style='color:green;font-weight:bold'>✅ Configuración actualizada</p>"
    else
      log "ERROR: Fallo al mover $TMP a /etc/gpio_config.sh"
      echo "<p style='color:red'><b>Error:</b> no se pudo escribir en /etc/gpio_config.sh</p>"
    fi
  fi
fi

# Página HTML
echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Configuración GPIO</title>"
echo "<style>table{border-collapse:collapse;width:90%}th,td{border:1px solid #ccc;padding:8px;text-align:center}th{background:#f7f7f7}input{width:95%}caption{font-weight:bold;margin-bottom:8px}</style>"
echo "</head><body><h1>Configuración de GPIOs</h1><p>Las etiquetas de R2 se generan automáticamente a partir de R1.</p>"
echo "<form method='POST'><table><caption>Editar nombres y pares</caption>"
echo "<tr><th>GPIO</th><th>Nombre</th><th>Grupo</th><th>Par (GPIO en R2)</th></tr>"

html_escape() { printf "%s" "$1" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/"/\&quot;/g'; }

for P in "${R1[@]}"; do
  NAME_SHOW=$(html_escape "${NAMES[$P]}")
  PAIR_SHOW="${PAIRS[$P]}"
  echo "<tr><td>$P</td><td><input type='text' name='name$P' value='$NAME_SHOW'></td><td>R1</td><td><input type='number' name='pair$P' value='$PAIR_SHOW' min='0'></td></tr>"
done

for P in "${R2[@]}"; do
  NAME_SHOW=$(html_escape "${NAMES[$P]}")
  PAIR_SHOW="${PAIRS[$P]}"
  echo "<tr><td>$P</td><td><input type='text' value='$NAME_SHOW' disabled></td><td>R2 (auto)</td><td>$PAIR_SHOW</td></tr>"
done

echo "</table><br><input type='submit' value='Guardar cambios'></form>"
echo "<h3>Depuración</h3><p>Consulta el log en: <code>/tmp/config_debug.log</code></p></body></html>"
