import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.rag import answer
import streamlit as st


st.title("My Chatbot" )

# answer part
q = st.text_input( 'What is your question : ')
if  st.button("Ask" ) or q:
    with st.spinner(' Processing...'):
        res = answer(q )

    st.markdown( res["answer" ] )


    with st.expander("Sources" ):
        for  s in res["sources" ]:
            st.write( f"- {s['title'  ]}")