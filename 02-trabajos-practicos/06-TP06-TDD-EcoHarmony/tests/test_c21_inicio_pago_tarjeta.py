"""C21 — Inicio del pago con tarjeta.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA04, A04
- Tipo: Interacción
- Condición: Solicitud válida con tarjeta; doble de pago disponible o con fallo al
  iniciar (PagoDoble(falla_al_iniciar=True)).
- Comportamiento esperado: Si disponible, redirigir una vez y dejar el pago
  pendiente. Si falla, ERROR_PAGO, sin compra confirmada ni correo.
- Preparación sugerida: crear_solicitud(forma_pago=FormaPago.TARJETA)
- Motivo esperado: ERROR_PAGO (variante con fallo)

Tests previstos (nombres sugeridos):
- test_c21_redirige_una_sola_vez_a_la_pasarela
- test_c21_informa_error_pago_si_falla_el_inicio

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
