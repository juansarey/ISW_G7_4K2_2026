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
| C03 | CA02, CA05 | `tests/test_c03_fecha_actual.py` | `test_c03_acepta_fecha_actual_con_parque_abierto`, con efectivo y tarjeta (2 ejecuciones) | Terminado |
| C04 | CA02, CA05 | `tests/test_c04_fecha_futura.py` | `test_c04_acepta_fecha_futura_con_parque_abierto`, con efectivo y tarjeta (2 ejecuciones) | Terminado |
| C05 | CA07, A03 | — | — | Pendiente |
| C06 | CA07, A03 | — | — | Pendiente |
| C07 | CA07, A03 | `tests/test_c07_diez_entradas.py` | `test_c07_acepta_el_maximo_de_diez_entradas` | Green directo |
| C08 | CA01, A03 | `tests/test_c08_pase_vip.py` | `test_c08_acepta_y_conserva_el_pase_vip` | Green directo |
| C09 | CA01, A03 | `tests/test_c09_pase_regular.py` | `test_c09_acepta_y_conserva_el_pase_regular` | Terminado |
| C10 | CA02 | `tests/test_c10_fecha_pasada.py` | `test_c10_rechaza_fecha_anterior_a_la_actual` | Terminado |
| C11 | CA05 | `tests/test_c11_parque_cerrado.py` | `test_c11_rechaza_fecha_futura_con_parque_cerrado`, efectivo y tarjeta (2 ejecuciones) | Terminado |
| C12 | CA07 | `tests/test_c12_maximo_entradas.py` | `test_c12_rechaza_mas_de_diez_entradas`, con efectivo y tarjeta (2 ejecuciones) | Terminado |
| C13 | CA06 | `tests/test_c13_forma_pago_ausente.py` | `test_c13_rechaza_compra_sin_forma_de_pago_seleccionada` (1 ejecución; sin parametrizar porque falta la forma de pago) | Terminado |
| C14 | CA09 | `tests/test_c14_usuario_no_registrado.py` | `test_c14_rechaza_compra_de_visitante_sin_registro`, con efectivo y tarjeta (2 ejecuciones) | Terminado |
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

C03 y C04 comprueban que D0 y D0 + 1, respectivamente, están abiertos en el
calendario preparado, que la solicitud se acepta y que la fecha se conserva en el
resultado y en la compra registrada. C11 verifica el rechazo de D0 + 2 con el
calendario inyectado, en efectivo y tarjeta, sin registrar compras ni iniciar
efectos externos. C12 verifica el rechazo de once entradas con once edades válidas,
en efectivo y tarjeta. C13 deja la solicitud base intacta salvo la forma de pago,
que queda sin elegir, y comprueba el rechazo con `FORMA_PAGO_AUSENTE` sin compra
registrada, redirección, pedido de pago ni correo. C14 usa el visitante de
referencia marcado como no registrado, con el resto de la solicitud válida, y
verifica en efectivo y tarjeta el rechazo con `USUARIO_NO_REGISTRADO` sin ningún
efecto. C05, C06 y C15 a C28 siguen pendientes.
