#python -m streamlit run desafio7.py

# Importaciones: (librerías)
import streamlit as st
from groq import Groq


st.set_page_config(page_title="Mi página", page_icon="🦎", layout="centered")

# Estado de Sesión:
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# Opción de ingresar nombre:
Nombre = st.text_input("¿Cuál es tu nombre?")

# Opción de Saludar:
if st.button("Saludar"):
    st.write(f"¡Hola, {Nombre}! ¿Qué necesitás saber?")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def configurar_pagina():
 
    # Agregamos un título principal a nuestra página
    st.title("Mela")

    #barra lateral
    st.sidebar.title("Configuración de la IA") # Creamos un sidebar con un título.
    elegirModelo =  st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

# Título de la página:
st.title("¡ChatBot!")



# Conectar con Groq:
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

# Modelos:
def Configurar_Modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
      model=modelo,
      messages=[{"role": "user", "content": mensajeDeEntrada}],
      stream=True
      )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#actualizar historial
def actualizar_historial(rol, contenido, avatar):
        st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

#mostrar historial
def mostrar_historial():
        for mensaje in st.session_state.mensajes:
                with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
                        st.markdown(mensaje["content"])

#AREA DE CHAT
def area_chat():
        contenedorDelChat = st.container(height=400,border=True)
        # Abrimos el contenedor del chat y mostramos el historial.
        with contenedorDelChat:
                mostrar_historial()


#GENERAR RESPUESTA
def generar_respuesta(chat_completo):
      respuesta_completa = ""
      for frase in chat_completo:
          if frase.choices[0].delta.content:
               respuesta_completa += frase.choices[0].delta.content
               yield frase.choices[0].delta.content
      return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()

# Tomamos el mensaje del usuario por el input.
    mensaje = st.chat_input("Escribí tu mensaje: ")
    # print(mensaje)
    # Verifica que el mensaje no esté vacío antes de configurarel modelo
    area_chat()
   
    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")

        chat_completo = Configurar_Modelo(clienteUsuario, modelo, mensaje)

        actualizar_historial("assistant", chat_completo,"🤖")

    st.rerun()

#llamar a la funcion para que revise todo
if __name__ == "__main__":
     main()
     

