import streamlit as st
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Método de Gauss-Jordan",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("## 📘 Método de Gauss-Jordan")
st.markdown(
    "<p style='font-size:16px;'>Resolución de sistemas de ecuaciones lineales mediante operaciones elementales por filas</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<b>Desarrollado por Ing Orlando Ramirez Rodriguez</b>",
    unsafe_allow_html=True
)
st.divider()

# =========================
# FUNCIONES AUXILIARES
# =========================
def mostrar_matriz(M):
    return np.round(M, 3)

def gauss_jordan(M):
    pasos = []
    filas, cols = M.shape

    pasos.append("Matriz inicial:")
    pasos.append(mostrar_matriz(M.copy()))

    for i in range(filas):
        pivote = M[i, i]

        if pivote == 0:
            pasos.append(f"No se puede continuar: pivote nulo en fila {i+1}")
            return pasos, None

        pasos.append(f"Paso {len(pasos)//2 + 1}: F{i+1} → F{i+1} / {pivote}")
        M[i] = M[i] / pivote
        pasos.append(mostrar_matriz(M.copy()))

        for j in range(filas):
            if j != i:
                factor = M[j, i]
                pasos.append(
                    f"Paso {len(pasos)//2 + 1}: F{j+1} → F{j+1} − ({factor})·F{i+1}"
                )
                M[j] = M[j] - factor * M[i]
                pasos.append(mostrar_matriz(M.copy()))

    return pasos, M

def generar_pdf(pasos, clasificacion, solucion):
    nombre_archivo = "gauss_jordan_procedimiento.pdf"
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("<b>Método de Gauss-Jordan</b>", styles["Title"]))
    elementos.append(Spacer(1, 12))
    elementos.append(
        Paragraph(
            "Desarrollado por <b>Ing Orlando Ramirez Rodriguez</b>",
            styles["Normal"]
        )
    )
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("<b>Desarrollo paso a paso</b>", styles["Heading2"]))
    elementos.append(Spacer(1, 10))

    for p in pasos:
        if isinstance(p, str):
            elementos.append(Paragraph(p, styles["Normal"]))
            elementos.append(Spacer(1, 8))
        else:
            tabla = Table(p.tolist())
            elementos.append(tabla)
            elementos.append(Spacer(1, 10))

    elementos.append(Spacer(1, 12))
    elementos.append(
        Paragraph(
            f"<b>Clasificación del sistema:</b> {clasificacion}",
            styles["Normal"]
        )
    )

    if solucion:
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph("<b>Solución:</b>", styles["Normal"]))
        for s in solucion:
            elementos.append(Paragraph(s, styles["Normal"]))

    doc.build(elementos)
    return nombre_archivo

# =========================
# ENTRADA DE DATOS
# =========================
orden = st.selectbox(
    "Seleccione el tamaño del sistema de ecuaciones lineales",
    ["2×2", "3×3"]
)

if orden == "2×2":
    st.subheader("Ingrese la matriz aumentada 2×3")
    M = np.array([
        [st.number_input("a11"), st.number_input("a12"), st.number_input("b1")],
        [st.number_input("a21"), st.number_input("a22"), st.number_input("b2")]
    ], dtype=float)

if orden == "3×3":
    st.subheader("Ingrese la matriz aumentada 3×4")
    M = np.array([
        [st.number_input("a11"), st.number_input("a12"), st.number_input("a13"), st.number_input("b1")],
        [st.number_input("a21"), st.number_input("a22"), st.number_input("a23"), st.number_input("b2")],
        [st.number_input("a31"), st.number_input("a32"), st.number_input("a33"), st.number_input("b3")]
    ], dtype=float)

# =========================
# PROCESAMIENTO
# =========================
if st.button("Aplicar método de Gauss-Jordan"):
    pasos, resultado = gauss_jordan(M.copy())

    st.subheader("📗 Desarrollo paso a paso")
    for p in pasos:
        if isinstance(p, str):
            st.markdown(f"**{p}**")
        else:
            st.table(p)

    clasificacion = ""
    solucion = []

    if resultado is not None:
        filas, cols = resultado.shape
        soluciones = True
        infinitas = False

        for i in range(filas):
            if all(resultado[i, j] == 0 for j in range(cols-1)) and resultado[i, -1] != 0:
                soluciones = False

            if all(resultado[i, j] == 0 for j in range(cols)):
                infinitas = True

        if not soluciones:
            clasificacion = "Sistema incompatible (sin solución)"
            st.subheader("❌ Clasificación del sistema")
            st.write(clasificacion)

        elif infinitas:
            clasificacion = "Sistema compatible indeterminado (infinitas soluciones)"
            st.subheader("⚠️ Clasificación del sistema")
            st.write(clasificacion)

        else:
            clasificacion = "Sistema compatible determinado (solución única)"
            st.subheader("✅ Clasificación del sistema")
            st.write(clasificacion)

            st.subheader("📌 Solución del sistema")
            for i in range(filas):
                texto = f"x{i+1} = {resultado[i, -1]:.3f}"
                solucion.append(texto)
                st.write(texto)

        st.divider()
        if st.button("📄 Exportar procedimiento a PDF"):
            archivo = generar_pdf(pasos, clasificacion, solucion)
            with open(archivo, "rb") as f:
                st.download_button(
                    label="📥 Descargar PDF",
                    data=f,
                    file_name=archivo,
                    mime="application/pdf"
                )

    

   

    
