#!/bin/bash
echo "Content-type: application/json"
echo ""

# Ejecutar el script
/bin/bash /usr/local/bin/antenna/gpio_reset_R2.sh

# Respuesta mínima en JSON
echo '{"status":"ok"}'
