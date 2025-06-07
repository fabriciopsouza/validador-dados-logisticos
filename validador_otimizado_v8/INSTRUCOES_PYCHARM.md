# Instruções Detalhadas para PyCharm - Sistema v8.0

## Guia Passo-a-Passo para Usuários Não Técnicos

### 📋 Pré-requisitos
- **PyCharm Community Edition** (gratuito) ou Professional
- **Python 3.8+** instalado no sistema
- **Arquivo ZIP** do projeto descompactado

### 🚀 Configuração Inicial

#### 1. Instalação do PyCharm
1. Baixe o PyCharm Community em: https://www.jetbrains.com/pycharm/download/
2. Instale seguindo as instruções padrão
3. Abra o PyCharm após a instalação

#### 2. Abertura do Projeto
1. **Clique em "Open"** na tela inicial do PyCharm
2. **Navegue até a pasta** `validador_otimizado_v8` (descompactada)
3. **Selecione a pasta** e clique em "OK"
4. **Aguarde** o PyCharm indexar o projeto (barra de progresso na parte inferior)

#### 3. Configuração do Interpretador Python
1. **Vá em File → Settings** (ou PyCharm → Preferences no Mac)
2. **Navegue para Project → Python Interpreter**
3. **Clique no ícone de engrenagem** → "Add..."
4. **Selecione "System Interpreter"**
5. **Escolha a versão do Python** instalada no seu sistema
6. **Clique em "OK"**

### ⚡ Execução do Sistema

#### Método 1: Execução Direta (Recomendado)
1. **Abra o arquivo** `sistema_validacao_v8_otimizado.py` no PyCharm
2. **Clique com botão direito** no arquivo
3. **Selecione "Run 'sistema_validacao_v8_otimizado'"**
4. **Aguarde** a instalação automática de dependências (primeira execução)
5. **A interface gráfica** abrirá automaticamente

#### Método 2: Usando o Botão Run
1. **Abra o arquivo** `sistema_validacao_v8_otimizado.py`
2. **Clique no botão verde "Run"** (▶️) no canto superior direito
3. **Aguarde** o processamento
4. **A interface gráfica** abrirá automaticamente

#### Método 3: Terminal Integrado
1. **Abra o terminal** no PyCharm (View → Tool Windows → Terminal)
2. **Digite**: `python sistema_validacao_v8_otimizado.py`
3. **Pressione Enter**

### 🎯 Usando a Interface Gráfica

#### Guia de Cores e Prioridades
- **🔴 VERMELHO**: Botões obrigatórios - Execute primeiro
- **🟡 AMARELO**: Botões recomendados - Para melhores resultados
- **🟢 VERDE**: Botões opcionais - Pode pular se quiser rapidez
- **⚪ CINZA**: Botões avançados - Apenas se precisar de detalhes

#### Fluxo de Uso Recomendado

##### Aba 1: Configuração (🔴 OBRIGATÓRIO)
1. **Clique em "📂 Procurar"** para selecionar o template Excel
2. **Escolha uma opção**:
   - **"📁 Usar pasta padrão"**: Sistema cria pasta automaticamente
   - **"🎯 Selecionar pasta personalizada"**: Escolha sua pasta
3. **Clique em "🔴 Analisar Template"** (OBRIGATÓRIO)
4. **Clique em "🔴 Detectar Bases"** (OBRIGATÓRIO)

##### Aba 2: Processamento (🟡 RECOMENDADO)
1. **Escolha o modo**:
   - **⚡ Rápido**: Validação essencial (segundos)
   - **📊 Completo**: Com estatísticas (minutos)
2. **Clique em "🟡 Processar Todas as Bases"** (RECOMENDADO)
3. **Aguarde** a barra de progresso completar

##### Aba 3: Relatórios (🟡 RECOMENDADO)
1. **Clique em "🟡 Tabela Campos Obrigatórios"** (RECOMENDADO)
2. **Clique em "🟡 Tabela Inconsistências"** (RECOMENDADO)
3. **Clique em "📁 Abrir Pasta de Resultados"** para ver arquivos

##### Aba 4: Logs (⚪ AVANÇADO)
- **Use apenas se houver problemas**
- **Clique em "🔄 Atualizar Logs"** para ver detalhes
- **Clique em "💾 Exportar Logs"** se precisar de suporte

### 📁 Localização dos Resultados

#### Pasta Padrão Automática
```
C:\Users\[seu_nome]\Documents\ValidadorLogistico\
├── dados_entrada\          # Coloque seus arquivos CSV aqui
├── output\                 # Resultados do processamento
│   ├── BASE1\
│   │   ├── input\          # Arquivos processados
│   │   └── relatorio_validacao_BASE1.md
│   └── BASE2\
├── tabela_campos_obrigatorios_[data].xlsx
└── tabela_inconsistencias_[data].xlsx
```

#### Como Encontrar os Arquivos
1. **Use os botões "📁 Abrir Pasta"** na interface
2. **Ou navegue manualmente** para `Documents\ValidadorLogistico`
3. **Os relatórios Excel** ficam na pasta principal
4. **Os arquivos processados** ficam em `output\[NOME_BASE]\input\`

### 🔧 Solução de Problemas Comuns

#### Problema: "No module named 'pandas'"
**Solução**: 
- O sistema instala automaticamente na primeira execução
- Aguarde alguns minutos durante a primeira execução
- Verifique sua conexão com a internet

#### Problema: Interface não abre
**Solução**:
1. Verifique se o Python tem tkinter instalado
2. No terminal do PyCharm, digite: `python -m tkinter`
3. Deve abrir uma janela pequena de teste

#### Problema: Template não encontrado
**Solução**:
1. Verifique se o arquivo Excel existe
2. Certifique-se de que o arquivo não está aberto em outro programa
3. Use o botão "📂 Procurar" para selecionar novamente

#### Problema: Bases não detectadas
**Solução**:
1. Verifique se os arquivos seguem o padrão `BASE-arquivo.csv`
2. Certifique-se de que há pelo menos 5 arquivos por base
3. Verifique se a pasta está correta

#### Problema: Processamento lento
**Solução**:
- Use o **Modo Rápido** em vez do Modo Completo
- Feche outros programas pesados
- Processe uma base por vez se necessário

### 💡 Dicas para Usuários Não Técnicos

#### Primeira Execução
1. **Seja paciente**: A primeira execução pode demorar 2-5 minutos
2. **Não feche** o PyCharm durante a instalação de dependências
3. **Aguarde** a mensagem "Sistema iniciado" aparecer

#### Uso Regular
1. **Sempre comece pela Aba 1** (Configuração)
2. **Siga a ordem das abas**: 1 → 2 → 3 → 4
3. **Use os botões coloridos** como guia de prioridade
4. **Leia as mensagens** na parte inferior da tela

#### Organização de Arquivos
1. **Mantenha** seus arquivos CSV organizados por base
2. **Use** a pasta padrão para facilitar o uso
3. **Faça backup** dos resultados importantes
4. **Nomeie** os arquivos seguindo o padrão `BASE-arquivo.csv`

### 📞 Suporte e Ajuda

#### Logs Detalhados
- **Aba 4 (Logs)**: Informações técnicas detalhadas
- **Botão "💾 Exportar Logs"**: Para enviar para suporte técnico
- **Mensagens na interface**: Orientações em tempo real

#### Informações do Sistema
- **Barra inferior**: Status atual do processamento
- **Áreas de texto**: Resultados e mensagens importantes
- **Botões "📁 Abrir Pasta"**: Acesso direto aos resultados

#### Em Caso de Problemas
1. **Consulte a Aba 4** para logs detalhados
2. **Exporte os logs** usando o botão específico
3. **Anote** a mensagem de erro exata
4. **Tente** reiniciar o sistema
5. **Verifique** se todos os arquivos estão acessíveis

---

**Este guia foi criado especificamente para usuários não técnicos. Siga os passos em ordem e use as cores dos botões como guia de prioridade. O sistema foi projetado para ser intuitivo e amigável.**

