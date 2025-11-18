Sistema de control de conmutador de antenas para Raspberry Pi.  
Permite seleccionar diferentes radios mediante botones físicos conectados a los pines GPIO y controlar relés desde una interfaz web.

---

## 🚀 Pasos previos en Raspberry Pi

1. Descargar e instalar **Raspberry Pi OS Lite** desde la web oficial.  
   - Grabar la imagen en la tarjeta SD con `Raspberry Pi Imager` o `dd`.  
   - Configurar red y acceso SSH si se desea.

2. Actualizar el sistema:
   ```bash
   sudo apt update
     ```
     ```bash
   sudo apt upgrade -y
   ```

3. Instalar dependencias necesarias:
   ```bash
   sudo apt install -y git apache2 php pigpio
   ```

---

## 📂 Instalación del proyecto

Clonar el repositorio y ejecutar el script de instalación:

```bash
git clone https://github.com/ea7ke/antenna-switch-control.git
```
```bas
cd antenna-switch-control
```
```bas
chmod +x install.sh uninstall.sh
```
```bas
sudo ./install.sh
```

Para desinstalar:

```bash
sudo ./uninstall.sh
```

---

## 🎛️ Asignación de pines GPIO

Cada botón físico de radio está conectado a un pin GPIO de la Raspberry Pi.  
La configuración actual es:

| Radio | Botón | GPIO (BCM) | Pin físico |
|-------|-------|------------|------------|
| Radio 1 | Botón 1 | GPIO 17 | Pin 11 |
| Radio 2 | Botón 2 | GPIO 27 | Pin 13 |
| Radio 3 | Botón 3 | GPIO 22 | Pin 15 |
| Radio 4 | Botón 4 | GPIO 23 | Pin 16 |
| Radio 5 | Botón 5 | GPIO 24 | Pin 18 |
| Radio 6 | Botón 6 | GPIO 25 | Pin 22 |

👉 Estos pines se pueden modificar en el archivo de configuración (`/etc/antenna/gpio.conf`).

---

## ⚙️ Configuración de Apache

El script `install.sh` crea un sitio en `/etc/apache2/sites-available/antenna.conf` y lo activa automáticamente.  
La interfaz web queda disponible en:

```
http://<IP-de-tu-RPi>/
```

Los scripts CGI se ejecutan desde:

```
http://<IP-de-tu-RPi>/cgi-bin/
```

---

## 🖼️ Esquema de conexión

![Esquema GPIO](docs/gpio-diagram.png)

*(Añade un diagrama en `docs/gpio-diagram.png` para mostrar la conexión de botones a GPIO y relés.)*

---

## ✅ Estado del sistema

- Archivos web: `/var/www/html/antenna`  
- Scripts CGI: `/usr/lib/cgi-bin/antenna`  
- Scripts de control: `/usr/local/bin/antenna`  
- Configuración: `/etc/antenna`  
- Documentación: `/usr/share/doc/antenna`  

---

## 📜 Créditos

Proyecto desarrollado por **EA7KE** 
