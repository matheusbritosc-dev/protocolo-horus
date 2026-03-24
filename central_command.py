import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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
