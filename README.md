# Sistema de Validação de Dados Logísticos v8.0 - Otimizado

## Visão Geral

Sistema avançado de validação de dados logísticos com processamento otimizado e interface amigável para usuários não técnicos. Versão 8.0 com melhorias significativas de performance e usabilidade.

## Principais Funcionalidades

### ⚡ Processamento Otimizado
- **Modo Rápido**: Validação essencial em segundos
- **Modo Completo**: Análise detalhada com estatísticas e gráficos
- **Auto-instalação**: Dependências instaladas automaticamente

### 🎯 Interface com Guia Visual
- **Prioridades coloridas**: Botões com cores indicando importância
- **Fluxo guiado**: Passos claros e organizados
- **4 abas intuitivas**: Configuração → Processamento → Relatórios → Logs

### 🔍 Validação Universal
- **Qualquer quantidade de bases**: Não limitado a bases específicas
- **Duas estruturas**: `BASE-arquivo.csv` e `\\BASE\arquivo.csv`
- **Preservação de encoding**: Mantém codificação original dos arquivos
- **Criação automática**: Arquivo `vazao-ilhas.csv` gerado automaticamente

### 📊 Relatórios Profissionais
- **Tabela Excel de campos obrigatórios**: Por arquivo e base
- **Tabela Excel de inconsistências**: Nomenclatura com recomendações
- **Relatórios por base**: Status e problemas detectados
- **Visualizações gráficas**: Estatísticas e análises avançadas

## Requisitos do Sistema

### Software Necessário
- Python 3.8 ou superior
- PyCharm (recomendado) ou qualquer IDE Python
- Sistema operacional: Windows, macOS ou Linux

### Dependências (Instaladas Automaticamente)
- pandas
- numpy
- matplotlib
- seaborn
- chardet
- openpyxl
- xlsxwriter
- tkinter (incluído no Python)

## Instalação e Configuração

### 1. Preparação do Ambiente
```bash
# Clone ou descompacte o projeto
cd validador_otimizado_v8

# O sistema instalará dependências automaticamente na primeira execução
```

### 2. Execução no PyCharm
1. Abra o PyCharm
2. Clique em "Open" e selecione a pasta `validador_otimizado_v8`
3. Abra o arquivo `sistema_validacao_v8_otimizado.py`
4. Clique no botão "Run" (▶️)
5. Aguarde a instalação automática de dependências (primeira execução)

### 3. Execução via Terminal
```bash
python sistema_validacao_v8_otimizado.py
```

## Guia de Uso

### 🔴 Passo 1: Configuração (OBRIGATÓRIO)
1. **Selecionar Template Excel**: Arquivo com campos obrigatórios preenchidos
2. **Escolher localização dos dados**:
   - **Pasta padrão**: `Documents/ValidadorLogistico/dados_entrada/`
   - **Pasta personalizada**: Selecionar via botão "Procurar"
3. **Analisar Template**: Clique em "Analisar Template"
4. **Detectar Bases**: Clique em "Detectar Bases Disponíveis"

### 🟡 Passo 2: Processamento (RECOMENDADO)
1. **Escolher modo de processamento**:
   - **⚡ Rápido**: Validação essencial (segundos)
   - **📊 Completo**: Com estatísticas e gráficos (minutos)
2. **Processar bases**:
   - **Todas as bases**: Processamento em lote
   - **Base específica**: Seleção individual

### 🟡 Passo 3: Relatórios (RECOMENDADO)
1. **Gerar Tabela de Campos Obrigatórios**: Excel com status por base
2. **Gerar Tabela de Inconsistências**: Problemas de nomenclatura
3. **Gráficos e Estatísticas**: Visualizações avançadas (opcional)

### ⚪ Passo 4: Logs (AVANÇADO)
- Monitoramento detalhado do processamento
- Exportação de logs para análise
- Limpeza de logs antigos

## Estrutura de Arquivos Gerados

```
Documents/ValidadorLogistico/
├── dados_entrada/                    # Pasta padrão para dados brutos
├── output/                          # Resultados do processamento
│   ├── BASE1/
│   │   ├── input/                   # Arquivos processados (sem prefixo)
│   │   │   ├── agend.csv
│   │   │   ├── baias.csv
│   │   │   ├── vazao-ilhas.csv      # Criado automaticamente
│   │   │   └── ... (outros arquivos)
│   │   ├── relatorio_validacao_BASE1.md
│   │   └── relatorio_completo_BASE1.md (se modo completo)
│   └── BASE2/
│       └── ... (estrutura similar)
├── tabela_campos_obrigatorios_[data].xlsx
├── tabela_inconsistencias_[data].xlsx
├── graficos_gerais/                 # Gráficos consolidados
└── logs/                           # Logs do sistema
```

## Funcionalidades Detalhadas

### Processamento Rápido vs Completo

#### ⚡ Modo Rápido (Recomendado)
- **Tempo**: Segundos
- **Funcionalidades**:
  - Validação de campos obrigatórios
  - Detecção de inconsistências de nomenclatura
  - Relatório por base
  - Tabelas Excel essenciais

#### 📊 Modo Completo
- **Tempo**: Minutos
- **Funcionalidades**:
  - Tudo do Modo Rápido +
  - Resumo estatístico detalhado
  - Gráficos e visualizações
  - Análises avançadas por arquivo

### Detecção de Inconsistências

O sistema identifica automaticamente:
- **Problemas de espaçamento**: "Capacidade (m3)" vs "Capacidade(m3)"
- **Acentuação**: "pátio" vs "patio"
- **Caracteres especiais**: Variações de nomenclatura
- **Recomendações**: Padronização sugerida

### Validação de Campos Obrigatórios

- **Baseada no template Excel**: Campos com dados são considerados obrigatórios
- **Verificação por base**: Status individual de cada base
- **Relatório detalhado**: Campos faltantes por arquivo
- **Status final**: Pronto para parser ou requer correções

## Orientações para Usuários Não Técnicos

### Primeira Execução
1. **Descompacte** o arquivo ZIP do projeto
2. **Abra o PyCharm** e selecione a pasta do projeto
3. **Clique em "Run"** no arquivo principal
4. **Aguarde** a instalação automática (pode demorar alguns minutos)
5. **Use a interface gráfica** que abrirá automaticamente

### Fluxo Recomendado
1. **Configure** o template Excel (aba 1)
2. **Processe** no modo rápido (aba 2)
3. **Gere** as tabelas Excel (aba 3)
4. **Revise** inconsistências detectadas
5. **Abra** as pastas de resultados usando os botões

### Localização dos Resultados
- **Pasta padrão**: `C:\Users\[seu_nome]\Documents\ValidadorLogistico\`
- **Botões "Abrir Pasta"**: Acesso direto aos resultados
- **Mensagens na interface**: Localização exata dos arquivos gerados

## Solução de Problemas

### Erro de Dependências
- **Problema**: "No module named 'pandas'"
- **Solução**: O sistema instala automaticamente na primeira execução

### Erro de Template
- **Problema**: Template não encontrado
- **Solução**: Verifique se o arquivo Excel existe e está acessível

### Erro de Dados
- **Problema**: Bases não detectadas
- **Solução**: Verifique se os arquivos seguem o padrão `BASE-arquivo.csv`

### Performance Lenta
- **Problema**: Processamento demorado
- **Solução**: Use o Modo Rápido em vez do Modo Completo

## Suporte e Contato

### Logs Detalhados
- Consulte a **aba 4 (Logs)** para informações detalhadas
- Use **"Exportar Logs"** para enviar logs para suporte

### Estrutura de Suporte
- **Logs automáticos**: Todas as operações são registradas
- **Mensagens claras**: Interface informa problemas e soluções
- **Botões de ajuda**: Acesso direto às pastas de resultados

## Informações Técnicas

### Autor
**Fabrício Pinheiro Souza**  
Analista de Dados Sênior

### Versão
8.0 - Otimizada com Processamento Rápido/Completo

### Data
06/06/2025

### Licença
Uso interno - Projeto de otimização logística

---

**Sistema desenvolvido para análise universal de bases de dados logísticos, com foco na identificação de campos obrigatórios e inconsistências de nomenclatura para otimização do processo de parsing e validação de dados.**

