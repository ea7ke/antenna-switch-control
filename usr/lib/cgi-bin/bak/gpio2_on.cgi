#!/bin/bash
echo "Content-type: text/html"
echo ""
echo "<html><body>"
sudo -u www-data /usr/bin/pigs w 2 1
echo "<h2>GPIO2 encendido</h2>"
echo "<a href=\"/index.html\">Volver</a>"
echo "</body></html>"
