#!/bin/bash
# uninstall.sh - Desinstalador del sistema de control de antenas
# Autor: EA7KE

set -e  # detener si hay error

echo "=== Desinstalación del sistema de control de antenas ==="

# 1. Parar servicios relacionados
echo "[1/6] Deteniendo pigpio y servicio gpio-reset..."
sudo systemctl stop pigpiod || true
sudo systemctl disable pigpiod || true
sudo systemctl stop gpio-reset.service || true
sudo systemctl disable gpio-reset.service || true

# 2. Desactivar sitio de Apache
echo "[2/6] Desactivando sitio de Apache..."
sudo a2dissite antenna.conf || true
sudo rm -f /etc/apache2/sites-available/antenna.conf
sudo systemctl reload apache2

# 3. Eliminar directorios instalados
echo "[3/6] Eliminando directorios..."
sudo rm -rf /usr/lib/cgi-bin/antenna
sudo rm -rf /var/www/html/antenna
sudo rm -rf /usr/local/bin/antenna
sudo rm -rf /etc/antenna
sudo rm -rf /usr/share/doc/antenna

# 4. Eliminar servicio gpio-reset
echo "[4/6] Eliminando unidad systemd gpio-reset..."
sudo rm -f /etc/systemd/system/gpio-reset.service
sudo systemctl daemon-reload

# 5. Limpiar logs de Apache relacionados
echo "[5/6] Eliminando logs de Apache..."
sudo rm -f /var/log/apache2/antenna_error.log
sudo rm -f /var/log/apache2/antenna_access.log

# 6. Mensaje final
echo "[6/6] Desinstalación completada ✅"
echo "El sistema de control de antenas ha sido eliminado."
