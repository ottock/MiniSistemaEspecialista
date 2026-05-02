# Mini Sistema Especialista — Diagnóstico de Arboviroses

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

Sistema especialista baseado em regras para auxílio ao diagnóstico clínico de doenças arbovirais (Dengue, Chikungunya e Zika). Desenvolvido em Python com interface gráfica moderna via CustomTkinter, oferecendo uma solução intuitiva e acessível para triagem clínica.

---

## Funcionalidades Principais

- **Questionário interativo** com 9 sintomas/fatores clínicos validados
- **Motor de inferência avançado** com encadeamento progressivo (*forward chaining*)
- **Diagnósticos em tempo real** com múltiplos níveis de confiança
- **Base de conhecimento configurável** via YAML (sem alteração de código)
- **Logs de auditoria** com rotação automática diária
- **Interface intuitiva** com feedback visual (cores e cartões)
- **Facilmente extensível** para incluir novas doenças e regras

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| **Linguagem** | Python 3.10+ |
| **Interface Gráfica** | CustomTkinter |
| **Base de Conhecimento** | PyYAML |
| **Sistema de Logs** | `logging` (stdlib Python) |
| **Gerenciamento de Projeto** | Git + venv |

---

## Estrutura do Projeto

```
MiniSistemaEspecialista/
├── src/
│   ├── main.py                              # Ponto de entrada da aplicação
│   ├── presentation/
│   │   └── gui/
│   │       ├── __init__.py
│   │       └── app.py                       # Interface gráfica (CustomTkinter)
│   └── core/
│       ├── ai/
│       │   ├── __init__.py
│       │   ├── shell.py                     # Motor de inferência (forward chaining)
│       │   └── diagnostic.yaml              # Base de conhecimento (regras + perguntas)
│       └── logger/
│           ├── __init__.py
│           ├── logger.py                    # Configuração e setup de logs
│           └── configs/
│               └── base_config.json         # Parâmetros do logger (formato, rotação, etc)
├── scripts/
│   └── createVenv.bat                       # Script para criar env virtual (Windows)
├── log/                                     # Diretório com logs gerados em runtime
├── .venv/                                   # Ambiente virtual Python
├── .git/                                    # Repositório Git
├── .gitignore                               # Arquivos ignorados pelo Git
├── requirements.txt                         # Dependências do projeto
└── README.md                                # Este arquivo
```

---

## Instalação e Configuração

### Pré-requisitos

- **Python 3.10 ou superior**
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para versionamento)

### Windows

Execute o script fornecido para criar automaticamente o ambiente virtual e instalar dependências:

```bat
scripts\createVenv.bat
```

Ou manualmente:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Verificando a Instalação

Após a instalação, confirme que as dependências foram instaladas:

```bash
pip list
```

Você deverá ver `customtkinter` e `PyYAML` na lista.

---

## Como Executar

**Ativar o ambiente virtual (se necessário):**

- Windows: `.venv\Scripts\activate`
- Linux/macOS: `source .venv/bin/activate`

**Executar a aplicação:**

```bash
python src/main.py
```

A janela principal da aplicação abrirá automaticamente.

---

## Guia de Uso

### Fluxo Principal

1. **Inicie a aplicação** conforme instruções acima
2. **Responda ao questionário**: Para cada symptom exibido, clique em **Sim** ou **Não**
3. **Analise as perguntas**: Leia com atenção e responda baseado nas informações clínicas do paciente
4. **Clique em "Diagnosticar"**: O motor de inferência processará as respostas
5. **Visualize os resultados**: Os diagnósticos aparecem como cartões coloridos:
   - **Verde** — Diagnóstico provável com alta confiança (ex.: *Chikungunya — fase aguda*)
   - **Âmbar** — Alerta clínico com recomendação de diferenciação (ex.: *Arbovirose provável, investigar*)
6. **Reinicie** para avaliar novo paciente (botão "Limpar")

### Exemplos de Diagnósticos

| Sintomas | Diagnóstico |
|---|---|
| Febre alta + Dor articular intensa | Chikungunya (fase aguda) |
| Febre alta + Dor intensa + Duração prolongada | Chikungunya crônica |
| Febre alta + Dor nos olhos | Dengue |
| Febre ausente + Rash + Prurido + Olhos vermelhos | Zika (alta confiança) |

---

## Base de Conhecimento

A base de conhecimento está definida em [`src/core/ai/diagnostic.yaml`](src/core/ai/diagnostic.yaml) e é composta por:

- **Questions (Perguntas)**: 9 questões clínicas estruturadas
- **Rules (Regras)**: 16 regras de inferência (premissas → conclusões)

### Sintomas Avaliados

| Código | Descrição |
|---|---|
| `febre_alta` | Febre alta (> 39°C) |
| `febre_baixa_ou_ausente` | Febre baixa ou ausente |
| `dor_articular_intensa` | Dor intensa nas articulações |
| `dor_articular_leve_moderada` | Dor leve a moderada nas articulações |
| `dor_olhos` | Dor atrás/nos olhos (retro-ocular) |
| `olhos_vermelhos` | Olhos vermelhos (hiperemia conjuntival) |
| `rash_cutaneo` | Exantema (manchas vermelhas na pele) |
| `prurido` | Prurido intenso nas lesões |
| `duracao_prolongada_dor` | Dor articular persistindo por meses |

### Doenças Detectadas

- **Dengue**: Febre alta + dor ocular + dor articular moderada
- **Chikungunya**: Febre alta + dor articular intensa (aguda ou crônica)
- **Zika**: Febre baixa/ausente + rash + prurido (com ou sem conjuntivite)

### Customizando a Base de Conhecimento

Para adicionar novas doenças ou modificar regras, edite [`src/core/ai/diagnostic.yaml`](src/core/ai/diagnostic.yaml). **Nenhuma alteração no código-fonte é necessária!**

**Exemplo de adição de nova regra:**

```yaml
- if: [febre_alta, rash_cutaneo]
  then: "Diagnóstico: Arbovirose provável. Diferenciação clínica necessária."
```

---

## Sistema de Logs

Todos os diagnósticos e interações são registrados automaticamente em `log/log_YYYY-MM-DD.log` com:

- Data e hora de cada diagnóstico
- Respostas do paciente
- Resultado da inferência
- Erros e exceções

Os logs são rotacionados diariamente para melhor organização.

---

## Arquitetura Técnica

### Padrão: Motor de Inferência (Forward Chaining)

O sistema implementa o padrão de **encadeamento progressivo**:

1. **Coleta de fatos**: Respostas do questionário
2. **Aplicação de regras**: Verifica todas as regras contra os fatos coletados
3. **Geração de novos fatos**: Conclusões derivadas das regras
4. **Repetição**: Continua até não haver novas conclusões
5. **Exibição**: Apresenta todos os diagnósticos gerados

### Componentes Principais

- **`presentation/gui/app.py`**: Interface gráfica com CustomTkinter
- **`core/ai/shell.py`**: Motor de inferência (lógica de diagnóstico)
- **`core/logger/logger.py`**: Sistema de logs com rotação
- **`core/ai/diagnostic.yaml`**: Dados declarativos (perguntas + regras)

---