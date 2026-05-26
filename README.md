# PYDT-Simulacion

Este proyecto es una simulación de chat muy básico.

Tiene 3 programas:

server.py -> el servidor, que coordina todo
client1.py -> primer cliente
client2.py -> segundo cliente

El servidor:

- Espera que los clientes se conecten.
- Revisa el login (usuario y clave).
- Recibe mensajes de un cliente.
- Pasa ese mensaje al otro cliente.
- Responde al que envió si se entregó o no.

Cada cliente:

- Se conecta al servidor.
- Pide usuario y contraseña por la consola.
- Si el login es correcto, permite escribir mensajes.
- Envía mensajes al otro cliente.
- Muestra en pantalla:
    si el mensaje se entregó CONFIRMED
    si recibió un mensaje RECIBIDO ...

    
Por ahora, los datos de login que sirven son:
cliente1 con clave 1234
cliente2 con clave 1234

Para probar: 
Abrir 3 terminales:

- python3 server.py
- python3 client1.py
- python3 client2.py

Luego escribir un mensaje en client1 y este llega en client2.
