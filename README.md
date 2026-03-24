# 👁️ Protocolo Horus

> Sistema de Monitoramento em Tempo Real para Doação de Córneas — Governo de Goiás

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-MVP-orange)

## 📋 Sobre

O **Protocolo Horus** é um sistema GovTech desenvolvido para a Secretaria de Estado da Saúde de Goiás (SESA-GO) que monitora **em tempo real** óbitos hospitalares e identifica automaticamente potenciais doadores de córneas com base em critérios médicos.

### 🎯 Problema
No Brasil, a captação de córneas tem uma **janela crítica de 6 horas** após o óbito. Sem um sistema automatizado, muitos doadores elegíveis são perdidos por falta de comunicação rápida entre hospitais e centrais de captação.

### 💡 Solução
O Horus automatiza a triagem e alerta a Central de Comando em **menos de 3ms** quando um doador elegível é registrado, com:
- Classificação automática por regras de negócio médicas
- Dashboard tático com mapa de hospitais
- Cronômetro regressivo de 6h por doador
- Botão de despacho de equipe de captação

## 🏗️ Arquitetura

```
protocolo-horus/
├── app.py                  # Aplicação principal Streamlit
├── central_command.py      # Módulo Central de Comando
├── hospital_module.py      # Módulo Hospital (registro de óbitos)
├── demo_data.py            # Gerador de dados para demonstração
└── README.md
```

## 🚀 Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USER/protocolo-horus.git
cd protocolo-horus

# 2. Instale as dependências
pip install streamlit pandas

# 3. Execute
streamlit run app.py
```

## 📊 Funcionalidades

| Módulo | Descrição |
|--------|-----------|
| **🏥 Hospital** | Formulário de registro de óbito com validação e classificação automática |
| **🎯 Central de Comando** | Dashboard dark-mode com KPIs, mapa tático e painel de urgência |
| **⚡ Simulação** | Botão "Simular Caos" gera 10 casos variados para demonstração |

### Regras de Negócio
- **Idade:** entre 2 e 75 anos
- **Causa do Óbito:** Parada Cardiorrespiratória (PCR)
- **Janela:** 6 horas após óbito para captação

## 🛠️ Tech Stack

- **Backend:** Python 3.10+
- **Frontend:** Streamlit
- **Dados:** Pandas + session_state (MVP)
- **Mapas:** Streamlit Map (coordenadas Goiânia)

## 📄 Licença

MIT License — Desenvolvido por **Matheus Brito**
