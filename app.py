import gradio as gr

from rag_ley.pipeline import LegalRAG


rag = LegalRAG()

BRAND_CSS = """
:root {
  --ink: #101b2d;
  --navy: #10233f;
  --navy-soft: #1a3559;
  --gold: #b9975b;
  --gold-soft: #e8dcc4;
  --paper: #f5f3ef;
  --white: #ffffff;
  --muted: #677286;
  --line: #dfe3e8;
}

.gradio-container {
  background:
    radial-gradient(circle at 90% 2%, rgba(185, 151, 91, .12), transparent 22rem),
    linear-gradient(180deg, #f8f7f4 0%, #f2f4f7 100%);
  color: var(--ink);
  font-family: Inter, "Segoe UI", Arial, sans-serif;
}

.app-shell { max-width: 1180px !important; margin: 0 auto !important; padding: 26px 24px 12px !important; }
.hero {
  position: relative;
  overflow: hidden;
  padding: 38px 42px;
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 22px;
  background: linear-gradient(135deg, #0d1b2e 0%, #132b49 68%, #1c3c61 100%);
  box-shadow: 0 24px 60px rgba(16, 35, 63, .18);
}
.hero::after {
  content: ""; position: absolute; width: 280px; height: 280px; right: -80px; top: -125px;
  border: 1px solid rgba(185,151,91,.28); border-radius: 50%; box-shadow: 0 0 0 38px rgba(185,151,91,.05);
}
.eyebrow { color: #dbc69e; font-size: 12px; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }
.hero h1 { margin: 10px 0 8px; color: white; font-size: clamp(30px, 4vw, 46px); line-height: 1.08; letter-spacing: -.035em; }
.hero p { max-width: 760px; margin: 0; color: #cfdae7; font-size: 16px; line-height: 1.65; }
.trust-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
.trust-chip { padding: 7px 11px; border: 1px solid rgba(219,198,158,.25); border-radius: 999px; color: #e6dcc9; background: rgba(255,255,255,.055); font-size: 12px; }

.workspace { gap: 20px !important; margin-top: 22px; align-items: stretch; }
.premium-card {
  padding: 22px !important; border: 1px solid var(--line) !important; border-radius: 18px !important;
  background: rgba(255,255,255,.94) !important; box-shadow: 0 12px 34px rgba(16,35,63,.07) !important;
}
.section-kicker { color: var(--gold); font-size: 11px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; }
.section-title { margin: 3px 0 15px; color: var(--navy); font-size: 21px; font-weight: 720; letter-spacing: -.02em; }
.legal-input textarea { min-height: 178px !important; font-size: 16px !important; line-height: 1.6 !important; }
.legal-input, .answer-panel { border-color: #d9dee6 !important; border-radius: 12px !important; }
.answer-panel { min-height: 305px; padding: 10px 14px !important; background: #fbfcfd !important; }
.answer-panel h1, .answer-panel h2, .answer-panel h3 { color: var(--navy) !important; }
.answer-panel blockquote { border-left-color: var(--gold) !important; background: #f7f3eb !important; }
.processing-status {
  min-height: 28px; margin: 2px 0 8px !important; color: var(--navy) !important;
  font-size: 13px !important; font-weight: 700 !important;
}
.processing-status p { margin: 0 !important; }
.primary-action { border: 0 !important; border-radius: 10px !important; background: linear-gradient(135deg, #142c4b, #1c416c) !important; color: white !important; font-weight: 700 !important; box-shadow: 0 8px 18px rgba(20,44,75,.18) !important; }
.primary-action:hover { transform: translateY(-1px); box-shadow: 0 11px 24px rgba(20,44,75,.24) !important; }
.secondary-action { border-radius: 10px !important; border-color: #cfd5dd !important; color: var(--navy) !important; }
.examples-title { margin-top: 18px; color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.disclaimer { margin: 18px 3px 0; padding: 14px 17px; border-left: 3px solid var(--gold); color: #5d6878; background: rgba(255,255,255,.58); font-size: 12px; line-height: 1.55; }
.footer { padding: 18px 2px 8px; color: #7a8493; font-size: 11px; text-align: center; letter-spacing: .025em; }
footer { display: none !important; }

@media (max-width: 768px) {
  .app-shell { padding: 14px 12px !important; }
  .hero { padding: 28px 24px; border-radius: 17px; }
  .premium-card { padding: 17px !important; }
}
"""


def answer_question(question: str) -> str:
    """Presenta la respuesta del motor RAG sin exponer errores internos al usuario."""
    try:
        return rag.answer(question)
    except Exception:
        return (
            "### Servicio temporalmente no disponible\n\n"
            "No fue posible completar la consulta. Intenta nuevamente en unos instantes."
        )


with gr.Blocks(
    title="Proyecto RAG Ley 19.628",
    fill_height=True,
) as demo:
    with gr.Column(elem_classes="app-shell"):
        gr.HTML(
            """
            <header class="hero">
              <div class="eyebrow">Inteligencia jurídica · Chile</div>
              <h1>Proyecto RAG Ley 19.628</h1>
              <p>Consulta la Ley 19.628 mediante recuperación documental asistida por IA,
              con respuestas concisas y referencia al articulo utilizado.</p>
              <div class="trust-row">
                <span class="trust-chip">Base legal consolidada</span>
                <span class="trust-chip">Respuesta con artículos</span>
                <span class="trust-chip">Búsqueda semántica</span>
              </div>
            </header>
            """
        )

        with gr.Row(elem_classes="workspace"):
            with gr.Column(scale=5, elem_classes="premium-card"):
                gr.HTML('<div class="section-kicker">Nueva consulta</div><div class="section-title">¿Qué necesitas revisar?</div>')
                question = gr.Textbox(
                    label="Pregunta jurídica",
                    placeholder="Ej.: ¿Cómo debe otorgarse el consentimiento para tratar datos personales?",
                    lines=6,
                    max_lines=10,
                    elem_classes="legal-input",
                )
                with gr.Row():
                    clear = gr.Button("Limpiar", elem_classes="secondary-action")
                    submit = gr.Button("Consultar la ley", variant="primary", elem_classes="primary-action")

                gr.HTML('<div class="examples-title">Consultas frecuentes</div>')
                gr.Examples(
                    examples=[
                        "¿Qué es un dato personal sensible?",
                        "¿Cómo debe ser el consentimiento para tratar mis datos?",
                        "¿Qué infracción es grave y qué multa arriesga?",
                    ],
                    inputs=question,
                    label="Preguntas sugeridas",
                )

            with gr.Column(scale=7, elem_classes="premium-card"):
                gr.HTML('<div class="section-kicker">Análisis documental</div><div class="section-title">Respuesta fundamentada</div>')
                processing_status = gr.Markdown("", elem_classes="processing-status")
                answer = gr.Markdown(
                    value="_La respuesta aparecerá aquí después de realizar una consulta._",
                    elem_classes="answer-panel",
                )

        gr.HTML(
            """
            <aside class="disclaimer"><strong>Nota de responsabilidad.</strong> Esta herramienta facilita la
            consulta documental y no constituye asesoría jurídica. Verifica siempre la respuesta con el texto
            oficial vigente y, cuando corresponda, con un profesional competente.</aside>
            <div class="footer">RAG Ley 19.628 · Entorno productivo seguro · Grupo 1</div>
            """
        )

    submit.click(
        lambda: "Procesando la consulta",
        outputs=processing_status,
        queue=False,
    ).then(
        answer_question,
        inputs=question,
        outputs=answer,
        show_progress="minimal",
    ).then(lambda: "", outputs=processing_status, queue=False)

    question.submit(
        lambda: "Procesando la consulta",
        outputs=processing_status,
        queue=False,
    ).then(
        answer_question,
        inputs=question,
        outputs=answer,
        show_progress="minimal",
    ).then(lambda: "", outputs=processing_status, queue=False)
    clear.click(
        lambda: ("", "", "_La respuesta aparecerá aquí después de realizar una consulta._"),
        outputs=[question, processing_status, answer],
        queue=False,
    )


if __name__ == "__main__":
    demo.queue(default_concurrency_limit=20, max_size=30).launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Base(
            primary_hue="blue",
            neutral_hue="slate",
            font=[gr.themes.GoogleFont("Inter"), "Arial", "sans-serif"],
        ),
        css=BRAND_CSS,
    )
