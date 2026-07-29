# Proyecto RAG · Ley 19.628

Versión para VS Code basada en `Proyecto_RAG_Ley19628_GRUPOvfinal.ipynb`. Implementa chunking por artículo, embeddings OpenAI, almacenamiento vectorial en Qdrant, recuperación amplia, re-ranking por LLM, umbral de relevancia y una interfaz Gradio.

## Requisitos

- Python 3.11 o superior
- Una API key de OpenAI
- Un clúster de Qdrant y su API key
- El texto consolidado `Ley_19628_refundida_21719.txt`

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Completa `.env` con tus credenciales y copia el documento legal a:

```text
data/Ley_19628_refundida_21719.txt
```

## Uso

Primero crea o reemplaza la colección vectorial:

```bash
PYTHONPATH=src python scripts/index_law.py
```

Después inicia la interfaz:

```bash
PYTHONPATH=src python app.py
```

Abre la dirección local que muestra Gradio. En VS Code también puedes presionar `F5` y elegir una de las dos configuraciones incluidas.

> El comando de indexación reemplaza la colección configurada. La aplicación no entrega asesoría jurídica y sus respuestas deben verificarse contra la fuente oficial.

## Ejecución con Docker

Instala Docker Desktop, crea el archivo de configuración y agrega el documento:

```bash
cp .env.example .env
```

Completa las credenciales en `.env` y guarda la ley en
`data/Ley_19628_refundida_21719.txt`.

Construye la imagen:

```bash
docker compose build
```

La primera vez, indexa el documento en Qdrant. Este comando reemplaza únicamente
la colección indicada por `QDRANT_COLLECTION`:

```bash
docker compose --profile tools run --rm index
```

Luego inicia la aplicación:

```bash
docker compose up -d app
```

La interfaz estará disponible en <http://localhost:7860>. Para revisar el estado
y los registros:

```bash
docker compose ps
docker compose logs -f app
```

Para detenerla:

```bash
docker compose down
```

## Estructura

```text
Dockerfile                Imagen de ejecución
compose.yaml              Servicios de aplicación e indexación
app.py                    Interfaz Gradio
scripts/index_law.py      Indexación de la ley en Qdrant
src/rag_ley/chunking.py   División estructural por artículo
src/rag_ley/pipeline.py   Recuperación, re-ranking y generación
src/rag_ley/config.py     Configuración desde .env
tests/                    Pruebas unitarias
notebooks/                Notebook original de referencia
```
