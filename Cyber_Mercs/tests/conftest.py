# conftest.py — Aísla la DB de tests del archivo de producción.
# Antes los tests escribían sobre `mercenarios.db`, contaminando datos reales.
# Ahora cada sesión de tests usa un archivo temporal que se borra al terminar.

import os
import tempfile

# CRÍTICO: definir DB_PATH ANTES de importar config/main.
# config.py lee la variable al importarse y se cachea.
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["DB_PATH"] = _tmp.name

# Garantizar que CORP_API_KEY existe (config.py falla si no está).
os.environ.setdefault("CORP_API_KEY", "zaun-key-2026")


def pytest_sessionfinish(session, exitstatus):
    """Limpia el archivo de DB temporal al final de la corrida."""
    try:
        os.unlink(_tmp.name)
    except OSError:
        pass
