"""C26 — Opción de pase o pago no admitida (DG02).

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: DG02
- Tipo: Rechazo (decisión del grupo)
- Condición: Pase o forma de pago fuera de sus opciones; variar un campo por vez. Se
  comprueba en el límite de entrada (ecoharmony.entrada).
- Comportamiento esperado: Rechazar la opción no admitida.
- Preparación sugerida: convertir_solicitud con tipo_pase='PREMIUM' o
  forma_pago='CHEQUE'
- Motivo esperado: TIPO_PASE_INVALIDO / FORMA_PAGO_INVALIDA

Tests previstos (nombres sugeridos):
- test_c26_rechaza_opcion_no_admitida

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
