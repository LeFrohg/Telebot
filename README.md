# Telebot
Bot de telegram sencillo que será alojado y ejecutado en RaspbianOS

El bot está encargado de manipular un servomotor MG90S.
El bot permite: 
* Ejecutar una sencilla rutina. Posiciona el servomotor en un estado default y lo cambia a un ángulo de apertura previamente establecido,      espera un tiempo y vuelve la posición del servomotor al estado default
* Establecer el ángulo en el que se posicionará el servomotor, tanto al energizar como en estado de reposo
* Establecer el ángulo de apertura, siendo posible los 180° o bien 360° si es que se manipuló físicamente el servomotor
* Establecer el tiempo medido en segundos que tardará el servomotor en abrir y cerrar el ángulo de apertura
* Consultar los valores almacenados (con permanencia en caso de corte energético)
* Debido al OS al que está enfocado, permite agregar nuevas redes wifi
* Identificar el cliente con el que está interactuando, permitiendo que sólo el cliente definido haga uso y manipule el servomotor

Inconvenientes:
* La ecuación usada para obtener los grados fue establecida calibrando el servomotor en concreto. Una alta probabilidad de que falle en       caso de usar un servomotor distinto
* Imposible elejir manualmente a que red wifi se va a conectar
* El SSID y password de la red wifi que será añadida no admiten espacios en blanco
* Al añadir una nueva red wifi, se conectará a ella de forma inmediata
* No contempla el caso de ingresar una red con SSID o password con errores (es posible que el bot crashee de ocurrir ésto)
* No se contemplan errores tipográficos en los comandos enviados por el cliente. Concretamente en los argumentos.
* No se contempla la recepción de comandos desconocidos
