#!/bin/bash
# /usr/lib/cgi-bin/config.cgi
# Configuración de GPIOs con edición de nombres/pares y trazas de depuración

# Cabecera HTTP
echo "Content-type: text/html"
echo ""

# Archivo de trazas
LOG="/tmp/config_debug.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') | REQUEST_METHOD=$REQUEST_METHOD CONTENT_LENGTH=$CONTENT_LENGTH" >> "$LOG"

log() {
  # Prefijo con fecha y hora
  echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$LOG"
}

# Comienza la traza
log "=== Nueva petición a config.cgi ==="
log "REQUEST_METHOD=$REQUEST_METHOD CONTENT_LENGTH=$CONTENT_LENGTH"

# Cargar configuración actual
if ! source /etc/gpio_config.sh 2>>"$LOG"; then
  log "ERROR: No se pudo cargar /etc/gpio_config.sh"
  echo "<p style='color:red'><b>Error:</b> no se pudo cargar /etc/gpio_config.sh</p>"
fi

# Función para decodificar application/x-www-form-urlencoded
urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }

# Procesar POST
if [ "$REQUEST_METHOD" = "POST" ]; then
  if [ -z "$CONTENT_LENGTH" ]; then
    log "ERROR: CONTENT_LENGTH vacío en POST"
    echo "<p style='color:red'><b>Error:</b> POST sin CONTENT_LENGTH.</p>"
  else
    read -n "$CONTENT_LENGTH" POST_DATA
    log "POST_DATA(raw)=$POST_DATA"

    # Crear archivo temporal
    TMP="/tmp/gpio_config_new.sh"
    {
      echo "#!/bin/bash"
      echo "# Archivo generado automáticamente por config.cgi"
      echo "R1=(${R1[@]})"
      echo "R2=(${R2[@]})"

      echo "declare -A PAIRS=("
      for P in "${R1[@]}"; do
        PAIR_RAW=$(echo "$POST_DATA" | sed -n "s/.*pair$P=\([^&]*\).*/\1/p")
        PAIR=$(urldecode "$PAIR_RAW")
        # Validación simple: debe ser numérico y estar presente
        if [[ -z "$PAIR" || ! "$PAIR" =~ ^[0-9]+$ ]]; then
          log "WARN: Par inválido para $P: '$PAIR_RAW' -> '$PAIR'"
        fi
        echo "  [$P]=$PAIR"
        echo "  [$PAIR]=$P"
        log "PAIR[$P]=$PAIR y PAIR[$PAIR]=$P"
      done
      echo ")"

      echo "declare -A NAMES=("
      for P in "${R1[@]}"; do
        NAME_RAW=$(echo "$POST_DATA" | sed -n "s/.*name$P=\([^&]*\).*/\1/p")
        NAME=$(urldecode "$NAME_RAW")
        # Si no llega nombre, mantener el existente para no perder datos
        if [ -z "$NAME" ]; then
          NAME="${NAMES[$P]}"
          log "WARN: Nombre vacío para $P; se conserva '${NAMES[$P]}'"
        fi
        # Escapar comillas
        NAME_ESCAPED=$(printf "%s" "$NAME" | sed 's/"/\\"/g')
        echo "  [$P]=\"$NAME_ESCAPED\""
        log "NAME[$P]='$NAME_ESCAPED'"
      done
      echo ")"

      # Generar nombres para R2 a partir de R1
      echo "for P in \"\${R1[@]}\"; do PAR=\${PAIRS[\$P]}; NAMES[\$PAR]=\"\${NAMES[\$P]} (R2)\"; done"
    } > "$TMP"

    # Comprobar que el temporal existe y tiene contenido
    if [ ! -s "$TMP" ]; then
      log "ERROR: No se creó o está vacío $TMP"
      echo "<p style='color:red'><b>Error:</b> no se pudo generar el archivo temporal.</p>"
    else
      ls -l "$TMP" >> "$LOG"
      head -n 20 "$TMP" >> "$LOG"

      # Intentar mover sin sudo (requiere permisos adecuados en /etc/gpio_config.sh o en /etc)
      if mv "$TMP" /etc/gpio_config.sh 2>>"$LOG"; then
        log "OK: /etc/gpio_config.sh actualizado"
        echo "<p style='color:green;font-weight:bold'>✅ Configuración actualizada</p>"
      else
        log "ERROR: Fallo al mover $TMP a /etc/gpio_config.sh (permisos)"
        echo "<p style='color:red'><b>Error:</b> no se pudo escribir en /etc/gpio_config.sh. Ajusta permisos:</p>"
        echo "<pre>sudo chown root:www-data /etc/gpio_config.sh
sudo chmod 664 /etc/gpio_config.sh</pre>"
      fi
    fi
  fi
fi

# Página HTML (formulario)
echo "<!DOCTYPE html>"
echo "<html><head><meta charset='UTF-8'><title>Configuración GPIO</title>"
echo "<style>table{border-collapse:collapse;width:90%}th,td{border:1px solid #ccc;padding:8px;text-align:center}th{background:#f7f7f7}input{width:95%}caption{font-weight:bold;margin-bottom:8px}</style>"
echo "</head><body>"
echo "<h1>Configuración de GPIOs</h1>"
echo "<p>Las etiquetas de R2 se generan automáticamente a partir de R1.</p>"

echo "<form method='POST'>"
echo "<table>"
echo "<caption>Editar nombres y pares</caption>"
echo "<tr><th>GPIO</th><th>Nombre</th><th>Grupo</th><th>Par (GPIO en R2)</th></tr>"

# Filtrar entrada para evitar HTML roto (solo visual; el guardado usa sed/urldecode)
html_escape() { printf "%s" "$1" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/"/\&quot;/g'; }

for P in "${R1[@]}"; do
  NAME_SHOW=$(html_escape "${NAMES[$P]}")
  PAIR_SHOW="${PAIRS[$P]}"
  echo "<tr>"
  echo "<td>$P</td>"
  echo "<td><input type='text' name='name$P' value='$NAME_SHOW'></td>"
  echo "<td>R1</td>"
  echo "<td><input type='number' name='pair$P' value='$PAIR_SHOW' min='0'></td>"
  echo "</tr>"
done

for P in "${R2[@]}"; do
  NAME_SHOW=$(html_escape "${NAMES[$P]}")
  PAIR_SHOW="${PAIRS[$P]}"
  echo "<tr>"
  echo "<td>$P</td>"
  echo "<td><input type='text' value='$NAME_SHOW' disabled></td>"
  echo "<td>R2 (auto)</td>"
  echo "<td>$PAIR_SHOW</td>"
  echo "</tr>"
done

echo "</table>"
echo "<br><input type='submit' value='Guardar cambios'>"
echo "</form>"

# Info de depuración accesible desde la página
echo "<h3>Depuración</h3>"
echo "<p>Consulta el log en: <code>/tmp/config_debug.log</code></p>"
echo "</body></html>"
