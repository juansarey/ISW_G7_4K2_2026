> **Clase:** 13/10/2026 | **Tema:** Práctico TDD: estrategias de testing y clases de equivalencia

> **ESTA CLASE ES IMPORTANTE, PORQUE ACA SE VE TODO LO QUE VA A ENTRAR AL PARCIAL RESPECTO AL PRACTICO**
# Estrategias de Testing
Un caso de prueba es el conjunto de pasos que defino para ejecutar una prueba. En las pruebas de aceptación la forma de redactar la prueba es genérica, no es especifica, ahora en los casos de prueba **SÍ** es especifica. Lo que hacemos es juntar toda la información importante para que alguien se ponga a ejecutar esto.

Entre las estrategias de testing tenemos:
- **Caja Negra:** Sabemos las entradas y las salidas, pero no que pasa en medio digamos. Se separan en *Partición de equivalencias* y *Análisis de valores limites* y las dos utilizan clases de equivalencias.
- **Caja Blanca:** Estático, defino entradas pero conozco como es el proceso para obtener las salidas. Se definen en base a los algoritmos que pueden tener el código.

### ¿Por que definimos Estrategias de Testing?
**Objetivo:** Que la cobertura de la prueba sea la optima y la mas eficiente, menos costo, y que abarque lo mayor posible. Mayor cobertura de prueba, con menor costo posible. 

Las técnicas de caja negra plantean una forma de poder definir las distintas pruebas que puedo hacer y cuál me conviene elegir de ese conjunto de pruebas.

### Clases de Equivalencia
**UNA CLASE DE EQUIVALENCIA ES UN CONJUNTO DE CASOS DE PRUEBA**, primero definimos las clases de equivalencia, y después agarramos UN caso de prueba por cada clase de equivalencia definida, lo importante es ***definir bien las clases de equivalencia***. Dentro de cada clase de equivalencia se definen **LÍMITES**. A veces no se pueden definir claramente pero en algunos casos sí.

>Ejemplo: Tenemos una CE que es "mayores de 18 años", bueno entonces en ese caso nuestro limite inferior va a ser 18, y el limite superior va a ser 100 (ponele), de esa forma definimos limites, y hacemos pruebas especificas para esa CE, por ejemplo probar ingresar 18,1 o 18,0001 o cosas por el estilo.

Cuando definimos las CE definimos las CE de ***ENTRADA Y LAS DE SALIDA***. Las de entrada son cuales son los **conjuntos de entradas** que yo espero, y como las puedo agrupar para decir *Bueno yo espero que estas se comporten de esta manera*, también **defino como espero que sean las salidas** (ejemplo: mensajes de error, mensajes de exito, etc...).

 Las CE tiene CONDICIONES EXTERNAS validas e invalidas, las que cumplen con la condición externa son validas, y las que no, son invalidas.
### BodyPainting
Hacemos una prueba de como seria un CE con el US: Confirmar pedido de pago con tarjeta de crédito (Pag. 72 de la guía de trabajo practico resuelta)

| CE               | CE Validas                                                  | CE Invalidas                                              |
| ---------------- | ----------------------------------------------------------- | --------------------------------------------------------- |
| Datos de cliente | e-mail + loguea                                             | No e-mail - No log                                        |
| Domicilio envio  | Registrado                                                  | N.E. / N.S.                                               |
| Carrito          | Compra kits con stock                                       | Compra producto sin stock                                 |
| TC - Nro         | Numero entero de 16 dígitos                                 | S/N - Numero no valido                                    |
| TC - Titular     | Cadena de caracteres                                        | Sin Datos (S/D)                                           |
| TC - Fecha       | Fecha valida en el formato <br>correspondiente (DD/MM/AAAA) | S/D<br>Fecha vencida<br>Formato no valido                 |
| TC - CVV         | Numero entero de 3 caracteres                               | S/D<br>Cadena de string<br><3 caracteres<br>>3 caracteres |

Los datos de la primera columna son CONDICIONES EXTERNAS, porque representan la regla, variable, campo o parámetro que se pone a evaluar. Lo que ponemos como "válidas" o "inválidas" son CLASES DE EQUIVALENCIA. 

---
### Clases de equivalencia de SALIDA

|            | Validas           | Invalidas      |
| ---------- | ----------------- | -------------- |
| Msj. Exito | "Pago confirmado" | "No hay stock" |
|            |                   |                |

---
ID: 
Nombre CP:
Prioridad: Alta/Media/Baja
Clases de Equivalencia: (número)
Precondiciones:

Ejemplo de precondiciones: El cliente Joa Robles se encuentra registrado con el mail joarobles@gmail.com, el cliente (Joa Robles) tiene domicilio Humberto Primo blabla registrado, el producto X, con X cantidad y X precio se encuentra cargado en el carrito, bla bla bla

> Bueno la verdad que no entendi mucho pero bueno, algo vamos a hacer

# Taxi Mobile

**Consigna:** Definir las clases de equivalencia para la *US: Ver mapa de taxis*

| CE                   | CE Validas                                                                                 | CE Invalidas                                                            |
| -------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Estado Taxi          | -Libre<br>-Ocupado<br>-Solicitado<br>-Fuera de servicio<br>-Ninguna (No selecciona estado) | Cualquier otro<br>                                                      |
| Sistema de Ubicación | Sistema de ubicacion habilitado en taxis                                                   | Sistema de ubicacion no habilitado en taxis                             |
| Barrio               | -Barrio existente<br>-No ingresar barrio                                                   | Barrio no existente                                                     |
| Chapas               | -Formato AAA 000<br>-Formato AA 000 AA<br>-S/D                                             | Formato invalido                                                        |
| Usuario logueado     | -Usuario logeado con permisos de rol "Administrador" en la central                         | -Usuario no logeado<br>-Usuario logeado sin permisos de "Administrador" |
En el CE de Estado taxi hace mas referencia al *Estado del filtro*, ósea no se refiere a que estado puede tener el taxi si no en que opción se encuentra el filtro del mapa. No hace falta enroscarse en cosa estilo "Puedo ingresar un numero o no?", es mejor dejarlo simple y bien que enroscado y mal.

| CES               | Valido                                                                                                                                  | Invalido |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Color del taxi    | Verde<br>Amarillo<br>Rojo<br>Negro                                                                                                      |          |
| ID del pasajero   | Nombre, apellido y celular                                                                                                              |          |
| Hora del viaje    | - Formato valido de hora (hh:mm)<br>- Formato valido de dia (dd/mm/aaaa)<br>- Tanto la fecha como la hora tienen que ser >= a la actual |          |
| Precio            | Precio decimal > 0                                                                                                                      |          |
| Matricula         | Matricula del taxi en formato correspondiente                                                                                           |          |
| Mensajes de error |                                                                                                                                         |          |
Se segmenta lo mas posible la info para que después coincida en las precondiciones (o algo así)

ID: 001
Nombre CP: Taxis libres para un barrio
Prioridad: Alta
Clases de Equivalencia: 5
Precondiciones:
- Mínimo un taxi en el mapa
- Barrio libre para buscar
- Usuario registrado como pasajero


