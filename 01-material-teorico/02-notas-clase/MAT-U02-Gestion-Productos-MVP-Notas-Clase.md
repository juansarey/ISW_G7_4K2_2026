> **Clase:** 01/09/2026 | **Tema:** MVP (práctico)

1. **Hipótesis:** A partir de esa hipótesis definir..
2. **Alcance:** Este alcance va asociado a un conjunto de US (solo nos quedamos con las US que van a ser parte de ese MVP) --> Solamente frase verbal
3. **Fuera de alcance:** Definir que no es parte de este MVP

En el parcial --> Justificar a través de una hipótesis, justificar US, definir que queda fuera de alcance y listar las US que forman parte del MVP (no te piden identificar roles, o etc.. peor sugieren hacerlo para lograr un buen resultado)
## **Eco Harmony Park**
### Listado de US:
1. Consultar horarios de alimentación disponible
2. Filtrar horarios de alimentación por fecha
3. Visualizar mapa estatico del parque
4. Registrar cuenta de visitantes
5. Registrar compra de entradas al parque (con tarjeta o efectivo)
6. Inscribirse a actividades de capacidad limitada
7. Configurar notificaciones de horarios de alimentacion
8. Visualizar de ubicación en mapa en tiempo real
### MVP
#### Hipótesis
Se debe desarollar un MVP del sistema para Eco Harmony Park que cumpla con el listado de US seleccionados para esta primer versión del sistema. No contempla funcionalidades de administración y gestino de actividades, horarios, mapa, etc.. Va a cubrir los flujos principales que aportan valor al usuario/cliente. Haciendo foco en el registro de usuario, la compra de entradas con tarjeta de debito/credito como medio de pago, y la inscripción a actividades con capacidad limitada. No se contempla el método de pago efectivo en este MVP porque se considera que se debe resolver con pruebas fidedignas presenciales en el predio de Eco Harmony Park.

> Lo importante es demostrar que es lo que queremos probar con esta aplicación. La hipótesis
>  es POR QUE quiero construir esto. Tengo que declarar a QUIEN el voy a mejorar la experiencia.
>  **PRO-TIP:** Es mejor hacer foco en el usuario/cliente en el MVP.
#### Alcance
1. **US04: Registrar cuenta de visitantes**
   "Como cliente yo puedo registrar mi cuenta de forma tal que puedo ingresar al sistema con mis datos personales"
2. **US05: Registrar compra de entradas al parque (SOLO tarjeta)**
   "Como cliente yo puedo registrar la compra de entradas mediante tarjeta de credito/debito de forma tal que puedo pagar mediante la aplicación"
3. **US06: Inscribirse a actividades de capacidad limitada**
   "Como cliente yo puedo inscribirse a actividades de forma tal registro mis datos en cada actividad que desee y tenga capacidad"
4. **US03: Visualizar mapa estático del parque** 
   "Como cliente yo puedo visualizar el mapa estático del parque de forma tal que puedo ver el mapa para ubicarme dentro del mismo y tener mas información del parque"
5. **US01: Consultar horarios de alimentación disponible**
   "Como cliente yo puedo consultar horarios de alimentación disponible de forma tal que reviso los horarios para poder gestionar mi tiempo en la visita"
#### Fuera de alcance
1. ==US07: Configurar notificaciones de horarios de alimentación==
2. ==US08: Visualizar de ubicación en mapa en tiempo real==
3. ==US02: filtrar horarios de alimentación por fecha==
#### US: Registrar compra de entrada al parque (COMPLETO)
"_Como cliente yo quiero comprar entradas para obtener acceso al parque._"
##### Criterios de aceptación:
- El visitante debe estar registrado
- Un visitante no puede comprar mas de 10 entradas
- Se puede pagar en efectivo en boletería o con tarjeta con pasarela de MercadoPago
- Las entradas serán enviadas junto con una notificación de confirmación por mail
- Debe ingresar FV, cantidad de entradas y edades
- Debe ser una fecha donde esta abierto el parque
- Debe ser de una fecha igual o posterior a al actual
##### Casos de prueba:
- Probar comprar una entrada ingresando una fecha anterior a la actual = FALLA
- Probar comprar mas de 10 entradas = FALLA
- Probar comprar menos de 1 entrada = FALLA

> **SINTAXIS OBLIGATORIA:** Probar _frase verbal_ 
> Lo importante es poner a prueba los aspectos generales del sistema, entiendo que no tanto sobre el codigo si no mas bien sobre el concepto del dominio del problema