# Guardar el contenido corregido del archivo como app.py
codigo_corregido = """
import streamlit as st
import pandas as pd
import openai
import PyPDF2
import io
import base64
import time
from fpdf import FPDF

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Evaluador de Encuestas", page_icon="📊", layout="wide")

st.title("📊 Evaluador de Calidad de Encuestas")
st.markdown("Sube un archivo con preguntas para recibir retroalimentación automática.")

uploaded_file = st.file_uploader("Carga un archivo (CSV, Excel o PDF)", type=["csv", "xlsx", "pdf"])
preguntas = []

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        preguntas = df.iloc[:, 0].dropna().tolist()
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        preguntas = df.iloc[:, 0].dropna().tolist()
    elif uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        texto = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        preguntas = [line.strip() for line in texto.split("\\n") if "?" in line or line.strip().startswith("¿")]

    if preguntas:
        st.success(f"Se detectaron {len(preguntas)} preguntas. Procesando...")
        evaluaciones = []
        puntajes = []
        progress = st.progress(0, text="Evaluando preguntas...")

        for i, pregunta in enumerate(preguntas):
            prompt = f'''
Evalúa la siguiente pregunta de encuesta considerando estos aspectos:
- Claridad
- Pertinencia
- Posibles sesgos
- Recomendación de mejora
- Puntaje del 1 al 10

Pregunta: {pregunta}
'''
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                resultado = response.choices[0].message.content.strip()
                evaluaciones.append((pregunta, resultado))
                linea_puntaje = [l for l in resultado.split("\\n") if "Puntaje" in l or "puntaje" in l]
                if linea_puntaje:
                    try:
                        valor = int("".join([c for c in linea_puntaje[-1] if c.isdigit()]))
                        puntajes.append(valor)
                    except:
                        puntajes.append(0)
                else:
                    puntajes.append(0)
                time.sleep(3)
                progress.progress((i + 1) / len(preguntas), text=f"{i + 1}/{len(preguntas)} completado")
            except Exception as e:
                st.error(f"Error al evaluar la pregunta {i + 1}: {e}")
                evaluaciones.append((pregunta, "Error de evaluación"))
                puntajes.append(0)

        promedio = sum(puntajes) / len(puntajes) if puntajes else 0
        st.success(f"✅ Evaluación completada. Puntaje promedio: {promedio:.1f}/10")

        for i, (preg, evalua) in enumerate(evaluaciones):
            with st.expander(f"Pregunta {i + 1}: {preg}"):
                st.markdown(evalua)

        if st.button("📅 Descargar informe PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Informe de Evaluación de Encuesta\\nPuntaje promedio: {promedio:.1f}/10\\n")
            for idx, (pregunta, evaluacion) in enumerate(evaluaciones):
                contenido = f"Pregunta {idx + 1}: {pregunta}\\nEvaluación: {evaluacion}\\n"
                pdf.multi_cell(0, 10, contenido)
            pdf.multi_cell(0, 10, "Evaluación general del instrumento:\\n")
            pdf.multi_cell(0, 10, "- Introducción clara: Se presenta el propósito de la encuesta y se incluye consentimiento informado.\\n")
            pdf.multi_cell(0, 10, "- Datos sociodemográficos: Preguntas básicas como edad, sexo, ocupación o semestre.\\n")
            pdf.multi_cell(0, 10, "- Coherencia temática: Las preguntas se relacionan directamente con los objetivos de la encuesta.\\n")
            pdf.multi_cell(0, 10, "- Redacción neutral: No inducen respuestas ni contienen juicios de valor.\\n")
            pdf.multi_cell(0, 10, "- Secuencia lógica: Las preguntas avanzan de lo general a lo específico.\\n")
            pdf.multi_cell(0, 10, "- Duración razonable: El número de preguntas no resulta excesivo para el encuestado.\\n")
            pdf.multi_cell(0, 10, "- Uso adecuado de escalas: Se emplean escalas válidas, como Likert, cuando es pertinente.\\n")
            buffer = io.BytesIO()
            pdf.output(buffer)
            b64 = base64.b64encode(buffer.getvalue()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="informe_encuesta.pdf">📄 Descargar PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("No se encontraron preguntas en el archivo.")
else:
    st.info("Carga un archivo para comenzar.")

    st.subheader("📋 Evaluación general del instrumento")
    st.markdown(\"""
- 📌 **Introducción clara**: Se presenta el propósito de la encuesta y se incluye consentimiento informado.
- 👤 **Datos sociodemográficos**: Preguntas básicas como edad, sexo, ocupación o semestre.
- 🔍 **Coherencia temática**: Las preguntas se relacionan directamente con los objetivos de la encuesta.
- 📐 **Redacción neutral**: No inducen respuestas ni contienen juicios de valor.
- 🔀 **Secuencia lógica**: Las preguntas avanzan de lo general a lo específico.
- ⏳ **Duración razonable**: El número de preguntas no resulta excesivo para el encuestado.
- 📊 **Uso adecuado de escalas**: Se emplean escalas válidas, como Likert, cuando es pertinente.
\""\")
"""

# Guardar archivo

    f.write(codigo_corregido)

file_path
