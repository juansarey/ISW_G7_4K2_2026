# Trazabilidad de pruebas

Relación entre criterios de aceptación, casos del entregable, archivos de test y
variantes. «Pendiente» significa que el caso todavía no tiene archivo ni tests; su
especificación está en el entregable (páginas 7 a 9).

## Criterios de aceptación

| CA | Condición | Casos |
|---|---|---|
| CA01 | Fecha, cantidad, edad de cada visitante y tipo de pase | C01, C02, C08, C09, C15, C16, C17, C18 |
| CA02 | Fecha actual o futura | C03, C04, C10 |
| CA03 | Correo de confirmación | C19 |
| CA04 | Redirigir a Mercado Pago con tarjeta | C02, C21 |
| CA05 | Día de apertura del parque | C03, C04, C11 |
| CA06 | Efectivo en boletería o tarjeta | C01, C02, C13, C22 |
| CA07 | No más de diez entradas | C05, C06, C07, C12 |
| CA08 | Informar cantidad y fecha al finalizar | C01, C20 |
| CA09 | Solo usuarios registrados | C01, C14 |

## Casos y tests

| Caso | Criterios | Archivo | Tests / variantes | Estado |
|---|---|---|---|---|
| C01 | CA01, CA06, CA08, CA09 | `tests/test_c01_compra_valida_efectivo.py` | `test_c01_confirma_compra_en_efectivo_con_pago_pendiente_en_boleteria`, `test_c01_conserva_cantidad_y_fecha_validadas`, `test_c01_registra_la_compra_confirmada`, `test_c01_solicita_un_correo_al_visitante` | Terminado |
| C02 | CA01, CA04, CA06 | `tests/test_c02_compra_valida_tarjeta.py` | `test_c02_acepta_y_abre_la_pasarela_de_pago`, `test_c02_mantiene_compra_y_pago_pendientes_hasta_la_aprobacion` | Terminado |
| C03 | CA02, CA05 | — | — | Pendiente |
| C04 | CA02, CA05 | — | — | Pendiente |
| C05 | CA07, A03 | — | — | Pendiente |
| C06 | CA07, A03 | — | — | Pendiente |
| C07 | CA07, A03 | — | — | Pendiente |
| C08 | CA01, A03 | — | — | Pendiente |
| C09 | CA01, A03 | — | — | Pendiente |
| C10 | CA02 | — | — | Pendiente |
| C11 | CA05 | — | — | Pendiente |
| C12 | CA07 | — | — | Pendiente |
| C13 | CA06 | — | — | Pendiente |
| C14 | CA09 | — | — | Pendiente |
| C15 | CA01 | — | — | Pendiente |
| C16 | CA01 | — | — | Pendiente |
| C17 | CA01 | — | — | Pendiente |
| C18 | CA01 | — | — | Pendiente |
| C19 | CA03, A02, A04 | — | — | Pendiente |
| C20 | CA08, A03 | — | — | Pendiente |
| C21 | CA04, A04 | — | — | Pendiente |
| C22 | CA06, DD05 | — | — | Pendiente |
| C23 | DD02 | — | — | Pendiente |
| C24 | DD05, A02 | — | — | Pendiente |
| C25 | DG01 | — | — | Pendiente |
| C26 | DG02 | — | — | Pendiente |
| C27 | DG03 | — | — | Pendiente |
| C28 | DG04 | — | — | Pendiente |
