#!/bin/bash
# Instalador del sistema de control de antenas
# Autor: EA7KE

set -e  # detener si hay error

echo "=== Instalación del sistema de control de antenas ==="

# 1. Dependencias
echo "[1/6] Instalando dependencias..."
sudo apt update
sudo apt install -y apache2 php pigpio

# 2. Directorios destino
echo "[2/6] Creando directorios destino..."
sudo mkdir -p /usr/lib/cgi-bin/antenna
sudo mkdir -p /var/www/html/antenna
sudo mkdir -p /etc/antenna
sudo mkdir -p /usr/local/bin/antenna
sudo mkdir -p /usr/share/doc/antenna

# 3. Copiar archivos
echo "[3/6] Copiando archivos..."
# CGI
sudo cp -r cgi-bin/* /usr/lib/cgi-bin/antenna/
# Web
sudo cp -r html/antenna/* /var/www/html/antenna/
# Scripts
sudo cp -r bin/* /usr/local/bin/antenna/
# Configuración
sudo cp -r etc/* /etc/antenna/
# Documentación
# sudo cp -r antenna/docs/* /usr/share/doc/antenna/ || true

# 4. Permisos
echo "[4/6] Ajustando permisos..."
# Scripts → root
sudo chown -R root:root /usr/local/bin/antenna
sudo chmod +x /usr/local/bin/antenna/*
# CGI y web → www-data
sudo chown -R www-data:www-data /usr/lib/cgi-bin/antenna
sudo chown -R www-data:www-data /var/www/html/antenna
sudo chmod -R 755 /usr/lib/cgi-bin/antenna
sudo chmod -R 755 /var/www/html/antenna
# Configuración → root
sudo chown -R root:root /etc/antenna

# 5. Configuración de Apache
echo "[5/6] Configurando Apache..."
APACHE_CONF="/etc/apache2/sites-available/antenna.conf"

sudo tee $APACHE_CONF > /dev/null <<EOL
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html/antenna

    <Directory /var/www/html/antenna>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/antenna/
    <Directory "/usr/lib/cgi-bin/antenna">
        AllowOverride None
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/antenna_error.log
    CustomLog \${APACHE_LOG_DIR}/antenna_access.log combined
</VirtualHost>
EOL

# Activar sitio y reiniciar Apache
sudo a2ensite antenna.conf
sudo systemctl reload apache2

# 6. Servicios
echo "[6/6] Activando pigpio..."
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

echo "=== Instalación completada ✅ ==="
echo "Web: http://<IP-de-tu-RPi>/"
echo "CGI: http://<IP-de-tu-RPi>/cgi-bin/"
