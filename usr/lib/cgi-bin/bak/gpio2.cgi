

#!/bin/bash
echo "Content-type: text/html"
echo ""

# Apagar todos los GPIOs (2 a 7 en este ejemplo)
for PIN in 2 3 4 5 6 7; do
  /usr/bin/pigs w $PIN 0
done

# Encender solo el GPIO2
/usr/bin/pigs w 2 1

# Generar la página R1.html dinámica
echo "<!DOCTYPE html>"
echo "<html><head><meta charset=\"UTF-8\"><title>Panel R1</title></head><body>"
echo "<h1>Control de GPIOs (R1)</h1>"

for PIN in 2 3 4 5 6 7; do
  STATE=$(/usr/bin/pigs r $PIN)
  if [ "$STATE" -eq 1 ]; then
    COLOR="green"
  else
    COLOR="lightgray"
  fi
  echo "<form action=\"/cgi-bin/gpio${PIN}.cgi\" method=\"get\" style=\"display:inline;\">"
  echo "<button type=\"submit\" style=\"background-color:${COLOR};width:100px;height:50px;\">GPIO${PIN}</button>"
  echo "</form>"
done

echo "</body></html>"
