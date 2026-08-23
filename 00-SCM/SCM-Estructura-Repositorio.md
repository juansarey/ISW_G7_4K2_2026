# Estructura del Repositorio

## Objetivo

Definir la estructura para organizar los Items de Configuracion y los productos utilizados o generados durante el cursado de Ingenieria y Calidad de Software. La estructura debe facilitar su identificacion, ubicacion, mantenimiento y evolucion.

## Estructura objetivo

```text
.
|- 00-SCM/
|- 01-reglas-materia/
|- 02-material-teorico/
|- 03-trabajos-practicos/
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
`- 04-trabajo-investigacion-grupal/
```

## Criterios de organizacion

- Los directorios y subdirectorios usan prefijos numericos de dos digitos para mantener un orden uniforme.
- Se crea un subdirectorio solo cuando sea necesario agrupar varios archivos relacionados. Un unico archivo se guarda directamente en su directorio superior.
- La estructura puede evolucionar durante el cursado ante nuevos productos o necesidades de organizacion.
- Los directorios de actividades futuras pueden crearse a medida que se generen sus productos asociados.

## Consideraciones SCM

TP4 corresponde a la definicion e implementacion de la Gestion de Configuracion y esta representado por `00-SCM/`. TP5 evalua el uso y evolucion del repositorio definido en TP4; por ello ninguno de los dos posee un directorio independiente dentro de `03-trabajos-practicos/`.
