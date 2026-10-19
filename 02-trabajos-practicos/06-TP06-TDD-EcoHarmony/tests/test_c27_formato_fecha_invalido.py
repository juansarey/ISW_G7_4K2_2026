"""C27 — Fecha con formato inválido (DG03).

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: DG03
- Tipo: Rechazo (decisión del grupo)
- Condición: Fecha recibida en un formato que no puede convertirse en fecha.
- Comportamiento esperado: Rechazar en el límite de entrada; las reglas del dominio
  recibirán fechas válidas.
- Preparación sugerida: convertir_solicitud con fecha_visita='31/02/2030' o 'mañana'
- Motivo esperado: MotivoRechazo.FECHA_FORMATO_INVALIDO

Tests previstos (nombres sugeridos):
- test_c27_rechaza_fecha_con_formato_invalido

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
