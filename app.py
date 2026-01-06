import streamlit as st
import numpy as np

st.set_page_config(page_title="Gauss-Jordan", layout="centered")

st.title("📘 Método de Gauss-Jordan")
st.markdown("Resolución de sistemas de ecuaciones paso a paso")
st.markdown("**Desarrollado por Ing Orlando Ramirez Rodriguez**")
st.divider()

orden = st.selectbox("Seleccione el tamaño del sistema", ["2×2", "3×3"])

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

if st.button("Aplicar método de Gauss-Jordan"):
    pasos, resultado = gauss_jordan(M.copy())

    st.subheader("📗 Desarrollo paso a paso")
    for p in pasos:
        if isinstance(p, str):
            st.markdown(f"**{p}**")
        else:
            st.table(p)

    if resultado is not None:
        st.subheader("✅ Solución del sistema")
        for i in range(resultado.shape[0]):
            st.write(f"x{i+1} = {resultado[i, -1]:.3f}")