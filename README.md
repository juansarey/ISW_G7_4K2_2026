# Gestion de Configuracion del Software - ISW G7 4K2 2026

> **Fecha de creacion:** 23/08/2026 | **Ultima actualizacion:** 23/08/2026
>
> **Materia:** Ingenieria y Calidad de Software
>
> **Repositorio:** [ISW_G7_4K2_2026](https://github.com/juansarey/ISW_G7_4K2_2026)

---

## Integrantes del equipo

| Apellido y nombre | Legajo |
| --- | ---: |
| Adaime, Santiago | 91316 |
| Altamirano, Antonella | 402055 |
| Bongiorno, Valentino | 98495 |
| Grillo, Octavio | 94788 |
| Lenta, Martina | 95294 |
| Montes, Romeo Facundo | 406511 |
| Rossa Masselli, Maximo | 400034 |
| Sacco Rey, Juan Pablo | 89319 |
| Salomon Wendler, Thomas | 400501 |
| Schoninger, Lucas | 97927 |
| Tabares, Maximo Samir | 402064 |
| Tejeda, Emanuel Jesus | 401000 |
| Visintin, Juan Pablo | 95843 |
| Zengaro, Tomas | 403344 |

## Introduccion

### Proposito del repositorio

Centralizar y gestionar los productos de la materia Ingenieria y Calidad de Software. El repositorio conserva los materiales proporcionados por la catedra y los artefactos producidos por el grupo, manteniendo su identificacion, trazabilidad y evolucion mediante Git.

Este README constituye la referencia de Gestion de Configuracion del Software (SCM) del repositorio.

### Alcance

El repositorio contempla los siguientes elementos:

- Documentacion de Gestion de Configuracion del Software (SCM).
- Reglas, normas e indicaciones de la materia.
- Material teorico, bibliografia y presentaciones de referencia.
- Productos generados en los trabajos practicos.
- Productos del trabajo de investigacion grupal.

---

## Organizacion del repositorio

La estructura actual del repositorio es la siguiente:

```text
ISW_G7_4K2_2026/
|- README.md
|- 00-reglas-materia/
|- 01-material-teorico/
|- 02-trabajos-practicos/
|  |- 01-TP01-Requerimientos-Mis-Gastos/
|  |- 02-TP02-Requerimientos-EcoHarmony/
|  |- 03-TP03-Requerimientos-Recircula/
|  |- 06-TP06-TDD-EcoHarmony/
|  |  |- 00-codigo-fuente/
|  |  `- 01-pruebas-automatizadas/
|  |- 07-TP07-Scrum-Parque-Diversiones/
|  |- 08-TP08-Testing-Taxi-Mobile/
|  |- 09-TP09-Testing-EcoHarmony/
|  |- 10-TP10-Kanban/
|  |- 11-TP11-Scrum-Retrospectiva/
|  |- 12-TP12-Design-Thinking/
|  `- 13-TP13-Scrum-Release-Planning/
`- 03-trabajo-investigacion-grupal/
```

Los TP4 y TP5 no tienen directorio propio: el TP4 se representa mediante este README y el TP5 evalua el uso y evolucion de este repositorio.

> [!NOTE]
> Los directorios y subdirectorios utilizan prefijos numericos de dos digitos. Solo se crea un subdirectorio cuando sea necesario agrupar varios archivos relacionados.

---

## Convenciones de nombrado

Los nombres de directorios siguen el formato `<numero>-<descripcion>`. Para los trabajos practicos se utiliza `<numero>-TP<numero>-<tema>-<dominio>`.

Los nombres de archivos no deben incluir espacios, acentos, caracteres especiales ni numeros de version. Deben utilizar guiones medios como separadores y conservarse estables mientras representen el mismo Item de Configuracion.

| Item de configuracion | Formato del nombre | Ubicacion |
| --- | --- | --- |
| Reglas de la materia | `REG-<descripcion>.<extension>` | `00-reglas-materia/` |
| Material teorico | `MAT-<tema>-<descripcion>.<extension>` | `01-material-teorico/` |
| Material teorico por unidad | `MAT-U<numero>-<tema>-<descripcion>.<extension>` | `01-material-teorico/` |
| Producto de trabajo practico | `TP<numero>-<tipoCI>-<dominio>-<descripcion>.<extension>` | `02-trabajos-practicos/` |
| Trabajo de investigacion grupal | `INV-<descripcion>.<extension>` | `03-trabajo-investigacion-grupal/` |

Ejemplos: `REG-Criterios-Evaluacion.pdf`, `MAT-U03-SCM-Gestion-Configuracion.pdf` y `TP09-TST-EcoHarmony-CasosPrueba.xlsx`.

## Items de configuracion

Se considera Item de Configuracion (CI) a todo elemento relevante para la materia, que forme parte de una actividad, que pueda actualizarse o que necesite conservarse, identificarse y recuperarse posteriormente. No se incorporan archivos temporales, copias duplicadas ni apuntes personales.

| Codigo | Tipo de CI |
| --- | --- |
| `REG` | Reglas de la materia |
| `MAT` | Material teorico |
| `REQ` | Requerimientos |
| `SRC` | Codigo fuente |
| `AUT` | Pruebas automatizadas |
| `DES` | Documentacion de diseno |
| `TST` | Documentacion de testing |
| `SCR` | Artefactos Scrum |
| `RET` | Retrospectiva |
| `KAN` | Artefactos Kanban |
| `DT` | Design Thinking |
| `INV` | Trabajo de investigacion grupal |

---

## Convencion de mensajes de commit

La documentacion SCM vigente define que Git administra el historial y las versiones de los Items de Configuracion. La convencion especifica para los mensajes de commit aun no fue establecida; hasta su definicion, los mensajes deben describir de forma breve y clara el cambio realizado.

---

## Glosario de abreviaturas

| Abreviatura | Significado |
| --- | --- |
| `REG` | Reglas de la materia |
| `MAT` | Material teorico |
| `REQ` | Requerimientos |
| `SRC` | Codigo fuente |
| `AUT` | Pruebas automatizadas |
| `DES` | Documentacion de diseno |
| `TST` | Documentacion de testing |
| `SCR` | Artefactos Scrum |
| `RET` | Retrospectiva |
| `KAN` | Artefactos Kanban |
| `DT` | Design Thinking |
| `INV` | Trabajo de investigacion grupal |
| `TP` | Trabajo Practico |
| `CI` | Item de Configuracion |
| `LB` | Linea base |

## Criterios de linea base

Una linea base representa un estado estable e identificado de uno o mas Items de Configuracion. Se crea al alcanzar un hito academico relevante, siempre que los elementos asociados esten completos, revisados por el grupo, correctamente ubicados y respeten las reglas de nombrado.

Las lineas base se implementan mediante tags de Git con el formato `LB-<numero>-<descripcion>`, donde el numero es correlativo de dos digitos. La primera linea base prevista es `LB-01-Configuracion-Inicial`, una vez aprobadas la estructura inicial, la documentacion SCM y los CIs disponibles.

---

## Mantenimiento de esta guia

El contenido de este README reemplaza la documentacion SCM anteriormente separada. Cualquier cambio en la estructura, las reglas de nombrado, los Items de Configuracion o las lineas base debe actualizarse aqui y registrarse mediante Git.
