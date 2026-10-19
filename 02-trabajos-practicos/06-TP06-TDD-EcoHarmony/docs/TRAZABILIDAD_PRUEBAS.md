# Trazabilidad de pruebas

Relación entre criterios de aceptación, casos del entregable, archivos de test y
variantes. «Pendiente» significa que el archivo contiene la especificación pero
todavía no tiene tests.

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
| C03 | CA02, CA05 | `tests/test_c03_fecha_actual.py` | — | Pendiente |
| C04 | CA02, CA05 | `tests/test_c04_fecha_futura.py` | — | Pendiente |
| C05 | CA07, A03 | `tests/test_c05_una_entrada.py` | — | Pendiente |
| C06 | CA07, A03 | `tests/test_c06_nueve_entradas.py` | — | Pendiente |
| C07 | CA07, A03 | `tests/test_c07_diez_entradas.py` | — | Pendiente |
| C08 | CA01, A03 | `tests/test_c08_pase_vip.py` | — | Pendiente |
| C09 | CA01, A03 | `tests/test_c09_pase_regular.py` | — | Pendiente |
| C10 | CA02 | `tests/test_c10_fecha_pasada.py` | — | Pendiente |
| C11 | CA05 | `tests/test_c11_parque_cerrado.py` | — | Pendiente |
| C12 | CA07 | `tests/test_c12_mas_de_diez_entradas.py` | — | Pendiente |
| C13 | CA06 | `tests/test_c13_forma_pago_ausente.py` | — | Pendiente |
| C14 | CA09 | `tests/test_c14_usuario_no_registrado.py` | — | Pendiente |
| C15 | CA01 | `tests/test_c15_fecha_ausente.py` | — | Pendiente |
| C16 | CA01 | `tests/test_c16_edades_incompletas.py` | — | Pendiente |
| C17 | CA01 | `tests/test_c17_tipo_pase_ausente.py` | — | Pendiente |
| C18 | CA01 | `tests/test_c18_cantidad_ausente.py` | — | Pendiente |
| C19 | CA03, A02, A04 | `tests/test_c19_correo_confirmacion.py` | — | Pendiente |
| C20 | CA08, A03 | `tests/test_c20_resumen_compra.py` | — | Pendiente |
| C21 | CA04, A04 | `tests/test_c21_inicio_pago_tarjeta.py` | — | Pendiente |
| C22 | CA06, DD05 | `tests/test_c22_pago_efectivo_sin_redireccion.py` | — | Pendiente |
| C23 | DD02 | `tests/test_c23_rechazo_sin_efectos.py` | — | Pendiente |
| C24 | DD05, A02 | `tests/test_c24_redireccion_no_acredita_pago.py` | — | Pendiente |
| C25 | DG01 | `tests/test_c25_cantidad_no_entera_positiva.py` | — | Pendiente |
| C26 | DG02 | `tests/test_c26_opcion_no_admitida.py` | — | Pendiente |
| C27 | DG03 | `tests/test_c27_formato_fecha_invalido.py` | — | Pendiente |
| C28 | DG04 | `tests/test_c28_edad_invalida.py` | — | Pendiente |
