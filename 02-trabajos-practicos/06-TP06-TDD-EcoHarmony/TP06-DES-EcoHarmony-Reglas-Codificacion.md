# Reglas de codificación y pruebas — TP6 EcoHarmony Park


**Alcance:** User Story «Comprar entradas».  
**Destinatarios:** integrantes del equipo y asistentes de inteligencia artificial.  
**Estado:** versión inicial para adoptar en el repositorio y contrastar con las reglas de estilo elegidas en el TP2.


## 1. Propósito y fuentes


Mantener una implementación coherente, comprensible y verificable, aunque las personas utilicen distintas herramientas de IA.


Las fuentes del trabajo son:
- La consigna de la cátedra, especialmente TP2 y TP6.
- La definición de la User Story del grupo.
- Las reglas de estilo seleccionadas en el TP2.
- El entregable de decisiones de diseño y casos C01–C28.
- Los acuerdos de dominio y el contrato de implementación registrados en el repositorio.


Las reglas de este archivo complementan las del TP2. Si existe una contradicción, documentarla y resolverla con el equipo; ninguna persona o IA debe adoptar una solución diferente de manera aislada. No atribuir a la cátedra decisiones adicionales del grupo.


## 2. Tecnologías y dependencias


- Implementar la lógica de compra en Python.
- Utilizar pytest para los tests del proyecto. Registrar el cambio respecto de unittest, propuesto inicialmente en el entregable.
- Mantener una sola configuración compartida de Python y dependencias, con las versiones efectivamente verificadas.
- Usar un entorno virtual por integrante. Excluirlo del control de versiones.
- Incorporar dependencias cuando exista una necesidad concreta y documentar su uso.
- La propuesta de interfaz es Tkinter; cualquier cambio de tecnología se acuerda y registra para todo el equipo.


## 3. Convenciones de escritura


Aplicar PEP 8 como base y las reglas del TP2 que estén documentadas.


| Elemento | Convención del proyecto | Ejemplo |
|---|---|---|
| Archivos y módulos | snake_case en minúsculas | servicio_compras.py |
| Funciones, métodos y variables | snake_case descriptivo | validar_fecha_visita |
| Clases | PascalCase | SolicitudCompra |
| Constantes | MAYUSCULAS_CON_GUIONES_BAJOS | MAXIMO_ENTRADAS |
| Funciones de prueba | test_cXX_comportamiento_esperado | test_c12_rechaza_mas_de_diez_entradas |


- Usar cuatro espacios por nivel de indentación y evitar tabuladores.
- Usar UTF-8 y conservar las tildes en documentación y mensajes.
- Escribir identificadores propios en español, sin tildes ni ñ; conservar los nombres exigidos por bibliotecas.
- Usar comillas dobles como preferencia del proyecto; delegar el formato final en la herramienta configurada.
- Adoptar 88 caracteres como ancho objetivo inicial, sujeto al límite acordado en el TP2. No confundir esta elección con el límite recomendado por PEP 8.
- Separar importaciones de biblioteca estándar, terceros y módulos propios. Evitar importaciones con asterisco.
- Eliminar importaciones y variables sin uso.
- Usar nombres que expresen su función. Evitar abreviaturas ambiguas, código comentado y números de negocio repetidos.
- Mantener las funciones centradas en una responsabilidad. Extraer componentes cuando el código lo justifique.


## 4. Tipado y documentación


- Agregar anotaciones de tipos a las funciones públicas, los modelos y los contratos entre componentes.
- Definir explícitamente qué campos pueden estar ausentes y cómo se representan.
- Evitar Any cuando se conoce el tipo.
- Documentar el propósito, las decisiones relevantes y los supuestos del dominio.
- Los comentarios deben explicar decisiones que el código no haga evidentes.
- Mantener mensajes de la interfaz y documentación del proyecto en español.


## 5. Separación de responsabilidades


- La interfaz recoge datos, presenta resultados y llama a la lógica compartida.
- El límite de entrada convierte los datos y reconoce formatos inválidos.
- La lógica de compra aplica las reglas del dominio y coordina las acciones necesarias.
- El reloj, calendario, pago y correo se suministran como dependencias controlables.
- Las pruebas llaman al código que utiliza la aplicación; no deben comprobar una implementación alternativa creada solo para los tests.
- Mantener pytest y las fixtures fuera del código de producción.
- Evitar iniciar ventanas, pedir datos o producir efectos al importar módulos.


## 6. Contrato de implementación compartido


Antes de distribuir cambios que dependan entre sí, documentar en docs/CONTRATO_IMPLEMENTACION.md:
- Los nombres públicos de funciones, clases y módulos.
- La estructura y los tipos de la solicitud.
- Los resultados de aceptación y rechazo y sus campos.
- Los identificadores de motivos de rechazo.
- Los estados de compra y pago y sus transiciones permitidas.
- Las interfaces del reloj, calendario y servicios simulados.


Una vez elegido, mantener un único mecanismo para comunicar cada resultado esperado. No mezclar de forma improvisada diccionarios, booleanos, mensajes impresos y excepciones para representar lo mismo.


Un rechazo de negocio debe exponer un motivo estable comprobable por los tests. La interfaz puede traducir ese motivo a un mensaje legible.


Los cambios incompatibles del contrato requieren coordinación con el equipo y actualización de sus consumidores.


## 7. Validaciones y errores


- Validar la solicitud antes de solicitar pagos, enviar correos o registrar una compra finalizada.
- Conservar los valores validados de cantidad, fecha y opciones.
- Distinguir un campo ausente, un formato inválido y un rechazo de negocio cuando el contrato así lo defina.
- Evitar capturar excepciones generales para ocultar errores de programación.
- No inventar restricciones de edad, precios, descuentos o reglas no acordadas.
- Registrar las validaciones adicionales DG como decisiones del grupo.
- No ajustar las expectativas de los tests para encubrir un defecto del programa.
- Si el usuario aporta varios datos inválidos, seguir una política compartida de selección o acumulación de errores. Los casos individuales deben aislar la causa esperada.


## 8. Desarrollo mediante TDD


Incorporar los comportamientos gradualmente:
1. Red: escribir una prueba para el comportamiento pendiente y ejecutarla. Identificar el fallo y su causa.
2. Green: implementar lo mínimo necesario y ejecutar la nueva prueba y las anteriores.
3. Refactor: mejorar el diseño cuando corresponda y volver a verificar.


- No construir toda la funcionalidad antes de escribir las pruebas.
- Si una prueba nueva ya pasa, registrar que el comportamiento existe. No provocar un fallo artificial.
- No añadir ramas que reconozcan identificadores C01–C28 o detecten que se está ejecutando pytest.
- Conservar evidencia real; no inventar ejecuciones, resultados o refactorizaciones.


## 9. Estructura de los tests


- Nombrar archivos test_*.py y funciones test_cXX_comportamiento_esperado.
- Preferir un archivo por caso documental cuando facilite el reparto, con sus variantes dentro del mismo archivo.
- Organizar cada prueba en preparación, ejecución y verificación.
- Comprobar salidas y efectos observables mediante aserciones concretas.
- En un rechazo, comprobar la causa prevista y mantener válidas las demás condiciones.
- Un rechazo esperado significa que el test debe pasar cuando el sistema rechaza correctamente.
- Usar parametrización cuando cambien datos de una misma regla.
- Los 28 casos documentales pueden originar más de 28 ejecuciones.
- Evitar depender del orden de ejecución, del reloj real, de Internet o de pausas arbitrarias.
- No introducir skip, xfail o desactivaciones para presentar como completado un comportamiento pendiente.
- Mantener trazabilidad entre criterios de aceptación, casos, tests y variantes.


## 10. Fixtures y datos comunes


Centralizar las preparaciones reutilizables en tests/conftest.py. Cada test debe recibir un estado independiente; usar alcance de función para los objetos mutables y los dobles.


| Dato | Referencia de pruebas |
|---|---|
| Usuario | visitante01, registrado, correo visitante@example.com |
| Fecha actual D0 | 12 de junio de 2030 |
| Calendario | D0 − 1, D0 y D0 + 1 abiertos; D0 + 2 cerrado |
| Solicitud base | Visita en D0 + 1, dos entradas y edades de 24 y 36 años |
| Opciones base | Pase regular y efectivo en boletería |
| Servicios | Pago y correo nuevos, sin interacciones previas |


- Compartir las definiciones de preparación, no el mismo estado mutable entre pruebas.
- Mantener coherencia entre campos relacionados. Para probar once entradas, preparar once edades válidas.
- Los datos de prueba no establecen el calendario comercial del parque.
- El código de producción debe recibir dependencias; no importar las fixtures.


## 11. Pago y correo simulados


- Utilizar servicios simulados para la demostración y dobles controlados para los tests.
- Permitir observar las solicitudes de pago y correo.
- Distinguir inicio de pago y aprobación: una redirección no acredita un pago.
- Para efectivo, identificar el pago en boletería sin solicitar redirección a tarjeta.
- Acordar el momento de finalización y envío de correo antes de cerrar los casos dependientes.
- Verificar las interacciones cuando formen parte del comportamiento esperado, incluyendo su ausencia en una solicitud inválida.
- No presentar una simulación como evidencia de una integración real con Mercado Pago o correo externo.


## 12. Interfaz


- Mostrar resultados y motivos de rechazo comprensibles.
- Permitir demostrar casos como once entradas, fecha pasada y forma de pago ausente.
- Mantener las validaciones de negocio en la lógica compartida, aunque la interfaz agregue ayudas de carga.
- Identificar claramente el reloj y los servicios simulados.
- El dominio debe poder probarse sin abrir ventanas.
- La verificación manual de la interfaz y los tests automáticos de la lógica deben distinguirse en la evidencia.


## 13. Formato y controles automáticos


Usar Ruff como propuesta inicial de formateador y linter, con una configuración común en pyproject.toml y versiones registradas. Si ya existe otra herramienta acordada, conservarla y documentar el cambio de este apartado.


Cuando las herramientas estén instaladas y configuradas, ejecutar desde la raíz del proyecto:


~~~text
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
~~~


Para ejecutar los tests asociados a C12:


~~~text
python -m pytest -k c12 -v
~~~


- Configurar los controles de acuerdo con las reglas efectivamente adoptadas.
- No desactivar controles globales para resolver un problema local.
- Documentar las excepciones justificadas.
- Registrar resultados y limitaciones reales. Este archivo no acredita que esos comandos ya se hayan ejecutado.


## 14. Colaboración y commits


- Actualizar la base de trabajo antes de comenzar un caso y coordinar sus dependencias.
- Trabajar en una rama identificable y mantener los cambios centrados en los casos asignados.
- Coordinar cambios sobre funciones compartidas para evitar implementaciones incompatibles.
- Como política del equipo, registrar un commit por caso completado y verificado; sus variantes pueden compartir el commit.
- Este reparto de commits es una decisión organizativa, no una exigencia textual identificada en el TP6 disponible.
- Ejemplo de mensaje: TP6 C12: rechazar compras de más de diez entradas.
- Incluir únicamente los archivos relacionados con el avance.
- Conservar la autoría real y las modificaciones de otros integrantes.
- No reconstruir retrospectivamente un historial ficticio de TDD.
- Ejecutar la suite completa y los controles de estilo antes de integrar. No dejar cambios de casos completados con pruebas fallando.
- Registrar la evidencia Red antes de corregir y la evidencia Green posterior, sin necesidad de integrar una versión rota.


## 15. Reglas para asistentes de IA


Cada integrante debe proporcionar este archivo a su herramienta de IA y solicitar su lectura explícita.


La IA debe:
- Leer estas reglas, las instrucciones AGENTS.md aplicables, el contrato, el entregable y los tests existentes.
- Identificar los casos asignados y el estado actual antes de modificar archivos.
- Reutilizar los nombres públicos, fixtures y componentes del equipo.
- Desarrollar por TDD y respetar los contratos compartidos.
- Proponer y coordinar los cambios incompatibles antes de aplicarlos.
- Consultar decisiones de dominio que alteren resultados esperados, avanzando en tareas independientes.
- Informar los archivos modificados y los resultados realmente observados.
- Declarar si no pudo leer una fuente o ejecutar una comprobación.
- Mantener el alcance en el TP y conservar los cambios previos.


## 16. Documentación y definición de terminado


Mantener actualizados:
- README.md: instalación, versiones verificadas y comandos para aplicación y tests.
- docs/CONTRATO_IMPLEMENTACION.md: interfaz pública y resultados.
- docs/ASIGNACION_CASOS.md: responsables, dependencias y estado.
- docs/TRAZABILIDAD_PRUEBAS.md: casos, variantes y tests correspondientes.
- docs/REGISTRO_TDD.md: evidencia de Red, Green y refactorizaciones reales.
- docs/Acuerdos_del_grupo.md: acuerdos A01–A04 y decisiones adicionales.


Un caso se considera terminado cuando sus variantes acordadas tienen aserciones verificables, pasan junto con la suite previa, respetan los controles adoptados y cuentan con trazabilidad y evidencia.


No marcar como terminado un caso bloqueado por una definición de dominio pendiente.


## 17. Uso en el repositorio


Guardar este archivo como TP06-DES-EcoHarmony-Reglas-Codificacion.md en la carpeta del TP6.


Para herramientas que utilizan AGENTS.md, agregar allí una referencia a estas reglas y al contrato. Conservar las instrucciones existentes del repositorio.


Las herramientas que no leen esos archivos automáticamente deben recibirlos como adjuntos o texto. La revisión del equipo y los controles automáticos verifican el cumplimiento de las instrucciones.


## 18. Referencias


- Entregable TP6: https://docs.google.com/document/d/1pQn4NenJPZnAo-5I96zp5MJfi2sw5BZ410rZmewg7dU
- PEP 8: https://peps.python.org/pep-0008/
- pytest: https://docs.pytest.org/en/stable/
- Fixtures de pytest: https://docs.pytest.org/en/stable/how-to/fixtures.html
- Ruff: https://docs.astral.sh/ruff/
- Formato AGENTS.md: https://agents.md/
