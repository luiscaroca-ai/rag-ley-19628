import gradio as gr

from rag_ley.pipeline import LegalRAG

rag = LegalRAG()

demo = gr.Interface(
    fn=rag.answer,
    inputs=gr.Textbox(label="Tu pregunta", placeholder="¿Qué es un dato personal sensible?"),
    outputs=gr.Markdown(label="Respuesta con fuente"),
    title="Asistente RAG · Ley 19.628",
    description="Responde usando el texto consolidado de la ley y cita el artículo.",
    examples=[
        "¿Qué es un dato personal sensible?",
        "¿Cómo debe ser el consentimiento para tratar mis datos?",
        "¿Qué infracción es grave y qué multa arriesga?",
    ],
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
