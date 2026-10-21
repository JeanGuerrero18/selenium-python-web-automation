# Selenium Python – Automatización web

Framework de automatización UI con **Selenium 4 + Python + pytest + pytest-html + pytest-xdist**. Es la versión Python del proyecto `selenium-java-web-automation`: mismos sitios, mismos 28 casos y mismas prácticas.

| Sitio | Qué cubre | Carpeta |
|---|---|---|
| [SauceDemo](https://www.saucedemo.com/) | Flujos E2E de negocio: login, catálogo, carrito, checkout | `tests/saucedemo` |
| [The Internet](https://the-internet.herokuapp.com/) | Técnicas de Selenium aisladas: alerts, ventanas, frames, uploads, hovers, tablas, esperas | `tests/theinternet` |

## Requisitos

- Python 3.10+ (probado con 3.12)
- Chrome, Firefox y/o Edge instalados (los drivers los descarga **Selenium Manager** automáticamente)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
```

## Ejecución

```bash
pytest                                   # todo, 4 workers en paralelo, Chrome visible
pytest --headless                        # sin ventana
pytest --browser firefox                 # chrome | firefox | edge
pytest -m smoke                          # solo el grupo smoke
pytest tests/saucedemo                   # solo SauceDemo
pytest tests/theinternet                 # solo The Internet
pytest tests/saucedemo/test_checkout.py  # un archivo
pytest -n 0                              # en serie (útil para depurar)
ruff check . && ruff format --check .    # lint (debe quedar en 0 issues)
```

Reporte: `reports/report.html`. Es un HTML autocontenido con columna de descripción (docstring del test), metadatos de navegador/SO, pasos de cada test (log capturado) y captura de pantalla en los fallos.

## Estructura

```
framework/            ← núcleo reutilizable, sin nada de un sitio concreto
  config.py           opción CLI > variable de entorno > config.ini
  browser.py          navegadores soportados
  driver_factory.py   Chrome / Firefox / Edge (headless, tamaño de ventana, prefs)
  base_page.py        esperas explícitas y helpers comunes
pages/<sitio>/        Page Objects (y componentes, p. ej. HeaderComponent)
tests/<sitio>/        tests + conftest.py con fixtures del sitio
data/                 datos de prueba y archivos (upload)
conftest.py           fixture `driver`, opciones --browser/--headless y hooks de pytest-html
config.ini            valores por defecto
```

## Buenas prácticas aplicadas

- **Page Object Model** con métodos fluidos que devuelven la siguiente página; los tests no contienen locators.
- **Solo esperas explícitas** (`WebDriverWait`); nunca `implicitly_wait` ni `time.sleep`.
- **Un navegador por test** mediante la fixture `driver` → tests independientes. El paralelismo es por **procesos** (xdist), así que no hace falta estado por hilo.
- **Fixtures por sitio** (`login_page`, `inventory`) para preparar el estado sin repetir pasos.
- **Locators estables**: ids y clases semánticas; productos y filas de tabla se buscan por texto visible.
- **Data-driven** con `@pytest.mark.parametrize` e ids legibles.
- **Markers** `smoke` / `regression`, con `--strict-markers` para que un marker mal escrito falle.
- **Configuración externa**: todo se puede sobrescribir con variables de entorno (p. ej. `SAUCEDEMO_PASSWORD`). Las credenciales del repo son las demo públicas que muestra cada sitio; en una aplicación real van en secretos de CI.
- **Los logs no muestran contraseñas** (solo el usuario de prueba).
- **Versiones fijadas** en `requirements*.txt` y **lint con Ruff** a 0 issues como paso previo del CI.

## Notas técnicas

- **Windows y rutas largas:** si la carpeta del proyecto está muy anidada, la ruta a `.venv\...\selenium-manager.exe` puede superar los 260 caracteres y Selenium falla con `WinError 206` / `Unable to obtain driver`. Usa una ruta corta (p. ej. `Documents\selenium-python-web-automation`) o define `SE_MANAGER_PATH` apuntando a un `selenium-manager.exe` en una ruta corta.
- La advertencia de Selenium Manager sobre `se-metadata.json` al arrancar en paralelo es inocua (varios procesos escriben su caché a la vez).

## CI

`.github/workflows/ui-tests.yml`: primero un job de lint (Ruff); luego la suite en headless con una matriz Chrome / Firefox / Edge en `ubuntu-latest`. El reporte HTML de cada navegador se publica como artefacto, incluso si hay fallos. Se puede lanzar manualmente filtrando por marker (por ejemplo `smoke`).
