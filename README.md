# Gestión de Configuración del Software - ISW G7 4K2 2026

> **Fecha de creación:** 23/08/2026 | **Última actualización:** 24/08/2026
>
> **Materia:** Ingeniería y Calidad de Software
>
> **Repositorio:** [ISW_G7_4K2_2026](https://github.com/juansarey/ISW_G7_4K2_2026)

---

## Integrantes del equipo

| Apellido y nombre       | Legajo |
| ----------------------- | -----: |
| Adaime, Santiago        |  91316 |
| Altamirano, Antonella   | 402055 |
| Bongiorno, Valentino    |  98495 |
| Grillo, Octavio         |  94788 |
| Lenta, Martina          |  95294 |
| Montes, Romeo Facundo   | 406511 |
| Rossa Masselli, Máximo  | 400034 |
| Sacco Rey, Juan Pablo   |  89319 |
| Salomon Wendler, Thomas | 400501 |
| Schoninger, Lucas       |  97927 |
| Tabares, Maximo Samir   | 402064 |
| Tejeda, Emanuel Jesus   | 401000 |
| Visintin, Juan Pablo    |  95843 |
| Zengaro, Tomas          | 403344 |

## Introducción

### Propósito del repositorio

Centralizar y gestionar los productos de la materia Ingeniería y Calidad de Software. El repositorio conserva los materiales proporcionados por la cátedra y los artefactos producidos por el grupo, manteniendo su identificación, trazabilidad y evolución mediante Git.

Este README constituye la referencia de Gestión de Configuración del Software (SCM) del repositorio.

### Alcance

El repositorio contempla los siguientes elementos:

- Documentación de Gestion de Configuración del Software (SCM).
- Reglas, normas e indicaciones de la materia.
- Material teórico, bibliografía y presentaciones de referencia.
- Productos generados en los trabajos prácticos.
- Productos del trabajo de investigación grupal.

---

## Organización del Repositorio

A continuación se describe la estructura de directorios del repositorio:

```text
ISW_G7_4K2_2026/
├── README.md
├── 00-reglas-materia/
├── 01-material-teorico/
│   ├── 00-presentaciones-clases/
│   ├── 01-material-bibliografico/
│   │   └── <NN>-<TEMA>/
│   └── 02-notas-clase/
├── 02-trabajos-practicos/
│   └── <NN>-TP<N>-<NOMBRE_TP>/
└── 03-trabajo-investigacion-grupal/
```

Los TP4 y TP5 no tienen directorio propio: el TP4 se representa mediante este README y el TP5 evalúa el uso y evolución de este repositorio.

> [!NOTE]
> `<N>` representa el número secuencial del trabajo práctico (ejemplo: `01` ).
>
> `<NN>` representa el número secuencial de orden de dos dígitos (ejemplo: `00` , `01` ).
>
> `<TEMA>` representa el nombre del tema o material bibliográfico (ejemplo: `testing-software` ).
>
> `<NOMBRE_TP>` representa el nombre descriptivo asignado al trabajo práctico (ejemplo: `Requerimientos-EcoHarmony` ).

---

## Convenciones de nombrado

Los nombres de directorios siguen el formato `<numero>-<descripcion>`. Para los trabajos prácticos se utiliza `<numero>-TP<numero>-<tema>-<dominio>`.

### 00-reglas-materia/

| Ítem de configuración | Formato del nombre              | Ubicación            |
| --------------------- | ------------------------------- | -------------------- |
| Reglas de la materia  | `REG-<descripcion>.<extension>` | `00-reglas-materia/` |

**Ejemplo:**`REG-Criterios-Evaluacion.pdf`

### 01-material-teorico/

| Ítem de configuración       | Formato del nombre                               | Ubicación                                        |
| --------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| Material teórico general    | `MAT-<tema>-<descripcion>.<extension>`           | `01-material-teorico/`                           |
| Material teórico por unidad | `MAT-U<numero>-<tema>-<descripcion>.<extension>` | `01-material-teorico/`                           |
| Presentaciones de clase     | `MAT-U<numero>-<tema>-Presentacion.<extension>`  | `01-material-teorico/00-presentaciones-clases/`  |
| Material bibliográfico      | `MAT-U<numero>-<tema>-<descripcion>.<extension>` | `01-material-teorico/01-material-bibliografico/` |
| Notas de clase              | `MAT-U<numero>-<tema>-Notas-Clase.<extension>`   | `01-material-teorico/02-notas-clase/`            |

**Ejemplos:**`MAT-SCM-Gestion-Configuracion.pdf`, `MAT-U03-SCM-Gestion-Configuracion.pdf`, `MAT-U03-SCM-Presentacion.pdf`, `MAT-U03-SCM-Notas-Clase.md`

> [!NOTE]
> Las notas de clase se identifican mediante la unidad y el tema en el nombre del archivo, sin crear un subdirectorio por cada unidad. Si hubiera varias notas para una misma unidad y tema, puede agregarse el numero de clase: `MAT-U03-C02-SCM-Notas-Clase.md`.

### 02-trabajos-practicos/

| Ítem de configuración        | Formato del nombre                                        | Ubicación                |
| ---------------------------- | --------------------------------------------------------- | ------------------------ |
| Producto de trabajo práctico | `TP<numero>-<tipoCI>-<dominio>-<descripcion>.<extension>` | `02-trabajos-practicos/` |

**Ejemplos:**`TP01-REQ-Mis-Gastos-Especificacion.pdf`, `TP06-SRC-EcoHarmony-Codigo.py`, `TP09-TST-EcoHarmony-Casos-Prueba.xlsx`

> [!NOTE]
> Los archivos correspondientes a un mismo trabajo práctico se almacenan dentro del directorio del TP correspondiente. Solo se crean subdirectorios adicionales cuando sea necesario agrupar varios archivos relacionados.

### 03-trabajo-investigacion-grupal/

| Ítem de configuración           | Formato del nombre              | Ubicación                          |
| ------------------------------- | ------------------------------- | ---------------------------------- |
| Trabajo de investigación grupal | `INV-<descripcion>.<extension>` | `03-trabajo-investigacion-grupal/` |

**Ejemplos:**`INV-Informe-Final.pdf`, `INV-Presentacion-Final.pptx`

---

## Ítems de configuración

Se considera Ítem de Configuración (IC) a todo elemento relevante para la materia, que forme parte de una actividad, que pueda actualizarse o que necesite conservarse, identificarse y recuperarse posteriormente. No se incorporan archivos temporales, copias duplicadas ni apuntes personales.

| Código | Tipo de IC                      |
| ------ | ------------------------------- |
| `REG`  | Reglas de la materia            |
| `MAT`  | Material teórico                |
| `REQ`  | Requerimientos                  |
| `SRC`  | Código fuente                   |
| `AUT`  | Pruebas automatizadas           |
| `DES`  | Documentación de diseño         |
| `TST`  | Documentación de testing        |
| `SCR`  | Artefactos Scrum                |
| `RET`  | Retrospectiva                   |
| `KAN`  | Artefactos Kanban               |
| `DT`   | Design Thinking                 |
| `INV`  | Trabajo de investigación grupal |

---

## Glosario de abreviaturas

El glosario de abreviaturas define las siglas utilizadas en el documento para facilitar su comprensión y mantener un uso uniforme de los términos.

| Abreviatura | Significado                           |
| ----------- | ------------------------------------- |
| `SCM`       | Gestión de Configuración del Software |
| `CI`        | Ítem de Configuración                 |
| `TP`        | Trabajo Práctico                      |
| `LB`        | Línea Base                            |

---

## Convención de mensajes de commit

La documentación SCM vigente define que Git administra el historial y las versiones de los Ítems de Configuración.

`<Legajo>: <descripción del cambio>`

---

## Criterios de línea base

Se establecerá una línea base luego de la corrección de cada trabajo práctico evaluable. En ese momento, los ítems de configuración asociados al trabajo práctico deberán encontrarse completos, revisados y estables. Se adopta este criterio porque la corrección posterior a la evaluación representa un estado validado del trabajo y constituye un hito significativo en la evolución del repositorio.

Las líneas base se implementan mediante tags de Git con el formato `LB-<numero>-<descripcion>`, donde el numero es correlativo de dos digitos. La primera linea base prevista es `LB-01-Configuracion-Inicial`, una vez aprobadas la estructura inicial, la documentacion SCM y los CIs disponibles.
