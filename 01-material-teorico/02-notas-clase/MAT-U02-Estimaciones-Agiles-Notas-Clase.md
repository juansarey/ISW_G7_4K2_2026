> **Clase:** 08/09/2026 | **Tema:** Estimaciones ágiles (Planning Poker) y User Stories

**Estimación Relativa:** Comparamos el tamaño, complejidad y riesgo de una historia contra otra historia base, en lugar de calcular horas

#### ¿Como se estima en poker planning?
1. Entre todos los miembros del equipo se elige la US canonica
2. Cada miembro le da un valor a la US canonica (le puedo dar 1 valor, eventualmente 2, en caso de que una US este compuesta por US mas chicas)
3. Se da vuelta la carta de cada uno con el valor que le asigno a la US canonica y despues se debate para dejar un valor

Bueno hay algo de una user storie asi que lo hago aca de una

### US01: Confirmar propuesta de venta
_"Como vendedor quiero registrar mi respuesta a una propuesta de venta para que el negocio sepa que hacer con mis prendas"_

##### **Criterios de Aceptación:**
- El vendedor debe estar registrado
- Visualizar correctamente la información de las prendas, con fecha, listado de prendas con su nombre, categoria, estado, precio sugerido y ganancia
- Para cada prenda hay 3 opciones: "vender", "retirar", "donar"
- Se debe marcar una opción de las tres SI O SI entre "vender", "retirar", "donar" 
- Visualizar listado de prendas que no fueron seleccionadas para comprar en este caso
- Permitir elegir cuales prendas vender
- Permitir definir que hacer con las prendas que no se van a vender
- Las opciones anteriores son sobre LAS PRENDAS SELECCIONADAS por el supuesto comprador
  
> Es importante aclarar en estos casos por ejemplo "Visualizar correctamente la información de las prendas, con fecha, listado de prendas con su nombre, categoría, estado, precio sugerido y ganancia" es importante poner TODOS los datos que se tienen que mostrar

##### **Casos de Prueba:**
- Probar elegir prendas para vender y continuar = PASA
- Probar no elegir ninguna prenda para vender y continuar = NO PASA
- Probar no definir que hacer con las prendas que no vas a vender = NO PASA
- Probar elegir prendas para vender y seleccionar "Retirar" para las no vendidas = PASA
- Probar elegir prendas para vender y seleccionar "Donar" para las no vendidas = PASA

> Probar [frase verbal - acción] [lo que vamos a probar] + PASA/NO PASA

Eso lo mando el ayudante de la profe y la profe lo valido así que es importante

### Estimaciones
##### US CANONICA: Registrar usuario por mail
##### US Confirmar propuesta de venta (3)
**Complejidad:** Media, ya que no requiere validaciones complejas y requiere de un solo campo select.
**Esfuerzo:** No se requiere tanto esfuerzo a que es una unica bandeja con pocas opciones, y baja cantidad de logica de negocio. 
**Incertidumbre:** Nula. El requerimiento es claro y no hay duda tecnica.
##### US Enviar prendas para vender (5)
**Complejidad:** 
**Esfuerzo:**
**Incertidumbre:**
##### US Enviar prendas para vender (5)
**Complejidad:** 
**Esfuerzo:**
**Incertidumbre:**