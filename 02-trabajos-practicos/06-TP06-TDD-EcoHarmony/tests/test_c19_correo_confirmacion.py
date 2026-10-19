"""C19 — Correo de confirmación.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA03, A02, A04
- Tipo: Interacción
- Condición: Confirmación en efectivo o tarjeta aprobada; correo al visitante.
  Variar envío exitoso y fallo recuperable (CorreoDoble(falla_al_enviar=True)).
- Comportamiento esperado: Un correo por confirmación. Si falla: CORREO_PENDIENTE,
  conservando compra y pago. Reintentar solo el envío.
- Preparación sugerida: solicitud_base; para tarjeta aprobada se necesita definir la
  operación de aprobación (ver docs/CONTRATO_IMPLEMENTACION.md, operaciones
  pendientes)
- Motivo esperado: no corresponde (aceptación)

Tests previstos (nombres sugeridos):
- test_c19_envia_un_correo_por_confirmacion
- test_c19_marca_correo_pendiente_si_falla_el_envio
- test_c19_reintenta_solo_el_envio_del_correo

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
