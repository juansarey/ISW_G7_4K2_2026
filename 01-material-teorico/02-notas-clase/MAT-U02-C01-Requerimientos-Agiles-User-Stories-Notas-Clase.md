> **Clase:** 21/08/2026 | **Tema:** Requerimientos ágiles y User Stories

**Material importante de la clase: Diapositiva numero 3 de la uv**
## Plan de configuración

Forma parte de los items de configuración

Las líneas bases que contienen código se llaman lineas base operacionales, las que no contienen codigo se llaman linea base de especificacion

**Linea base Operacional:** contiene codigo
**Linea base de Especificación:** contiene requerimientos, documentacion, etc.. (todo lo que no es codigo)

Tipo de info vinculada al estado --> **TRAZABILIDAD DE LOS CAMBIOS**
Uno mantiene el control de los cambios para rastrear cuando cambio algo o ver la evolucion de algo en caso que alguien necesite verlo.

¿Que es lo que se le controla mas ESTRICTAMENTE a los cambios?
Las lineas base se les controla el cambio, el comite de control de cambios interviene cunado queres cambiar una linea base, y despues controlar si esa linea base cambio conforme a lo autorizado o no. Lo que empieza a tener control es cuando marcaste una linea base.
Hasta que conformas una linea base, los items de config. tenemos la libertad de administrarlos y el contorl de cambios lo hace la herramienta de versionado (git). 

### Auditorias de configuración
Se planifican en el plan de gestion de configuración (donde guardamos las decisiones de como mantener el plan), se planifican con **MOMENTOS**. Ej: "Vamos a hacer una auditoria al final de cada WF", "Vamos a hacer una auditoria cuando la idea este validada". Tipos de auditoria de configuracion: Fisica y Funcional.

Las auditorias se hacen al repo pero no a todas las lineas del repo, se hace a **UNA LINEA BASE**
Primeor se hace la auditoria FISICA, despues la FUNCIONAL. 

Primera pregunta de la auditoria funcional --> **¿Esta disponible el reporte de la auditoria Física?**

1. *Proceso* --> Definidos y Empíricos
2. *Proyecto <-- Personas*
3. *Producto*

**Agilismo: Pensamiento, Filosofía**
**Agile != Scrum !!! Scrum es el FRAMEWORK**
# Requerimientos en ambientes agiles

Dos formas de controlar los procesos:
1. **Procesos Definidos:** Los que vemos en años anteriores (PUD, RUP). Fracasan despues de un tiempo. La gente le echaba la culpa al proceso cunado el proyecto fracasaba. Debido a este fracaso es que nace el AGILISMO. 
2. **Procesos Empíricos:** Abordaremos estos proceso en la materia con dos filosofias, agil y lean. Ambos trabajan bajo la concepcion de los procesos empiricos.
   Lean --> kanban
   Agile --> Scrum

### Empirismo
Ciclos cortos para ver que no demoremos en lo que hacemos, el empirismo se trata de aprender de la experiencia, de la prueba y el error, "Se hace camino al andar" - Meles jua
#### Pilares del empirismo
- **Inspección:** La inspección puede realizarse para el producto, procesos, aspectos de personas, prácticas y mejoras continuas. Se realiza por todo el equipo y permite detectar varianzas o problemas potencialmente indeseables
- **Adaptación:** Se trata de la mejora continua, es la capacidad de adaptarse en función de los resultados de la inspección. Nos permite hacer ajustes en aspectos del proceso que se desvían fuera de los límites o si el producto es inaceptable.
- **Transparencia:** Transformar el conocimiento que cada miembro del equipo tiene implícito en conocimiento explícito, es decir, que pase a formar parte del conocimiento de todo el 33 equipo. Esto ayuda a que los procesos empíricos puedan fluir y generar esa experiencia necesaria para que el equipo evolucione. (no fingir demencia, no mentir, no guardarnos info.)

### Pensamiento Agil
Ocurre desde las bases, programadores se revelan contra las malas experiencias de usar procesos definidos, creado en Utah en 2001, se juntaron los actuales creadores de scrum y firmaron el **"Manifiesto agil"** es como la descripcion de la filosofia agil, tiene **4 valores y 12 principios.** 
#### 4 valores
1. Valoramos mas las interacciones entre las personas que respetar procesos y herramientas
2. Valoramos mas el sw funcionando que tener documentación detallada y extensa
3. Valoramos mas colaborar con el cliente y trabajar de forma conjunta que estar negociando contratos y abogados y bla bla
4. Valoramos mas dar respuestas a los cambios que aferrarnos a el cumplimiento de un plan solo porque lo escribimos nosotros

¿Qué solemos decir mal o confundir? NO dice que NO hay que documentar o NO hay que especificar o eso, nomas pone los valores

> Otros framework para investigar --> ShapeUp, XP, ATDD, Crystal

# Requerimientos Agiles / User Histories
**==HU:** Es la técnica para identificar requerimientos

Es importante aclarar QUE es un requerimiento agil antes de explicar que es una HU
La base del agilismo es SW funcionando por sobre la documentación, y uno de los principios que habla sobre eso dice que hay que satisfaces al cliente con entregas frecuentes y tempranas de SW funcionando. Tiene que ser funcional, no tiene que cubrir TODAS las funcionalidades planeadas, pero si las de un "Sprint" digamos.

El agilismo dice "Vamos a partir de una visión del producto que la trae el PO, que es el representante del negocio, el sabe lo que quiere, y lo que necesita" (necesidad >> querer)

Elemento calve del agilismo --> Trabajar con el concepto de valor (valor de negocio)
No alcanza con "hacer SW", tenemos que hacer SW que le sirva la negocio
> Vamos a trabajar con una nueva versión de SCRUM que hace énfasis en esto

Se cumple la regla de "Pareto" --> el 20% de las acciones genera el 80% de los resultados
EL 7% de un producto se usa SIEMPRE, en cambio el 45% de un producto no se usa NUNCA

#### Product Backlog
Es una "bolsa" de una caja, donde voy tirando las cosas que necesito hacer del producto, tecnicamente es el contenedor de los "items product backlog", cada item es cada cosa que quiero que haga el producto. La forma mas común que sugieren los FW, es que esos items de product backlog sean HU. 
Se ordena según prioridad: +arriba --> +prioridad ; +abajo --> -prioridad
> El concepto de "líder de proyecto" no existe en el agilismo

Dominio del problema:
1. Requerimientos de negocio
2. Requerimientos de usuario
Dominio de la solución:
3. Requerimientos de SW
# User Stories (HU) (Historias de usuario)
El PO nos va a contar una necesidad, una HU es una descripcion CORTA de una necesidad del usuario. Existen en el Dominio del problema.
> ¿Donde estan los CU? son req de SW, osea forman parte del dominio de la solución.  

**Partes de una US: (las 3 C)**
- Tarjeta (Card)
- Conversación (Conversation)
- Confirmación (confirmation)

En base a eso podemos decir entonces que la parte mas importante de una HU es la conversación.
El PO es el que escribe las HU. 
#### Sintaxis de las HU (Tarjeta, Card)
Como <nombre del rol>,
	Representa quien esta realizando la acción o quien recibe el valro de la actividad
yo puedo <actividad>
	Representa la acción que realizara el sistema
de forma tal que <valor de negocio que recibo>
	Comunica porque es necesaria la actividad

En ingles --> As **who**, I want **what**, so that's **why**

	

