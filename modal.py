from contextlib import contextmanager

import streamlit as st
import streamlit.components.v1 as components


class Modal:

    def __init__(self, title, key, padding=20, max_width=None):
        self.title = title
        self.padding = padding
        self.max_width = max_width
        self.key = key

    def is_open(self):
        return st.session_state.get(f'{self.key}-opened', False)

    def open(self):
        st.session_state[f'{self.key}-opened'] = True
        st.experimental_rerun()

    def close(self, rerun=True):
        st.session_state[f'{self.key}-opened'] = False
        if rerun:
            st.experimental_rerun()

    @contextmanager
    def container(self):
        if self.max_width:
            max_width = str(self.max_width) + "px"
        else:
            max_width = 'unset'

        st.markdown(
            f"""
            <style>
            
            div[data-modal-container='true'][key='{self.key}'] {{
                position: fixed;
                width: 100vw !important;
                max-width: 100vw !important;
                left: 0;
                top: 10%;  <!-- Position of the modal to the top of the page --> 
                z-index: 1001;
            }}
            
            div[data-modal-container='true'][key='{self.key}'] > div:first-child {{
                margin: auto;
            }}

            div[data-modal-container='true'][key='{self.key}'] h1 a {{
                display: none
            }}
            
            div[data-modal-container='true'][key='{self.key}']::before {{
                    position: fixed;
                    content: ' ';
                    left: 0;
                    right: 0;
                    top: 0;
                    bottom: 0;
                    z-index: 1000;
                    background-color: rgba(0, 0, 0, 0.5);
            }}
            
            div[data-modal-container='true'][key='{self.key}'] > div:first-child {{
                max-width: {max_width};
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child {{
                width: unset !important;
                background-color: #fff;
                padding: {self.padding}px;
                margin-top: {2*self.padding}px;
                margin-left: -{self.padding}px;
                margin-right: -{self.padding}px;
                margin-bottom: -{2*self.padding}px;
                z-index: 1001;
                border-radius: 5px;
            }}
             
            div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2)  {{
                z-index: 1003;
                position: absolute;    
            }}
            
            div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2) > div {{
                text-align: right;
                padding-right: {self.padding}px;
                max-width: {max_width};
            }}
            
            div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2) > div > button {{
                right: 0;
                margin-top: {2*self.padding + 14}px;
                overflow-y: scroll;
            }}
            
            div.stChatFloatingInputContainer {{
                display: none;
            }}
            
            div.stMarkdown {{
                padding: {self.padding}px;
            }}
            
            </style>
            """,
            unsafe_allow_html=True
        )
        pop_up_width = 1400

        st.markdown(
            f"""
            <style>
                div[data-modal-container='true'][key='{self.key}'] > div:first-child {{
                    width: {pop_up_width}px;
                }}
                div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child > div:first-child {{
                    width: {pop_up_width}px;
                    overflow-y: scroll;  <!-- Adds a scroller -->
                    max-height: 600px;
                    overflow-x: hidden;
                }}
                div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2) > div {{
                    width: {pop_up_width}px !important;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        with st.container():
            _container = st.container()
            if self.title:
                _container.markdown(
                    f"<h2>{self.title}</h2>", unsafe_allow_html=True)

        components.html(
            f"""
            <script>
            // STREAMLIT-MODAL-IFRAME-{self.key} <- Don't remove this comment. It's used to find our iframe
            const iframes = parent.document.body.getElementsByTagName('iframe');
            let container
            for(const iframe of iframes)
            {{
            if (iframe.srcdoc.indexOf("STREAMLIT-MODAL-IFRAME-{self.key}") !== -1) {{
                container = iframe.parentNode.previousSibling;
                container.setAttribute('data-modal-container', 'true');
                container.setAttribute('key', '{self.key}');
            }}
            }}
            </script>
            """,
            height=0, width=0
        )

        with _container:
            yield _container
