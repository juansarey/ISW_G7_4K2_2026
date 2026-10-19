"""C11 — Rechazo por parque cerrado.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA05
- Tipo: Rechazo
- Condición: Fecha D0 + 2; calendario preparado con parque cerrado.
- Comportamiento esperado: Rechazar por cierre del parque, aunque la fecha sea
  futura.
- Preparación sugerida: crear_solicitud(fecha_visita=fecha_actual +
  timedelta(days=2))
- Motivo esperado: MotivoRechazo.PARQUE_CERRADO

Tests previstos (nombres sugeridos):
- test_c11_rechaza_dia_de_cierre_del_parque

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
