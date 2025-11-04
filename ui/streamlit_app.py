import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.rag import answer
import streamlit as st


# logo
st.set_page_config( page_title="Ateme Chatbot")

if st.get_option('theme.base') == "dark":
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
else :
    logo_path = os.path.join(os.path.dirname(__file__), "logo-modified.png")


from PIL import Image


logo = Image.open(logo_path)
st.image(logo, width=180)



st.title("AtemeChat" )

# answer part
q = st.text_input( 'Quelle est ta question sur Ateme ou le stage')
if  st.button("Ask" ) or q:
    with st.spinner(' Processing...'):
        res = answer(q )

    st.markdown( res["answer" ] )


    with st.expander("Sources" ):
        for  s in res["sources" ]:
            st.write( f"- {s['title'  ]}")