> **Clase:** 25/08/2026 | **Tema:** Requerimientos ágiles y User Stories

#### Req Agiles
Son formas de identificar y gestionar los requerimienots en ambientes agiles con procesos empiricos. Un CU es un req en ambiente definido, es diferente de un req agiles como puede ser una **historia de usuario**, product backlog, spike (asociado a req no funcionales)

> spike es un item de backlog, es par reservar un espacio de tiempo en un sprint o en un tiempo determinado

#### Product Backlog
NO esta compuesto solo por US, puede estar compuesto por spikes, stories, etc... lso candidatos de item de un backlog son por ejemplo: tarea, US, epica, tema. 

**!! IMPORTANTE !!** 
- no olvidar poner el valor de neogcio a la hora de hacer una US
- leer estimaciones agiles (poker planing), y traer impresas las cartas para estimar (o algo para hacer la actividad sum like that)

#### Modelo Invest y US
Una US esta compuesta por una card, donde tengo la frase verbal, los puntos de historia, y los criterios de confirmación. Del otro lado de la tarjeta escribo las pruebas de aceptación de usuario (casos de prueba de aceptación de usuario). Todo lo que esta en la carta se agrupa en el MODELO INVEST. Cuando consideramos que una historia del PB esta lista para formar parte del sprint, lo catalogamos como "READY".

I - independiente
N - negociable (con el product owner)
V - valuable (puedo determinar cual es el valor de negocio)
E - estimable (podemos estimar complejidad, demoras, etc..)
S - small 
T - testeable

Despues de READY puede pasar a DONE y de ahi se puede dividir entre Output y Outcome. El Output es mas tipo terminar la user y como la parte mas tecnica me parece. Outcome es el resultado que produce la user que termine, esta mas relacionado con el valor de negocio. 

### Caso body-painting
Acordate que una US se hace así:
Como [nombre del rol],
yo puedo [actividad]
de forma tal que [valor de negocio que recibo]

**Roles:**
- Cliente
- Vendedor
- Admin. de productos

1 producto = 1 pincel
1 kit = 2 pinceles, 3 acrilicos, 1 esponja

se envían **mails** para ir avisando algunas cosas:
- confirmación de pago
- confirmación de pedido
- mail para numero de seguimiento de pedido
  
Además pueden haber cupones de descuento
Hay gestion de reclamos de clientes (en caso que el producto no coincida con lo pedido, o este en mal estado)

¿Como hago para identificar las US? Primero me paro en cada rol y pienso que necesita hacer ese rol y que genere valor de negocio, cunado hago la US no hace falta que este completa, sirve la frase nomas, despues se puede completar.

**Us Cliente:**
- Registrarse (darse de alta)
- Visualizar productos
- Armar carrito de compras
- Registrar domicilio de entrega
- Registrar pago (*Acá esta el valor de negocio, ¿en que formas lo puedo hacer? eso tengo que pensar*); dividir las US en forma VERTICAL no HORIZONTAL. *Aca podemos dividir en varias cosas como confirmar pago con MP, confirmar pago con TC, confirmar pago con efectivo, etc..*
- Recibir mail de confirmación de pedido
  
#### US: Confirmar pago con efectivo
Como *==Cliente==* quiero *==Confirmar el pago/pedido pagando en efectivo==* para *==Adquirir el producto==*

**Criterios de aceptación:**
- Que se aplique el descuento
- Que el cliente tenga cuenta
- Que tenga stock
- Que no se puedan combinar métodos de pago

**Pruebas:**
- Probar *{frase verbal} {escenario}*. (Pasa/Falla)

### TP Evaluables/Practico1/Req Agiles - User Stories
**Us Cliente:**
- Como cliente yo puedo ==registrar el tipo de gasto== de forma tal que organizo mis gastos  
- Como cliente yo puedo ==registrar gasto==   
- Como cliente yo puedo ==visualizar mis gastos== de forma tal que puedo ver mis gastos
- Como cliente yo puedo ==iniciar sesión== de forma tal que puedo ingresar a la pagina
- Como cliente yo puedo ==cerrar sesión== de forma tal que puedo ingresar a la pagina
- Como cliente yo puedo ==registrar usuario== de forma tal que puedo ingresar a la pagina
- Como cliente yo puedo ==filtrar por tipo de gasto== de forma tal que visualizo solo por tipo
- Como cliente yo puedo ==filtrar por responsable de gasto== de forma tal que visualizo solo por responsable
- Como cliente yo puedo ==filtrar por rango de montos== de forma tal que visualizo solo por rango
- Como cliente yo puedo ==cambiar el criterio de ordenamiento== de forma tal que visualizo de manera ordenada

#### US: Filtrar gastos (y ordenarlos)

