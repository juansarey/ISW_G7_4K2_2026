# Asignación de casos

Completar el responsable antes de comenzar un caso y actualizar el estado al
terminarlo (regla 16). Un caso está **terminado** cuando sus tests pasan junto con la
suite, respetan Ruff y tienen trazabilidad y evidencia en `TP06-TST-EcoHarmony-Registro-TDD.md`.

| Caso | Tema | Responsable                     | Depende de | Estado    |
|---|---|---------------------------------|---|-----------|
| C01 | Compra válida en efectivo | Bongiorno (98495)               | — | Terminado |
| C02 | Compra válida con tarjeta | Bongiorno (98495)               | C01 | Terminado |
| C03 | Fecha actual | Thomas Salomon Wendler (400501) | C01 | Terminado |
| C04 | Fecha futura | Thomas Salomon Wendler (400501) | C01 | Terminado |
| C05 | Una entrada | Por asignar                     | C01 | Pendiente |
| C06 | Nueve entradas | Por asignar                     | C01 | Pendiente |
| C07 | Diez entradas | Por asignar                     | C01 | Pendiente |
| C08 | Pase VIP | Por asignar                     | C01 | Pendiente |
| C09 | Pase regular | Máximo Samir Tabares (402064)   | C01 | Terminado |
| C10 | Fecha pasada | Máximo Samir Tabares (402064)   | C01 | Terminado |
| C11 | Parque cerrado | Martina Lenta (95294)           | C01 | Terminado |
| C12 | Más de diez entradas | Martina Lenta (95294)           | C01 | Terminado |
| C13 | Forma de pago ausente | Tomas Zengaro (403344)          | C01 | Terminado |
| C14 | Usuario no registrado | Tomas Zengaro (403344)          | C01 | Terminado |
| C15 | Fecha ausente | Nicolas Steffolani (94196)      | C01 | Terminado |
| C16 | Edades incompletas | Nicolas Steffolani (94196)      | C01 | Terminado |
| C17 | Tipo de pase ausente | Santiago Adaime (91316)         | C01 | Terminado |
| C18 | Cantidad ausente | Santiago Adaime (91316)                     | C01 | Terminado |
| C19 | Correo de confirmación | Lucas Schoninger (97927)       | C01, C02; contrato §7 | Terminado |
| C20 | Resumen de la compra | Lucas Schoninger (97927)       | C01, C08 | Terminado |
| C21 | Inicio del pago con tarjeta | Juan Pablo Sacco Rey (89319)   | C02 | Terminado |
| C22 | Efectivo sin redirección | Juan Pablo Sacco Rey (89319)   | C01 | Terminado |
| C23 | Rechazo sin efectos | Facundo Montes (406511)                     | C12 | Terminado |
| C24 | Redirección no acredita pago | Facundo Montes (406511)                     | C02 | Terminado |
| C25 | Cantidad no entera positiva (DG01) | Máximo Rossa (400034)                     | C18; `ecoharmony/entrada.py` | Terminado |
| C26 | Opción no admitida (DG02) | Máximo Rossa (400034)                     | `ecoharmony/entrada.py` | Terminado |
| C27 | Fecha con formato inválido (DG03) | Emanuel Tejeda (401000)         | `ecoharmony/entrada.py` | Terminado |
| C28 | Edad inválida (DG04) | Emanuel Tejeda (401000)         | C16; `ecoharmony/entrada.py` | Terminado |
