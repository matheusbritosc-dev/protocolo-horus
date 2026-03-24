import streamlit as st
from datetime import datetime, timedelta
import random

def gerar_dados_fake():
    """
    Gera 10 casos fictícios variados para demonstração comercial do Protocolo Horus.
    
    Cenários incluídos:
    - Doadores perfeitos (alta prioridade, recentes)
    - Não doadores (fora dos critérios)
    - Casos críticos (próximos do limite de 6h)
    """
    
    # Lista de nomes anônimos
    nomes_pacientes = [
        "PACIENTE_ALPHA_001",
        "PACIENTE_BETA_002",
        "PACIENTE_GAMMA_003",
        "PACIENTE_DELTA_004",
        "PACIENTE_EPSILON_005",
        "PACIENTE_ZETA_006",
        "PACIENTE_ETA_007",
        "PACIENTE_THETA_008",
        "PACIENTE_IOTA_009",
        "PACIENTE_KAPPA_010"
    ]
    
    # Hospitais disponíveis
    hospitais = ["Hosp. Urgências (HUGO)", "Santa Casa", "IML"]
    
    # Causas de óbito
    causas_doador = ["Parada Cardiorrespiratória", "PCR"]
    causas_nao_doador = ["Morte Encefálica", "Trauma", "Sepse", "Outros"]
    
    # Inicializar lista de óbitos no session_state
    st.session_state['obitos'] = []
    
    # Horário atual
    agora = datetime.now()
    
    # ========================================
    # CENÁRIO 1: DOADORES PERFEITOS (4 casos)
    # ========================================
    # Casos recentes, idade ideal, PCR -> Alertas verdes/amarelos
    
    for i in range(4):
        # Tempo decorrido: entre 30 minutos e 3 horas
        minutos_atras = random.randint(30, 180)
        horario_obito = agora - timedelta(minutes=minutos_atras)
        
        caso = {
            "id": i + 1,
            "nome_paciente": nomes_pacientes[i],
            "idade": random.randint(25, 45),  # Idade ideal para doação
            "horario_obito": horario_obito.strftime("%H:%M:%S"),
            "causa_obito": random.choice(causas_doador),
            "hospital": random.choice(hospitais),
            "timestamp": horario_obito.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "ELEGÍVEL - ALTA PRIORIDADE",
            "elegivel": True
        }
        st.session_state['obitos'].append(caso)
    
    # ========================================
    # CENÁRIO 2: NÃO DOADORES (3 casos)
    # ========================================
    # Idade fora do critério OU causa não elegível
    
    # Caso 2.1: Idade muito avançada (90 anos)
    horario_obito = agora - timedelta(hours=1, minutes=30)
    caso = {
        "id": 5,
        "nome_paciente": nomes_pacientes[4],
        "idade": 90,  # Fora do critério (> 75)
        "horario_obito": horario_obito.strftime("%H:%M:%S"),
        "causa_obito": "Parada Cardiorrespiratória",  # Mesmo com PCR, idade descarta
        "hospital": hospitais[0],
        "timestamp": horario_obito.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "NÃO ELEGÍVEL",
        "elegivel": False
    }
    st.session_state['obitos'].append(caso)
    
    # Caso 2.2: Idade muito jovem (1 ano)
    horario_obito = agora - timedelta(hours=2, minutes=15)
    caso = {
        "id": 6,
        "nome_paciente": nomes_pacientes[5],
        "idade": 1,  # Fora do critério (< 2)
        "horario_obito": horario_obito.strftime("%H:%M:%S"),
        "causa_obito": "PCR",
        "hospital": hospitais[1],
        "timestamp": horario_obito.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "NÃO ELEGÍVEL",
        "elegivel": False
    }
    st.session_state['obitos'].append(caso)
    
    # Caso 2.3: Causa não elegível (Sepse)
    horario_obito = agora - timedelta(hours=1)
    caso = {
        "id": 7,
        "nome_paciente": nomes_pacientes[6],
        "idade": 40,  # Idade OK
        "horario_obito": horario_obito.strftime("%H:%M:%S"),
        "causa_obito": "Sepse",  # Causa não elegível
        "hospital": hospitais[2],
        "timestamp": horario_obito.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "NÃO ELEGÍVEL",
        "elegivel": False
    }
    st.session_state['obitos'].append(caso)
    
    # ========================================
    # CENÁRIO 3: CASOS CRÍTICOS (3 casos)
    # ========================================
    # Óbitos há quase 6 horas -> Cronômetro em vermelho sangue
    
    # Caso 3.1: Faltando 30 minutos para vencer
    horario_obito = agora - timedelta(hours=5, minutes=30)
    caso = {
        "id": 8,
        "nome_paciente": nomes_pacientes[7],
        "idade": 38,
        "horario_obito": horario_obito.strftime("%H:%M:%S"),
        "causa_obito": "Parada Cardiorrespiratória",
        "hospital": hospitais[0],
        "timestamp": horario_obito.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ELEGÍVEL - ALTA PRIORIDADE",
        "elegivel": True
    }
    st.session_state['obitos'].append(caso)
    
    # Caso 3.2: Faltando 1 hora para vencer
    horario_obito = agora - timedelta(hours=5)
    caso = {
        "id": 9,
        "nome_paciente": nomes_pacientes[8],
        "idade": 42,
        "horario_obito": horario_obito.strftime("%H:%M:%S"),
        "causa_obito": "PCR",
        "hospital": hospitais[1],
        "timestamp": horario_obito.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ELEGÍVEL - ALTA PRIORIDADE",
        "elegivel": True
    }
    st.session_state['obitos'].append(caso)
    
    # Caso 3.3: Faltando 1h45min para vencer
    horario_obito = agora - timedelta(hours=4, minutes=15)
    caso = {
        "id": 10,
        "nome_paciente": nomes_pacientes[9],
        "idade": 35,
        "horario_obito": horario_obito.strftime("%H:%M:%S"),
        "causa_obito": "Parada Cardiorrespiratória",
        "hospital": hospitais[2],
        "timestamp": horario_obito.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ELEGÍVEL - ALTA PRIORIDADE",
        "elegivel": True
    }
    st.session_state['obitos'].append(caso)
    
    return True


def render_demo_button_sidebar():
    """
    Renderiza o botão de simulação na sidebar.
    Deve ser chamado dentro do contexto st.sidebar.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎭 Modo Demonstração")
    
    if st.sidebar.button("⚡ SIMULAR CAOS", type="primary", use_container_width=True):
        gerar_dados_fake()
        st.sidebar.success("✅ 10 casos simulados gerados!")
        st.sidebar.info(
            "📊 **Dados gerados:**\n"
            "- 4 Doadores Perfeitos\n"
            "- 3 Não Doadores (filtrados)\n"
            "- 3 Casos Críticos (< 2h)"
        )
        st.rerun()  # Atualiza a página para mostrar os dados
    
    st.sidebar.caption("Utilize este botão para popular o sistema com dados fictícios para demonstração.")
