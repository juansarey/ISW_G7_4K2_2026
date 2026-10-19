# Asignación de casos

Completar el responsable antes de comenzar un caso y actualizar el estado al
terminarlo (regla 16). Un caso está **terminado** cuando sus tests pasan junto con la
suite, respetan Ruff y tienen trazabilidad y evidencia en `TP06-TST-EcoHarmony-Registro-TDD.md`.

| Caso | Tema | Responsable | Depende de | Estado |
|---|---|---|---|---|
| C01 | Compra válida en efectivo | Bongiorno (98495) | — | Terminado |
| C02 | Compra válida con tarjeta | Bongiorno (98495) | C01 | Terminado |
| C03 | Fecha actual | Thomas Salomon Wendler (400501) | C01 | Terminado |
| C04 | Fecha futura | Thomas Salomon Wendler (400501) | C01 | Terminado |
| C05 | Una entrada | Por asignar | C01 | Pendiente |
| C06 | Nueve entradas | Por asignar | C01 | Pendiente |
| C07 | Diez entradas | Por asignar | C01 | Pendiente |
| C08 | Pase VIP | Por asignar | C01 | Pendiente |
| C09 | Pase regular | Por asignar | C01 | Pendiente |
| C10 | Fecha pasada | Por asignar | C01 | Pendiente |
| C11 | Parque cerrado | Por asignar | C01 | Pendiente |
| C12 | Más de diez entradas | Por asignar | C01 | Pendiente |
| C13 | Forma de pago ausente | Por asignar | C01 | Pendiente |
| C14 | Usuario no registrado | Por asignar | C01 | Pendiente |
| C15 | Fecha ausente | Por asignar | C01 | Pendiente |
| C16 | Edades incompletas | Por asignar | C01 | Pendiente |
| C17 | Tipo de pase ausente | Por asignar | C01 | Pendiente |
| C18 | Cantidad ausente | Por asignar | C01 | Pendiente |
| C19 | Correo de confirmación | Por asignar | C01, C02; operaciones pendientes del contrato §7 | Pendiente |
| C20 | Resumen de la compra | Por asignar | C01, C08 | Pendiente |
| C21 | Inicio del pago con tarjeta | Por asignar | C02 | Pendiente |
| C22 | Efectivo sin redirección | Por asignar | C01 | Pendiente |
| C23 | Rechazo sin efectos | Por asignar | C12 | Pendiente |
| C24 | Redirección no acredita pago | Por asignar | C02 | Pendiente |
| C25 | Cantidad no entera positiva (DG01) | Por asignar | C18; `ecoharmony/entrada.py` | Pendiente |
| C26 | Opción no admitida (DG02) | Por asignar | `ecoharmony/entrada.py` | Pendiente |
| C27 | Fecha con formato inválido (DG03) | Por asignar | `ecoharmony/entrada.py` | Pendiente |
| C28 | Edad inválida (DG04) | Por asignar | C16; `ecoharmony/entrada.py` | Pendiente |
