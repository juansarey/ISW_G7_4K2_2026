"""Aplicación Flask de la demostración.

La interfaz solo recoge datos, llama a ``ServicioCompras`` y presenta el resultado;
las reglas de negocio permanecen en la lógica compartida (regla 12). El reloj, el
calendario, el pago y el correo son simulados y se identifican como tales.
"""

from datetime import date
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException

from ecoharmony.entrada import convertir_solicitud
from ecoharmony.modelos import Compra, ResultadoCompra, TipoPase, Usuario
from ecoharmony.servicio_compras import ServicioCompras
from ecoharmony.simulados import (
    CalendarioParque,
    CorreoSimulado,
    PagoSimulado,
    RelojFijo,
    RepositorioComprasEnMemoria,
)
from ecoharmony.tarifas import MAXIMO_ENTRADAS, TARIFAS_POR_PASE
from ecoharmony.web.mensajes import (
    MENSAJE_ERROR_INTERNO,
    MENSAJE_FORMATO_INVALIDO,
    MENSAJES_RECHAZO,
)

# A01: la demostración usa D0 = 12/06/2030 y el 14/06/2030 es cierre excepcional.
FECHA_DEMOSTRACION = date(2030, 6, 12)
CIERRES_EXCEPCIONALES = {date(2030, 6, 14)}
DIAS_CALENDARIO_VISIBLES = 14

USUARIOS_SIMULADOS: dict[str, Usuario] = {
    "visitante01": Usuario("visitante01", "visitante@example.com", registrado=True),
    "invitado02": Usuario("invitado02", "invitado@example.com", registrado=False),
}

CARPETA_ESTATICOS = Path(__file__).parent / "static"


def crear_app(fecha_actual: date = FECHA_DEMOSTRACION) -> Flask:
    reloj = RelojFijo(fecha_actual)
    calendario = CalendarioParque(CIERRES_EXCEPCIONALES)
    pago = PagoSimulado()
    correo = CorreoSimulado()
    repositorio = RepositorioComprasEnMemoria()
    servicio = ServicioCompras(reloj, calendario, pago, correo, repositorio)

    app = Flask(__name__, static_folder=str(CARPETA_ESTATICOS))

    @app.get("/")
    def pagina_compra():
        return send_from_directory(CARPETA_ESTATICOS, "index.html")

    @app.get("/pasarela-simulada/<id_compra>")
    def pagina_pasarela(id_compra: str):
        return send_from_directory(CARPETA_ESTATICOS, "pasarela.html")

    @app.get("/api/configuracion")
    def configuracion():
        return jsonify(
            fecha_actual=reloj.hoy().isoformat(),
            maximo_entradas=MAXIMO_ENTRADAS,
            usuarios=[
                {
                    "nombre_usuario": usuario.nombre_usuario,
                    "registrado": usuario.registrado,
                }
                for usuario in USUARIOS_SIMULADOS.values()
            ],
            tarifas={
                pase.value: str(monto) for pase, monto in TARIFAS_POR_PASE.items()
            },
            tipos_pase=[pase.value for pase in TipoPase],
            calendario=[
                {"fecha": fecha.isoformat(), "abierto": abierto}
                for fecha, abierto in calendario.proximos_dias(
                    reloj.hoy(), DIAS_CALENDARIO_VISIBLES
                )
            ],
        )

    @app.post("/api/compras")
    def crear_compra():
        datos = request.get_json(silent=True) or {}
        usuario = USUARIOS_SIMULADOS.get(str(datos.get("usuario", "")))
        if usuario is None:
            return jsonify(error="Usuario simulado desconocido."), 400
        try:
            solicitud = convertir_solicitud(datos, usuario)
        except ValueError:
            return jsonify(
                aceptada=False, motivo=None, mensaje=MENSAJE_FORMATO_INVALIDO
            ), 400
        resultado = servicio.comprar(solicitud)
        return jsonify(_resultado_a_dict(resultado))

    @app.get("/api/compras/<id_compra>")
    def consultar_compra(id_compra: str):
        compra = repositorio.obtener(id_compra)
        if compra is None:
            return jsonify(error="Compra inexistente."), 404
        return jsonify(_compra_a_dict(compra))

    @app.get("/api/correos")
    def bandeja_correo_simulado():
        return jsonify([_compra_a_dict(compra) for compra in reversed(correo.enviados)])

    @app.errorhandler(Exception)
    def error_interno(error: Exception):
        # No oculta el error: Flask lo registra en la consola con su traza completa.
        if isinstance(error, HTTPException):
            return error
        app.logger.exception("Error no controlado al procesar la solicitud")
        return jsonify(error=MENSAJE_ERROR_INTERNO, detalle=repr(error)), 500

    return app


def _resultado_a_dict(resultado: ResultadoCompra) -> dict[str, object]:
    return {
        "aceptada": resultado.aceptada,
        "motivo": resultado.motivo.value if resultado.motivo else None,
        "mensaje": MENSAJES_RECHAZO.get(resultado.motivo) if resultado.motivo else None,
        "url_redireccion": resultado.url_redireccion,
        "compra": _compra_a_dict(resultado.compra) if resultado.compra else None,
    }


def _compra_a_dict(compra: Compra) -> dict[str, object]:
    return {
        "id_compra": compra.id_compra,
        "usuario": compra.usuario.nombre_usuario,
        "correo": compra.usuario.correo,
        "fecha_visita": compra.fecha_visita.isoformat(),
        "cantidad_entradas": compra.cantidad_entradas,
        "edades": list(compra.edades),
        "tipo_pase": compra.tipo_pase.value,
        "forma_pago": compra.forma_pago.value if compra.forma_pago else None,
        "total": str(compra.total),
        "estado_compra": compra.estado_compra.value,
        "estado_pago": compra.estado_pago.value,
        "estado_correo": compra.estado_correo.value,
    }
