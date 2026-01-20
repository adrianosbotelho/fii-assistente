"""
Sistema de Autenticação Simples para FII Assistente
Permite apenas um usuário específico: adrianosbotelho@gmail.com
"""

import streamlit as st
import hashlib
import time
from datetime import datetime, timedelta
import os

class SimpleAuth:
    """Autenticação simples com email e senha específicos"""
    
    def _hash_password(self, password: str) -> str:
        """Gera hash da senha"""
        return hashlib.sha256(f"{password}fii_salt".encode()).hexdigest()
    
    def __init__(self):
        # Configurações do usuário autorizado
        self.authorized_email = "adrianosbotelho@gmail.com"
        
        # Obter senha da variável de ambiente (obrigatória)
        auth_password = os.getenv("AUTH_PASSWORD")
        if not auth_password:
            raise ValueError("AUTH_PASSWORD não definida. Configure no arquivo .env ou variável de ambiente.")
        
        self.authorized_password_hash = self._hash_password(auth_password)
        
        # Inicializar session state
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "user_info" not in st.session_state:
            st.session_state.user_info = None
        if "login_attempts" not in st.session_state:
            st.session_state.login_attempts = 0
        if "last_attempt" not in st.session_state:
            st.session_state.last_attempt = 0
    
    def _hash_password(self, password: str) -> str:
        """Gera hash da senha"""
        return hashlib.sha256(f"{password}fii_salt".encode()).hexdigest()
    
    def is_authenticated(self) -> bool:
        """Verifica se o usuário está autenticado"""
        return st.session_state.authenticated
    
    def authenticate(self, email: str, password: str) -> bool:
        """Autentica o usuário"""
        # Verificar rate limiting (máximo 5 tentativas por hora)
        current_time = time.time()
        if st.session_state.login_attempts >= 5:
            if current_time - st.session_state.last_attempt < 3600:  # 1 hora
                return False
            else:
                # Reset após 1 hora
                st.session_state.login_attempts = 0
        
        # Verificar credenciais
        if (email.lower().strip() == self.authorized_email.lower() and 
            self._hash_password(password) == self.authorized_password_hash):
            
            # Login bem-sucedido
            st.session_state.authenticated = True
            st.session_state.user_info = {
                "email": self.authorized_email,
                "name": "Adriano Botelho",
                "user_id": "adriano_main",
                "login_time": datetime.now().isoformat()
            }
            st.session_state.login_attempts = 0
            return True
        else:
            # Login falhou
            st.session_state.login_attempts += 1
            st.session_state.last_attempt = current_time
            return False
    
    def logout(self):
        """Faz logout do usuário"""
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.rerun()
    
    def get_user_info(self):
        """Retorna informações do usuário"""
        return st.session_state.user_info if self.is_authenticated() else None
    
    def render_login_page(self):
        """Renderiza a página de login simples"""
        st.set_page_config(
            page_title="FII Assistente - Login",
            layout="centered",
            page_icon="🔐"
        )
        
        # CSS customizado para página de login
        st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
            color: white;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: white;
        }
        .login-subtitle {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        .stTextInput > div > div > input {
            background-color: rgba(255,255,255,0.9);
            color: #333;
            border-radius: 8px;
            border: none;
            padding: 12px;
        }
        .login-info {
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Container principal
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Título
        st.markdown('<h1 class="login-title">📊 FII Assistente</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Análise Profissional de Carteira de FIIs</p>', unsafe_allow_html=True)
        
        # Verificar se há muitas tentativas
        if st.session_state.login_attempts >= 5:
            time_remaining = 3600 - (time.time() - st.session_state.last_attempt)
            if time_remaining > 0:
                minutes_remaining = int(time_remaining / 60)
                st.error(f"🚫 Muitas tentativas de login. Tente novamente em {minutes_remaining} minutos.")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        # Formulário de login
        st.markdown("### 🔐 Acesso Restrito")
        
        with st.form("login_form"):
            email = st.text_input(
                "📧 Email",
                placeholder="seu@email.com",
                help="Email autorizado para acesso"
            )
            
            password = st.text_input(
                "🔑 Senha",
                type="password",
                placeholder="Digite sua senha",
                help="Senha de acesso"
            )
            
            submitted = st.form_submit_button("🚀 Entrar", use_container_width=True)
            
            if submitted:
                if not email or not password:
                    st.error("❌ Por favor, preencha email e senha")
                elif self.authenticate(email, password):
                    st.success("✅ Login realizado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                else:
                    remaining_attempts = 5 - st.session_state.login_attempts
                    if remaining_attempts > 0:
                        st.error(f"❌ Credenciais inválidas. {remaining_attempts} tentativas restantes.")
                    else:
                        st.error("🚫 Muitas tentativas. Acesso bloqueado por 1 hora.")
        
        # Informações
        st.markdown("""
        <div class="login-info">
        <strong>ℹ️ Informações:</strong><br>
        • Acesso restrito ao proprietário<br>
        • Máximo 5 tentativas por hora<br>
        • Dados seguros e criptografados
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informações para desenvolvimento (apenas em modo debug)
        if os.getenv("DEBUG", "false").lower() == "true":
            st.markdown("---")
            st.markdown("**🔧 Debug Info:**")
            st.markdown(f"- Email autorizado: {self.authorized_email}")
            st.markdown(f"- Tentativas: {st.session_state.login_attempts}/5")
            st.markdown(f"- AUTH_PASSWORD definida: {'✅' if os.getenv('AUTH_PASSWORD') else '❌'}")
    
    def render_user_info(self):
        """Renderiza informações do usuário na sidebar"""
        if not self.is_authenticated():
            return
        
        user = self.get_user_info()
        if not user:
            return
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 Usuário Logado")
        
        # Informações
        st.sidebar.markdown(f"**Nome:** {user.get('name', 'N/A')}")
        st.sidebar.markdown(f"**Email:** {user.get('email', 'N/A')}")
        
        # Tempo de login
        try:
            login_time = datetime.fromisoformat(user.get('login_time', ''))
            st.sidebar.markdown(f"**Login:** {login_time.strftime('%d/%m %H:%M')}")
        except:
            pass
        
        # Botão de logout
        if st.sidebar.button("🚪 Logout", type="secondary"):
            self.logout()

# Instância global do autenticador simples
simple_auth = SimpleAuth()