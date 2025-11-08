# tu_app/management/commands/import_maestros.py
import json
from pathlib import Path
from typing import Iterable, Dict, Any, Tuple

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.timezone import now

from Clinica.models import (
    Pais, Municipio, Ocupacion, Etnia, Comunidad_Etnica, Discapacidad,
    Tipo_documento, Entidad_Prestadora_Salud,
    Modalidad_Realizacion_Tecnologia_Salud, Via_Ingreso_Servicio_Salud,
    Motivo_Atencion, Enfermedad_Huerfana, Diagnostico, Paciente, Paciente_Pais, Paciente_Discapacidad
)

# -------- Utilidades de IO -------- #

def read_table(path_str: str) -> pd.DataFrame:
    """
    Lee CSV/XLSX/JSON y retorna un DataFrame. Normaliza NaN a ''.
    Para JSON acepta lista de dicts o dict con clave 'rows'.
    """
    if not path_str:
        return pd.DataFrame()
    path = Path(path_str)
    if not path.exists():
        raise CommandError(f"Archivo no existe: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    elif suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path, dtype=str, engine="openpyxl")
    elif suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        rows = data if isinstance(data, list) else data.get("rows", [])
        df = pd.DataFrame(rows, dtype=str)
    else:
        raise CommandError(f"Formato no soportado: {suffix}")

    # Normaliza: quita espacios alrededor y reemplaza NaN por ''
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.fillna("")
    return df

def ensure_columns(df: pd.DataFrame, required: Iterable[str], label: str):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise CommandError(f"[{label}] Faltan columnas requeridas: {missing}")

# -------- Importadores (uno por modelo) -------- #

def upsert_simple(df: pd.DataFrame, model, key: str, fields_map: Dict[str, str]) -> Tuple[int, int]:
    """
    Import genérico para modelos sin FKs.
    - key: nombre del campo clave (PK o único) en el modelo (y en el archivo).
    - fields_map: mapea columna_archivo -> campo_modelo
    Retorna (created, updated).
    """
    created = updated = 0
    for _, row in df.iterrows():
        lookup = {key: row[key]}
        defaults = {to: row[fr] for fr, to in fields_map.items()}
        obj, was_created = model.objects.update_or_create(**lookup, defaults=defaults)
        if was_created:
            created += 1
        else:
            updated += 1
    return created, updated

def import_pacientes(df: pd.DataFrame):
    created = updated = 0

    for _, row in df.iterrows():
        paciente_uuid = row["paciente_UUID"]

        # RESOLVER FK
        defaults = {
            "numero_documento": row["numero_documento"],
            "primer_nombre": row["primer_nombre"],
            "segundo_nombre": row["segundo_nombre"],
            "primer_apellido": row["primer_apellido"],
            "segundo_apellido": row["segundo_apellido"],
            "fecha_nacimiento": row["fecha_nacimiento"],

            # FK -> código_id
            "sexo_biologico_id": row["sexo_biologico"],
            "identidad_genero_id": row["identidad_genero"],
            "zona_territorial_residencia_id": row["zona_territorial_residencia"],
            "tipo_documento_id": row["tipo_documento"],
            "residencia_id": row["residencia"],
            "ocupacion_id": row["ocupacion"],
            "etnia_id": row["etnia"],
            "comunidad_Etnica_id": row["comunidad_Etnica"] or None,
            "entidad_prestadora_salud_id": row["entidad_prestadora_salud"]
        }

        obj, was_created = Paciente.objects.update_or_create(
            paciente_UUID=paciente_uuid,
            defaults=defaults
        )

        if was_created:
            created += 1
        else:
            updated += 1

    return created, updated

def import_paciente_pais(df: pd.DataFrame):
    created = updated = 0
    for _, row in df.iterrows():
        paciente = Paciente.objects.get(paciente_UUID=row["paciente_UUID"])
        pais = Pais.objects.get(codigo_pais=row["codigo_pais"])

        _, was_created = Paciente_Pais.objects.update_or_create(
            paciente_UUID=paciente,
            codigo_pais=pais
        )

        if was_created:
            created += 1
        else:
            updated += 1
    return created, updated

def import_paciente_discapacidad(df: pd.DataFrame):
    created = updated = 0

    for _, row in df.iterrows():
        paciente = Paciente.objects.get(paciente_UUID=row["paciente_UUID"])
        disc = Discapacidad.objects.get(id_discapacidad=row["id_discapacidad"])

        _, was_created = Paciente_Discapacidad.objects.update_or_create(
            paciente_UUID=paciente,
            id_discapacidad=disc
        )

        if was_created:
            created += 1
        else:
            updated += 1

    return created, updated


class Command(BaseCommand):
    help = "Importa catálogos maestros (idempotente) desde CSV/XLSX/JSON para tus modelos."

    def add_arguments(self, parser):
        # Un argumento por catálogo (opcional, para cargar solo lo que necesites).
        parser.add_argument("--paciente", type=str, help="Archivo de Pacientes")
        parser.add_argument("--paciente_pais", type=str, help="Tabla de paciente_pais")
        parser.add_argument("--paciente_discapacidad", type=str, help="Tabla de paciente_discapacidad")
        parser.add_argument("--pais", type=str, help="Archivo de País (codigo_pais, nombre_pais)")
        parser.add_argument("--municipio", type=str, help="Archivo de Municipio (codigo_municipio, nombre_municipio)")
        parser.add_argument("--ocupacion", type=str, help="Archivo de Ocupación (codigo_ocupacion, nombre_ocupacion)")
        parser.add_argument("--etnia", type=str, help="Archivo de Etnia (identificador_etnia, nombre_etnia)")
        parser.add_argument("--comunidad", type=str, help="Archivo de Comunidad Étnica (codigo_comunidad_etnica, nombre_comunidad_etnica)")
        parser.add_argument("--discapacidad", type=str, help="Archivo de Discapacidad (id_discapacidad, nombre_discapacidad)")
        parser.add_argument("--tipo_doc", type=str, help="Archivo de Tipo de Documento (codigo_tipo_documento, nombre_tipo_documento)")
        parser.add_argument("--entidad_prestadora", type=str,
                            help="Archivo de Entidad Prestadora de Salud (codigo_entidad_prestadora, nombre_entidad_prestadora, es_eps, es_ips, es_arl, es_aseguradora)")
        parser.add_argument("--modalidad_tec", type=str,
                            help="Archivo Modalidad Realización TS (codigo_modalidad_realizacion_tecnologia_salud, nombre_modalidad_realizacion_tecnologia_salud)")
        parser.add_argument("--via_ingreso", type=str,
                            help="Archivo Vía de Ingreso (codigo_via_ingreso_usuario_servicio_salud, nombre_via_ingreso_usuario_servicio_salud)")
        parser.add_argument("--motivo_atencion", type=str,
                            help="Archivo Motivo de Atención (codigo_causa_motivo_atencion, nombre_causa_motivo_atencion)")
        parser.add_argument("--enf_huerfana", type=str,
                            help="Archivo Enfermedad Huérfana (codigo_enfermedad_huerfana, nombre_enfermedad_huerfana)")
        parser.add_argument("--diagnostico", type=str,
                            help="Archivo Diagnóstico (codigo_diagnostico, nombre_diagnostico)")

        parser.add_argument("--dry-run", action="store_true", help="Valida sin escribir cambios")
        parser.add_argument("--batch", type=int, default=0, help="(Opcional) No usado aquí; placeholder para futuras optimizaciones")

    def handle(self, *args, **opts):
        start = now()
        dry = opts["dry_run"]

        # Carga de DataFrames + validación de columnas requeridas
        loaders = []

        def add(label, path, required, fn):
            if path:
                df = read_table(path)
                ensure_columns(df, required, label)
                loaders.append((label, df, fn))

        add("paciente", opts["paciente"], [
            "paciente_UUID", "numero_documento",
            "primer_nombre", "segundo_nombre",
            "primer_apellido", "segundo_apellido",
            "fecha_nacimiento",
            "sexo_biologico", "identidad_genero",
            "zona_territorial_residencia",
            "tipo_documento", "residencia",
            "ocupacion", "etnia",
            "comunidad_Etnica",
            "entidad_prestadora_salud"
        ], import_pacientes)

        add("paciente_pais", opts["paciente_pais"],
            ["paciente_UUID", "codigo_pais"],
            import_paciente_pais)

        add("paciente_discapacidad", opts["paciente_discapacidad"],
            ["paciente_UUID", "id_discapacidad"],
            import_paciente_discapacidad)

        add("pais", opts["pais"], ["codigo_pais", "nombre_pais"],
            lambda df: upsert_simple(df, Pais, "codigo_pais", {"nombre_pais": "nombre_pais"}))

        add("municipio", opts["municipio"], ["codigo_municipio", "nombre_municipio"],
            lambda df: upsert_simple(df, Municipio, "codigo_municipio", {"nombre_municipio": "nombre_municipio"}))

        add("ocupacion", opts["ocupacion"], ["codigo_ocupacion", "nombre_ocupacion"],
            lambda df: upsert_simple(df, Ocupacion, "codigo_ocupacion", {"nombre_ocupacion": "nombre_ocupacion"}))

        add("etnia", opts["etnia"], ["identificador_etnia", "nombre_etnia"],
            lambda df: upsert_simple(df, Etnia, "identificador_etnia", {"nombre_etnia": "nombre_etnia"}))

        add("comunidad_etnica", opts["comunidad"], ["codigo_comunidad_etnica", "nombre_comunidad_etnica"],
            lambda df: upsert_simple(df, Comunidad_Etnica, "codigo_comunidad_etnica", {"nombre_comunidad_etnica": "nombre_comunidad_etnica"}))

        add("discapacidad", opts["discapacidad"], ["id_discapacidad", "nombre_discapacidad"],
            lambda df: upsert_simple(df, Discapacidad, "id_discapacidad", {"nombre_discapacidad": "nombre_discapacidad"}))

        add("tipo_documento", opts["tipo_doc"], ["codigo_tipo_documento", "nombre_tipo_documento"],
            lambda df: upsert_simple(df, Tipo_documento, "codigo_tipo_documento", {"nombre_tipo_documento": "nombre_tipo_documento"}))

        add("entidad_prestadora_salud", opts["entidad_prestadora"],
            ["codigo_entidad_prestadora", "nombre_entidad_prestadora", "es_eps", "es_ips", "es_arl", "es_aseguradora"],
            lambda df: upsert_simple(df, Entidad_Prestadora_Salud, "codigo_entidad_prestadora", {
                "nombre_entidad_prestadora": "nombre_entidad_prestadora",
                "es_eps": "es_eps",
                "es_ips": "es_ips",
                "es_arl": "es_arl",
                "es_aseguradora": "es_aseguradora",
            }))

        add("modalidad_realizacion_tecnologia_salud", opts["modalidad_tec"],
            ["codigo_modalidad_realizacion_tecnologia_salud", "nombre_modalidad_realizacion_tecnologia_salud"],
            lambda df: upsert_simple(df, Modalidad_Realizacion_Tecnologia_Salud,
                                     "codigo_modalidad_realizacion_tecnologia_salud",
                                     {"nombre_modalidad_realizacion_tecnologia_salud": "nombre_modalidad_realizacion_tecnologia_salud"}))

        add("via_ingreso_servicio_salud", opts["via_ingreso"],
            ["codigo_via_ingreso_usuario_servicio_salud", "nombre_via_ingreso_usuario_servicio_salud"],
            lambda df: upsert_simple(df, Via_Ingreso_Servicio_Salud,
                                     "codigo_via_ingreso_usuario_servicio_salud",
                                     {"nombre_via_ingreso_usuario_servicio_salud": "nombre_via_ingreso_usuario_servicio_salud"}))

        add("motivo_atencion", opts["motivo_atencion"],
            ["codigo_causa_motivo_atencion", "nombre_causa_motivo_atencion"],
            lambda df: upsert_simple(df, Motivo_Atencion, "codigo_causa_motivo_atencion",
                                     {"nombre_causa_motivo_atencion": "nombre_causa_motivo_atencion"}))

        add("enfermedad_huerfana", opts["enf_huerfana"],
            ["codigo_enfermedad_huerfana", "nombre_enfermedad_huerfana"],
            lambda df: upsert_simple(df, Enfermedad_Huerfana, "codigo_enfermedad_huerfana",
                                     {"nombre_enfermedad_huerfana": "nombre_enfermedad_huerfana"}))

        add("diagnostico", opts["diagnostico"],
            ["codigo_diagnostico", "nombre_diagnostico"],
            lambda df: upsert_simple(df, Diagnostico, "codigo_diagnostico",
                                     {"nombre_diagnostico": "nombre_diagnostico"}))

        if not loaders:
            raise CommandError("No se especificó ningún archivo. Usa --help para ver opciones.")

        # Ejecución
        stats = {}
        try:
            with transaction.atomic():
                for label, df, fn in loaders:
                    c, u = fn(df)
                    stats[label] = (c, u)
                if dry:
                    raise CommandError("Dry-run OK: validación y conteos listos; no se guardaron cambios.")
        except CommandError as e:
            # Imprime stats parciales cuando aplica a dry-run
            for label, (c, u) in stats.items():
                self.stdout.write(f"[{label}] created={c} updated={u}")
            raise e

        # Éxito
        for label, (c, u) in stats.items():
            self.stdout.write(self.style.SUCCESS(f"[{label}] created={c} updated={u}"))
        elapsed = (now() - start).total_seconds()
        self.stdout.write(self.style.SUCCESS(f"Importación completa en {elapsed:.2f}s"))