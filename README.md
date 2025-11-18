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

La configuración de antenas se define en `gpio.conf`.  
Cada antena está asociada a un pin GPIO de R1 y emparejada con un pin de R2.

| Antena        | GPIO R1 (BCM) | GPIO R2 (BCM) | Pin físico R1 | Pin físico R2 |
|---------------|---------------|---------------|---------------|---------------|
| 10m Yagi      | 2             | 8             | Pin 3         | Pin 24        |
| 15m Yagi      | 3             | 9             | Pin 5         | Pin 21        |
| 20m Yagi      | 4             | 10            | Pin 7         | Pin 19        |
| 40m Dipolo    | 5             | 11            | Pin 29        | Pin 23        |
| 80m Dipolo    | 6             | 12            | Pin 31        | Pin 32        |
| 160m L Inv    | 7             | 13            | Pin 26        | Pin 33        |

👉 Los números de **GPIO (BCM)** son los que usa el sistema.  
👉 Los números de **Pin físico** corresponden al conector de 40 pines de la Raspberry Pi.  
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
