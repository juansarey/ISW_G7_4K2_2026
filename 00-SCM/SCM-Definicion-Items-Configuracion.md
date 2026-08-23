# Definicion de Items de Configuracion

## Objetivo

Definir los tipos de Items de Configuracion (CI) que se almacenan y gestionan en el repositorio durante el cursado. Incluyen productos generados por el grupo y material de la catedra que sea necesario conservar y controlar.

## Criterio de seleccion

Un elemento es un CI si tiene relevancia para la materia, forma parte de una actividad o trabajo, sirve de referencia posterior, puede actualizarse, requiere historial o debe poder identificarse y recuperarse. No son CIs los temporales, duplicados, apuntes personales ni elementos sin relevancia para el trabajo grupal.

## Tipos definidos

| Codigo | Item | Ubicacion prevista |
| --- | --- | --- |
| `SCM` | Documentacion de Gestion de Configuracion | `00-SCM/` |
| `REG` | Reglas de la materia | `01-reglas-materia/` |
| `MAT` | Material teorico | `02-material-teorico/` |
| `REQ` | Productos de requerimientos | `03-trabajos-practicos/` |
| `SRC` | Codigo fuente | `03-trabajos-practicos/` |
| `AUT` | Pruebas automatizadas | `03-trabajos-practicos/` |
| `DES` | Documentacion de diseno | `03-trabajos-practicos/` |
| `TST` | Documentacion de testing | `03-trabajos-practicos/` |
| `SCR` | Artefactos Scrum | `03-trabajos-practicos/` |
| `RET` | Productos de retrospectiva | `03-trabajos-practicos/` |
| `KAN` | Artefactos Kanban | `03-trabajos-practicos/` |
| `DT` | Productos de Design Thinking | `03-trabajos-practicos/` |
| `INV` | Trabajo de investigacion grupal | `04-trabajo-investigacion-grupal/` |

Los CIs se incorporan cuando son proporcionados por la catedra o generados por el grupo. Sus modificaciones se registran con Git; el material de la catedra conserva su contenido original y cualquier actualizacion queda versionada.
