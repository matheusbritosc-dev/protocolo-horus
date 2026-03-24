import streamlit as st
from datetime import datetime, time

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
