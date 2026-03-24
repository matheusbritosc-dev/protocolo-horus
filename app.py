"""
PROTOCOLO HORUS
Sistema de Monitoramento em Tempo Real para Doação de Córneas - Goiás

Tech Stack: Python + Streamlit (Single Script)
Desenvolvido por: Engenheiro de Software Sênior - GovTech Specialist

INSTRUÇÕES DE EXECUÇÃO:
1. Instale as dependências: pip install streamlit pandas
2. Execute o aplicativo: streamlit run app.py
3. Acesse no navegador o endereço mostrado no terminal
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import random

# ============================================
# CONFIGURAÇÃO INICIAL DA PÁGINA
# ============================================

st.set_page_config(
    page_title="PROTOCOLO HORUS | Governo de Goiás",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session_state
if 'obitos' not in st.session_state:
    st.session_state['obitos'] = []


# ============================================
# FUNÇÃO: GERAÇÃO DE DADOS FAKE (DEMO)
# ============================================

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


# ============================================
# FUNÇÃO: MÓDULO HOSPITAL
# ============================================

def render_hospital_view():
    """
    Módulo de Registro de Óbito - Interface para hospitais registrarem óbitos
    e ativar o Protocolo Horus automaticamente quando critérios forem atendidos.
    """
    
    st.title("🏥 Módulo de Registro de Óbito - Hospital de Urgências (HUGO)")
    st.markdown("---")
    
    # Container estilizado para o formulário
    with st.container():
        st.markdown("### 📋 Formulário de Registro de Óbito")
        
        # Formulário usando columns para layout profissional
        col1, col2 = st.columns(2)
        
        with col1:
            # Nome do Paciente (Anonimizado)
            nome_paciente = st.text_input(
                "Nome do Paciente (Anonimizado)",
                value="",
                placeholder="Ex: PACIENTE_001",
                help="Utilize identificador anônimo para preservar privacidade"
            )
            
            # Idade
            idade = st.slider(
                "Idade do Paciente",
                min_value=0,
                max_value=100,
                value=45,
                help="Idade do paciente no momento do óbito"
            )
            
            # Horário do Óbito
            horario_obito = st.time_input(
                "Horário do Óbito",
                value=time(12, 0),
                help="Horário exato do óbito registrado"
            )
        
        with col2:
            # Causa do Óbito
            causa_obito = st.selectbox(
                "Causa do Óbito",
                options=[
                    "Parada Cardiorrespiratória",
                    "Morte Encefálica",
                    "Trauma",
                    "Sepse",
                    "Outros"
                ],
                help="Selecione a causa primária do óbito"
            )
            
            # ID do Hospital
            hospital = st.selectbox(
                "Hospital de Origem",
                options=[
                    "Hosp. Urgências (HUGO)",
                    "Santa Casa",
                    "IML"
                ],
                help="Instituição onde o óbito foi registrado"
            )
        
        st.markdown("---")
        
        # Botão de Registro
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            btn_registrar = st.button(
                "🚨 REGISTRAR ÓBITO",
                type="primary",
                use_container_width=True
            )
        
        # LÓGICA DE PROCESSAMENTO
        if btn_registrar:
            # Validação básica
            if not nome_paciente or nome_paciente.strip() == "":
                st.error("⚠️ Por favor, preencha o Nome do Paciente (Anonimizado)")
                return
            
            # Criar registro de óbito
            registro = {
                "id": len(st.session_state.get('obitos', [])) + 1,
                "nome_paciente": nome_paciente.strip().upper(),
                "idade": idade,
                "horario_obito": horario_obito.strftime("%H:%M:%S"),
                "causa_obito": causa_obito,
                "hospital": hospital,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "",  # Será definido pela regra de negócio
                "elegivel": False  # Flag para dashboard
            }
            
            # 🧠 APLICAR REGRA DE NEGÓCIO - GATILHO HORUS
            # Critérios: Idade entre 2 e 75 anos E Causa = PCR ou Parada Cardiorrespiratória
            if (2 <= idade <= 75) and (causa_obito in ["Parada Cardiorrespiratória", "PCR"]):
                registro["status"] = "ELEGÍVEL - ALTA PRIORIDADE"
                registro["elegivel"] = True
                is_elegivel = True
            else:
                registro["status"] = "NÃO ELEGÍVEL"
                registro["elegivel"] = False
                is_elegivel = False
            
            # Salvar no session_state
            if 'obitos' not in st.session_state:
                st.session_state['obitos'] = []
            
            st.session_state['obitos'].append(registro)
            
            # Feedback visual baseado na elegibilidade
            st.markdown("---")
            
            if is_elegivel:
                # Caso ELEGÍVEL - Alerta crítico
                st.success("✅ Óbito registrado com sucesso!")
                st.warning(
                    "🚨 **PROTOCOLO HORUS ATIVADO**\n\n"
                    f"⚡ Notificação enviada à Central de Comando em **3ms**\n\n"
                    f"👤 Paciente: {registro['nome_paciente']}\n"
                    f"📊 Classificação: **{registro['status']}**\n"
                    f"🏥 Hospital: {registro['hospital']}\n"
                    f"⏰ Horário: {registro['horario_obito']}"
                )
                st.balloons()
            else:
                # Caso NÃO ELEGÍVEL
                st.success("✅ Óbito registrado com sucesso!")
                st.info(
                    f"ℹ️ **Registro Processado**\n\n"
                    f"👤 Paciente: {registro['nome_paciente']}\n"
                    f"📊 Classificação: **{registro['status']}**\n"
                    f"🏥 Hospital: {registro['hospital']}\n"
                    f"⏰ Horário: {registro['horario_obito']}\n\n"
                    f"*Caso não atende critérios do Protocolo Horus para doação de córneas.*"
                )
    
    # Seção de Histórico (opcional - para contexto do hospital)
    st.markdown("---")
    st.markdown("### 📊 Registros Recentes - Este Hospital")
    
    if 'obitos' in st.session_state and len(st.session_state['obitos']) > 0:
        # Filtrar apenas registros do hospital atual
        registros_hospital = [
            r for r in st.session_state['obitos'] 
            if r['hospital'] == hospital
        ]
        
        if registros_hospital:
            st.markdown(f"**Total de registros:** {len(registros_hospital)}")
            
            # Mostrar últimos 5 registros
            for reg in reversed(registros_hospital[-5:]):
                status_color = "🟢" if reg['elegivel'] else "⚪"
                st.markdown(
                    f"{status_color} **{reg['nome_paciente']}** | "
                    f"Idade: {reg['idade']} | "
                    f"Status: {reg['status']} | "
                    f"Registrado em: {reg['timestamp']}"
                )
        else:
            st.info("Nenhum registro anterior deste hospital.")
    else:
        st.info("Nenhum óbito registrado no sistema ainda.")


# ============================================
# FUNÇÃO: CENTRAL DE COMANDO
# ============================================

def render_central_view():
    """
    Módulo Central de Comando - Dashboard tático para monitoramento em tempo real
    de doadores elegíveis de córneas com estética dark mode e alertas críticos.
    """
    
    # Estilização Dark Mode
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
        }
        .metric-container {
            background: linear-gradient(135deg, #1a1d29 0%, #2d1b3d 100%);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #ff4444;
            box-shadow: 0 4px 6px rgba(255, 68, 68, 0.3);
        }
        .urgent-alert {
            background-color: #8b0000;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header tático
    st.markdown("# 🎯 CENTRAL DE COMANDO HORUS")
    st.markdown("### Monitoramento em Tempo Real - Captação de Córneas | Goiás")
    st.markdown("---")
    
    # Obter dados de óbitos
    obitos = st.session_state.get('obitos', [])
    
    # Filtrar apenas ELEGÍVEIS
    elegiveis = [o for o in obitos if o.get('elegivel', False)]
    
    # Calcular métricas
    total_obitos_hoje = len(obitos)
    total_alertas = len(elegiveis)
    
    # Calcular tempo médio de resposta (simulado - em minutos)
    tempo_medio_resposta = 12  # Placeholder - seria calculado com base em despachos reais
    
    # 📊 KPIs NO TOPO
    st.markdown("### 📊 Indicadores em Tempo Real")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💀 Óbitos Registrados Hoje",
            value=total_obitos_hoje,
            delta=f"+{total_obitos_hoje} nas últimas 24h"
        )
    
    with col2:
        # Destaque vermelho para alertas
        st.metric(
            label="🚨 ALERTAS DE CÓRNEA ATIVOS",
            value=total_alertas,
            delta="URGENTE" if total_alertas > 0 else "Nenhum alerta",
            delta_color="inverse" if total_alertas > 0 else "off"
        )
    
    with col3:
        st.metric(
            label="⚡ Tempo Médio de Resposta",
            value=f"{tempo_medio_resposta} min",
            delta="-3 min vs. semana passada",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # 🗺️ MAPA TÁTICO
    st.markdown("### 🗺️ Mapa Tático - Hospitais com Alertas Ativos")
    
    # Coordenadas fictícias de hospitais em Goiânia
    hospitais_coords = {
        "Hosp. Urgências (HUGO)": {"lat": -16.6869, "lon": -49.2648},
        "Santa Casa": {"lat": -16.6782, "lon": -49.2537},
        "IML": {"lat": -16.6950, "lon": -49.2700}
    }
    
    # Criar dados para o mapa (apenas hospitais com alertas)
    map_data = []
    for elegivel in elegiveis:
        hospital = elegivel.get('hospital', '')
        if hospital in hospitais_coords:
            map_data.append({
                'lat': hospitais_coords[hospital]['lat'],
                'lon': hospitais_coords[hospital]['lon']
            })
    
    if map_data:
        df_map = pd.DataFrame(map_data)
        st.map(df_map, size=200, color='#ff0000', zoom=11)
        st.caption(f"🔴 {len(map_data)} alerta(s) ativo(s) - Pontos vermelhos indicam hospitais com doadores elegíveis")
    else:
        st.info("✅ Nenhum alerta ativo no momento. Mapa limpo.")
    
    st.markdown("---")
    
    # 🚨 TABELA DE URGÊNCIA (CRÍTICO)
    st.markdown("### 🚨 PAINEL DE URGÊNCIA - DOADORES ELEGÍVEIS")
    
    if len(elegiveis) == 0:
        st.success("✅ **Sistema em Stand-by** - Nenhum caso elegível aguardando processamento.")
    else:
        st.warning(f"⚠️ **{len(elegiveis)} CASO(S) CRÍTICO(S) AGUARDANDO AÇÃO**")
        
        # Processar cada caso elegível
        for idx, caso in enumerate(elegiveis):
            # Calcular tempo decorrido
            try:
                # Obter hora do óbito
                hora_obito_str = caso.get('horario_obito', '00:00:00')
                timestamp_str = caso.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                
                # Combinar data e hora para cálculo preciso
                data_obito = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                
                # Calcular tempo decorrido
                agora = datetime.now()
                tempo_decorrido = agora - data_obito
                
                # Janela de 6 horas para captação
                janela_total = timedelta(hours=6)
                tempo_restante = janela_total - tempo_decorrido
                
                # Converter para horas e minutos
                horas_restantes = int(tempo_restante.total_seconds() // 3600)
                minutos_restantes = int((tempo_restante.total_seconds() % 3600) // 60)
                
                # Determinar criticidade
                is_critico = tempo_restante < timedelta(hours=2)
                
                # Cor de fundo baseada na urgência
                if is_critico:
                    bg_color = "#8b0000"  # Vermelho sangue
                    border_color = "#ff0000"
                    status_emoji = "🔴"
                    urgencia_texto = "CRÍTICO - MENOS DE 2H"
                elif tempo_restante < timedelta(hours=4):
                    bg_color = "#ff8c00"  # Laranja
                    border_color = "#ffa500"
                    status_emoji = "🟠"
                    urgencia_texto = "ATENÇÃO - MENOS DE 4H"
                else:
                    bg_color = "#2d5016"  # Verde escuro
                    border_color = "#4caf50"
                    status_emoji = "🟢"
                    urgencia_texto = "DENTRO DO PRAZO"
                
            except Exception as e:
                # Fallback em caso de erro
                horas_restantes = 5
                minutos_restantes = 30
                is_critico = False
                bg_color = "#2d5016"
                border_color = "#4caf50"
                status_emoji = "🟢"
                urgencia_texto = "DENTRO DO PRAZO"
            
            # Card para cada caso
            st.markdown(f"""
                <div style="
                    background-color: {bg_color};
                    border: 3px solid {border_color};
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 15px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
                ">
                    <h4 style="color: white; margin-top: 0;">
                        {status_emoji} ALERTA #{caso.get('id', idx+1)} - {urgencia_texto}
                    </h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Detalhes do caso
            col_info1, col_info2, col_info3, col_btn = st.columns([2, 2, 2, 1.5])
            
            with col_info1:
                st.markdown(f"**👤 Paciente:** {caso.get('nome_paciente', 'N/A')}")
                st.markdown(f"**📅 Idade:** {caso.get('idade', 'N/A')} anos")
            
            with col_info2:
                st.markdown(f"**🏥 Hospital:** {caso.get('hospital', 'N/A')}")
                st.markdown(f"**💔 Causa:** {caso.get('causa_obito', 'N/A')}")
            
            with col_info3:
                st.markdown(f"**⏰ Óbito:** {caso.get('horario_obito', 'N/A')}")
                if tempo_restante.total_seconds() > 0:
                    st.markdown(f"**⏳ TEMPO RESTANTE:** {horas_restantes}h {minutos_restantes}min")
                else:
                    st.markdown(f"**⏳ TEMPO RESTANTE:** ❌ EXPIRADO")
            
            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento
                if st.button(
                    "🚁 DESPACHAR EQUIPE",
                    key=f"despachar_{caso.get('id', idx)}",
                    type="primary" if is_critico else "secondary",
                    use_container_width=True
                ):
                    st.success(f"✅ Equipe despachada para {caso.get('hospital', 'hospital')}!")
                    st.info(f"📡 Tempo estimado de chegada: 15 minutos\n\n🚁 Unidade Móvel HORUS-{idx+1} em rota")
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rodapé com estatísticas adicionais
    st.markdown("### 📈 Estatísticas do Sistema")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        taxa_elegibilidade = (total_alertas / total_obitos_hoje * 100) if total_obitos_hoje > 0 else 0
        st.metric("Taxa de Elegibilidade", f"{taxa_elegibilidade:.1f}%")
    
    with col_stat2:
        st.metric("Total de Hospitais Conectados", "3")
    
    with col_stat3:
        st.metric("Córneas Captadas (Mês)", "47")  # Simulado
    
    # Timestamp de atualização
    st.caption(f"🔄 Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ============================================
# SIDEBAR - NAVEGAÇÃO E CONTROLES
# ============================================

with st.sidebar:
    # Logo e Header
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #ff4444; margin: 0;">👁️ HORUS</h1>
            <p style="color: #888; font-size: 14px; margin: 5px 0;">Protocolo de Captação de Córneas</p>
            <p style="color: #666; font-size: 12px;">Governo de Goiás | SESA</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação
    st.markdown("### 🎯 Módulos do Sistema")
    
    modulo = st.radio(
        "Selecione o Módulo:",
        options=["🏥 Módulo Hospital", "🎯 Central de Comando"],
        label_visibility="collapsed"
    )
    
    # Botão de simulação para demo
    st.markdown("---")
    st.markdown("### 🎭 Modo Demonstração")
    
    if st.button("⚡ SIMULAR CAOS", type="primary", use_container_width=True):
        gerar_dados_fake()
        st.success("✅ 10 casos simulados gerados!")
        st.info(
            "📊 **Dados gerados:**\n"
            "- 4 Doadores Perfeitos\n"
            "- 3 Não Doadores (filtrados)\n"
            "- 3 Casos Críticos (< 2h)"
        )
        st.rerun()  # Atualiza a página para mostrar os dados
    
    st.caption("Utilize este botão para popular o sistema com dados fictícios para demonstração.")
    
    # Informações do sistema
    st.markdown("---")
    st.markdown("### 📊 Status do Sistema")
    st.success("🟢 Sistema Operacional")
    st.metric("Uptime", "99.9%")
    
    st.markdown("---")
    st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    st.caption("v1.0.0-MVP | © 2026 SESA-GO")


# ============================================
# ÁREA PRINCIPAL - RENDERIZAÇÃO DE MÓDULOS
# ============================================

if modulo == "🏥 Módulo Hospital":
    render_hospital_view()
elif modulo == "🎯 Central de Comando":
    render_central_view()


# ============================================
# FOOTER
# ============================================

st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.caption("🏛️ **Secretaria de Estado da Saúde de Goiás**")

with col_footer2:
    st.caption("🚑 **Sistema Integrado de Captação de Órgãos**")

with col_footer3:
    st.caption("📞 **Suporte 24h: 0800-XXX-XXXX**")


# ============================================
# ENTRY POINT
# ============================================

if __name__ == '__main__':
    # O Streamlit não precisa de main() explícito
    # Mas podemos adicionar mensagens de debug se necessário
    pass
