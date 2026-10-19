# Acuerdos del grupo

Decisiones de la simulación adoptadas por el grupo. No son exigencias de la cátedra.

## Acuerdos del dominio (entregable, página 10)

| ID | Aspecto | Decisión adoptada | Dónde se implementa |
|---|---|---|---|
| A01 | Calendario de apertura | Abre de martes a domingo y cierra los lunes. El 14/06/2030 es cierre excepcional. Calendario configurable; la demostración usa D0 = 12/06/2030. | `ecoharmony/simulados.py` (`CalendarioParque`), `ecoharmony/web/app.py` |
| A02 | Confirmación, pago y correo | Efectivo: compra confirmada, pago pendiente en boletería y correo al confirmar. Tarjeta: compra y pago pendientes al abrir la pasarela simulada; confirmar y enviar correo tras aprobar. Rechazo o cancelación no confirman ni envían correo. | `ecoharmony/servicio_compras.py` |
| A03 | Tarifas | Regular $10.000 y VIP $15.000 por visitante, sin descuentos ni cargos extra. Total = cantidad × tarifa, con `Decimal`. | `ecoharmony/tarifas.py` |
| A04 | Simulación y fallos | Pago y correo locales. Fallo al iniciar pago: `ERROR_PAGO`. Fallo de correo: `CORREO_PENDIENTE` y reintento solo del envío. Fallos configurables en los dobles. | `ecoharmony/simulados.py`, `tests/dobles.py` |

## Validaciones adicionales (DG)

| ID | Decisión | Caso |
|---|---|---|
| DG01 | Rechazar cantidad cero, negativa o no entera | C25 |
| DG02 | Rechazar pase o forma de pago fuera de sus opciones | C26 |
| DG03 | Rechazar en el límite de entrada una fecha que no pueda convertirse | C27 |
| DG04 | Rechazar edad negativa o no entera; sin máximo de edad ni descuentos | C28 |

## Decisiones técnicas

| ID | Decisión | Estado |
|---|---|---|
| DT01 | **pytest** en lugar de unittest (cambio respecto de DD06 del entregable, regla 2). | Adoptada |
| DT02 | **Interfaz web** (Flask + HTML/CSS/JS sin frameworks) en lugar de Tkinter. La lógica de compra no depende de la interfaz. | **A confirmar por el equipo** (regla 2) |
| DT03 | Ruff como formateador y linter, configurado en `pyproject.toml`. Excepción justificada: N818, por los nombres de excepciones en español. | Adoptada |
| DT04 | Los rechazos devuelven un único motivo según el orden de `TP06-DES-EcoHarmony-Contrato-Implementacion.md` §4. | Propuesta |
| DT05 | Documentos en `00-documentacion/` con el formato `TP06-<tipoCI>-EcoHarmony-<descripcion>`; código, pruebas y configuración en `01-implementacion/` con snake_case (regla 3). | Adoptada (README del repositorio y regla 17) |
