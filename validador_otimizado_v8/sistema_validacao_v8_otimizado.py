#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Validação de Dados Logísticos - Versão 8.0 Otimizada
Autor: Fabrício Pinheiro Souza / Analista de Dados Sênior
Data: 06/06/2025
Versão: 8.0 - Otimizada com Processamento Rápido/Completo
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import logging
from datetime import datetime
import re
import threading
import subprocess
import shutil
import chardet
import time

# Auto-instalação de dependências
def instalar_dependencias():
    """Instala dependências automaticamente se necessário"""
    dependencias = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'chardet', 'openpyxl', 'xlsxwriter'
    ]
    
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            print(f"📦 Instalando {dep}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])

# Instala dependências na primeira execução
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
except ImportError:
    print("🔍 Verificando dependências...")
    instalar_dependencias()
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

class ValidadorLogisticoOtimizado:
    """Sistema de Validação de Dados Logísticos - Versão 8.0 Otimizada"""
    
    def __init__(self):
        """Inicializa o sistema"""
        self.root = None
        self.setup_logging()
        self.inicializar_variaveis()
        self.criar_interface_gui()
        
    def setup_logging(self):
        """Configura sistema de logging funcional"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"validador_v8_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        logging.info("🚀 Sistema de Validação v8.0 Otimizado iniciado")
        
    def inicializar_variaveis(self):
        """Inicializa todas as variáveis do sistema"""
        # Caminhos e configurações
        self.pasta_padrao = Path.home() / "Documents" / "ValidadorLogistico"
        self.template_excel_path = None
        self.dados_brutos_path = None
        self.pasta_saida = None
        
        # Dados de análise
        self.campos_obrigatorios = {}
        self.bases_detectadas = []
        self.resultados_validacao = {}
        self.inconsistencias_nomenclatura = {}
        
        # Configurações de processamento
        self.modo_processamento = "rapido"  # "rapido" ou "completo"
        
        # Interface
        self.notebook = None
        self.progress_var = None
        self.progress_bar = None
        self.status_text = None
        self.tree_bases = None
        self.tree_inconsistencias = None
        
    def criar_interface_gui(self):
        """Cria interface gráfica amigável com guia visual"""
        self.root = tk.Tk()
        self.root.title("Sistema de Validação de Dados Logísticos v8.0 - Otimizado")
        self.root.geometry("1500x950")
        self.root.configure(bg='#f0f0f0')
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores para prioridades
        style.configure('Obrigatorio.TButton', background='#e74c3c', foreground='white')
        style.configure('Recomendado.TButton', background='#f39c12', foreground='white')
        style.configure('Opcional.TButton', background='#27ae60', foreground='white')
        style.configure('Avancado.TButton', background='#95a5a6', foreground='white')
        
        # Título principal
        titulo_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        titulo_frame.pack(fill='x', pady=(0,10))
        titulo_frame.pack_propagate(False)
        
        titulo_label = tk.Label(
            titulo_frame, 
            text="⚡ Sistema de Validação de Dados Logísticos v8.0 - OTIMIZADO",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        titulo_label.pack(expand=True)
        
        subtitulo_label = tk.Label(
            titulo_frame,
            text="🚀 Processamento Rápido • 📊 Análise Completa • 🎯 Guia Visual de Prioridades",
            font=('Arial', 10),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitulo_label.pack()
        
        # Guia de prioridades
        self.criar_guia_prioridades()
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Criar abas
        self.criar_aba_configuracao()
        self.criar_aba_processamento()
        self.criar_aba_relatorios()
        self.criar_aba_logs()
        
        # Barra de status
        self.criar_barra_status()
        
    def criar_guia_prioridades(self):
        """Cria guia visual de prioridades dos botões"""
        guia_frame = tk.Frame(self.root, bg='#ecf0f1', height=60)
        guia_frame.pack(fill='x', padx=10, pady=(0,5))
        guia_frame.pack_propagate(False)
        
        tk.Label(guia_frame, text="🎯 GUIA DE PRIORIDADES:", 
                font=('Arial', 10, 'bold'), bg='#ecf0f1').pack(side='left', padx=10)
        
        # Legendas coloridas
        cores_prioridades = [
            ("🔴 OBRIGATÓRIO", "#e74c3c", "Clique primeiro"),
            ("🟡 RECOMENDADO", "#f39c12", "Para melhores resultados"),
            ("🟢 OPCIONAL", "#27ae60", "Pode pular se quiser rapidez"),
            ("⚪ AVANÇADO", "#95a5a6", "Apenas se precisar de detalhes")
        ]
        
        for texto, cor, tooltip in cores_prioridades:
            label = tk.Label(guia_frame, text=texto, bg=cor, fg='white', 
                           font=('Arial', 8, 'bold'), padx=8, pady=2)
            label.pack(side='left', padx=5)
            
    def criar_aba_configuracao(self):
        """Cria aba de configuração com prioridades visuais"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔴 1. Configuração (OBRIGATÓRIO)")
        
        # Instruções claras
        instrucoes_frame = tk.Frame(frame, bg='#e8f4fd', relief='solid', bd=1)
        instrucoes_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(instrucoes_frame, 
                text="📋 PASSO 1: Configure o template Excel e localização dos dados (OBRIGATÓRIO)",
                font=('Arial', 12, 'bold'), bg='#e8f4fd', fg='#2c3e50').pack(pady=10)
        
        # Seção Template Excel
        template_frame = ttk.LabelFrame(frame, text="📋 Template Excel com Campos Obrigatórios", padding=15)
        template_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(template_frame, text="Selecione o arquivo Excel que contém os campos obrigatórios preenchidos:", 
                 font=('Arial', 10)).pack(anchor='w', pady=(0,5))
        
        template_path_frame = ttk.Frame(template_frame)
        template_path_frame.pack(fill='x', pady=5)
        
        self.template_path_var = tk.StringVar()
        template_entry = ttk.Entry(template_path_frame, textvariable=self.template_path_var, 
                                 width=80, font=('Arial', 9))
        template_entry.pack(side='left', fill='x', expand=True, padx=(0,10))
        
        ttk.Button(template_path_frame, text="📂 Procurar", 
                  command=self.selecionar_template, style='Obrigatorio.TButton').pack(side='right')
        
        ttk.Button(template_frame, text="🔴 Analisar Template (OBRIGATÓRIO)", 
                  command=self.analisar_template, style='Obrigatorio.TButton').pack(pady=10)
        
        # Seção Dados Brutos
        dados_frame = ttk.LabelFrame(frame, text="📊 Localização dos Dados Brutos", padding=15)
        dados_frame.pack(fill='x', padx=20, pady=10)
        
        # Opções de localização
        self.dados_opcao_var = tk.StringVar(value="padrao")
        
        ttk.Radiobutton(dados_frame, text="📁 Usar pasta padrão (Recomendado)", 
                       variable=self.dados_opcao_var, value="padrao",
                       command=self.atualizar_opcao_dados).pack(anchor='w', pady=5)
        
        self.pasta_padrao_label = tk.Label(dados_frame, 
                                          text=f"📂 {self.pasta_padrao / 'dados_entrada'}",
                                          font=('Arial', 9), fg='#7f8c8d')
        self.pasta_padrao_label.pack(anchor='w', padx=20)
        
        ttk.Button(dados_frame, text="📁 Abrir Pasta Padrão", 
                  command=self.abrir_pasta_padrao, style='Recomendado.TButton').pack(anchor='w', padx=20, pady=5)
        
        ttk.Radiobutton(dados_frame, text="🎯 Selecionar pasta personalizada", 
                       variable=self.dados_opcao_var, value="personalizada",
                       command=self.atualizar_opcao_dados).pack(anchor='w', pady=(10,5))
        
        dados_path_frame = ttk.Frame(dados_frame)
        dados_path_frame.pack(fill='x', pady=5, padx=20)
        
        self.dados_path_var = tk.StringVar()
        self.dados_entry = ttk.Entry(dados_path_frame, textvariable=self.dados_path_var, 
                                   width=70, font=('Arial', 9), state='disabled')
        self.dados_entry.pack(side='left', fill='x', expand=True, padx=(0,10))
        
        self.dados_browse_btn = ttk.Button(dados_path_frame, text="📂 Procurar", 
                                         command=self.selecionar_dados, state='disabled')
        self.dados_browse_btn.pack(side='right')
        
        # Botão de detecção
        ttk.Button(dados_frame, text="🔴 Detectar Bases Disponíveis (OBRIGATÓRIO)", 
                  command=self.detectar_bases, style='Obrigatorio.TButton').pack(pady=15)
        
    def criar_aba_processamento(self):
        """Cria aba de processamento com opções rápido/completo"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🟡 2. Processamento (RECOMENDADO)")
        
        # Instruções
        instrucoes_frame = tk.Frame(frame, bg='#fff3cd', relief='solid', bd=1)
        instrucoes_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(instrucoes_frame, 
                text="⚡ PASSO 2: Escolha o tipo de processamento (RECOMENDADO: Rápido)",
                font=('Arial', 12, 'bold'), bg='#fff3cd', fg='#856404').pack(pady=10)
        
        # Opções de processamento
        processamento_frame = ttk.LabelFrame(frame, text="⚡ Modo de Processamento", padding=15)
        processamento_frame.pack(fill='x', padx=20, pady=10)
        
        self.modo_var = tk.StringVar(value="rapido")
        
        # Modo Rápido
        rapido_frame = tk.Frame(processamento_frame, bg='#d4edda', relief='solid', bd=1)
        rapido_frame.pack(fill='x', pady=5)
        
        ttk.Radiobutton(rapido_frame, text="⚡ PROCESSAMENTO RÁPIDO (Recomendado - Segundos)", 
                       variable=self.modo_var, value="rapido").pack(anchor='w', padx=10, pady=5)
        
        tk.Label(rapido_frame, text="✅ Validação de campos obrigatórios\n"
                                   "✅ Detecção de inconsistências de nomenclatura\n"
                                   "✅ Relatório por base\n"
                                   "✅ Tabelas Excel (campos obrigatórios + inconsistências)",
                bg='#d4edda', font=('Arial', 9), justify='left').pack(anchor='w', padx=30, pady=(0,10))
        
        # Modo Completo
        completo_frame = tk.Frame(processamento_frame, bg='#f8d7da', relief='solid', bd=1)
        completo_frame.pack(fill='x', pady=5)
        
        ttk.Radiobutton(completo_frame, text="📊 PROCESSAMENTO COMPLETO (Opcional - Minutos)", 
                       variable=self.modo_var, value="completo").pack(anchor='w', padx=10, pady=5)
        
        tk.Label(completo_frame, text="✅ Tudo do Modo Rápido +\n"
                                     "📈 Resumo estatístico detalhado\n"
                                     "📊 Gráficos e visualizações\n"
                                     "🔍 Análises avançadas",
                bg='#f8d7da', font=('Arial', 9), justify='left').pack(anchor='w', padx=30, pady=(0,10))
        
        # Botões de processamento
        botoes_frame = ttk.Frame(processamento_frame)
        botoes_frame.pack(fill='x', pady=15)
        
        ttk.Button(botoes_frame, text="🟡 Processar Todas as Bases (RECOMENDADO)", 
                  command=self.processar_todas_bases, style='Recomendado.TButton').pack(side='left', padx=(0,10))
        
        ttk.Button(botoes_frame, text="🎯 Processar Base Específica", 
                  command=self.processar_base_especifica, style='Opcional.TButton').pack(side='left')
        
        # Progresso
        progress_frame = ttk.LabelFrame(frame, text="📊 Progresso do Processamento", padding=10)
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=10)
        
        self.progress_label = tk.Label(progress_frame, text="Aguardando processamento...", 
                                     font=('Arial', 10))
        self.progress_label.pack()
        
        # Resultados
        resultados_frame = ttk.LabelFrame(frame, text="📋 Bases Detectadas e Status", padding=10)
        resultados_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        colunas = ('Base', 'Status', 'Arquivos Válidos', 'Total Arquivos', 'Observações')
        self.tree_bases = ttk.Treeview(resultados_frame, columns=colunas, show='headings', height=10)
        
        for col in colunas:
            self.tree_bases.heading(col, text=col)
            self.tree_bases.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(resultados_frame, orient='vertical', command=self.tree_bases.yview)
        self.tree_bases.configure(yscrollcommand=scrollbar.set)
        
        self.tree_bases.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def criar_aba_relatorios(self):
        """Cria aba de relatórios"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🟡 3. Relatórios (RECOMENDADO)")
        
        # Instruções
        instrucoes_frame = tk.Frame(frame, bg='#fff3cd', relief='solid', bd=1)
        instrucoes_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(instrucoes_frame, 
                text="📋 PASSO 3: Gere relatórios Excel para análise (RECOMENDADO)",
                font=('Arial', 12, 'bold'), bg='#fff3cd', fg='#856404').pack(pady=10)
        
        # Controles de relatórios
        controles_frame = ttk.LabelFrame(frame, text="📊 Geração de Relatórios", padding=15)
        controles_frame.pack(fill='x', padx=20, pady=10)
        
        botoes_rel_frame = ttk.Frame(controles_frame)
        botoes_rel_frame.pack(fill='x', pady=10)
        
        ttk.Button(botoes_rel_frame, text="🟡 Tabela Campos Obrigatórios (Excel)", 
                  command=self.gerar_tabela_campos_obrigatorios, 
                  style='Recomendado.TButton').pack(side='left', padx=(0,10))
        
        ttk.Button(botoes_rel_frame, text="🟡 Tabela Inconsistências (Excel)", 
                  command=self.gerar_tabela_inconsistencias,
                  style='Recomendado.TButton').pack(side='left', padx=(0,10))
        
        ttk.Button(botoes_rel_frame, text="🟢 Gráficos e Estatísticas (OPCIONAL)", 
                  command=self.gerar_graficos_estatisticas,
                  style='Opcional.TButton').pack(side='left')
        
        # Botões de abertura de pastas
        pastas_frame = ttk.Frame(controles_frame)
        pastas_frame.pack(fill='x', pady=10)
        
        ttk.Button(pastas_frame, text="📁 Abrir Pasta de Resultados", 
                  command=self.abrir_pasta_resultados,
                  style='Recomendado.TButton').pack(side='left', padx=(0,10))
        
        ttk.Button(pastas_frame, text="📁 Abrir Pasta de Logs", 
                  command=self.abrir_pasta_logs,
                  style='Opcional.TButton').pack(side='left')
        
        # Inconsistências detectadas
        inconsistencias_frame = ttk.LabelFrame(frame, text="⚠️ Inconsistências de Nomenclatura Detectadas", padding=10)
        inconsistencias_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        colunas_inc = ('Arquivo', 'Campo Obrigatório', 'Variação Encontrada', 'Bases Afetadas', 'Tipo Problema')
        self.tree_inconsistencias = ttk.Treeview(inconsistencias_frame, columns=colunas_inc, show='headings', height=15)
        
        for col in colunas_inc:
            self.tree_inconsistencias.heading(col, text=col)
            self.tree_inconsistencias.column(col, width=180)
        
        scrollbar_inc = ttk.Scrollbar(inconsistencias_frame, orient='vertical', command=self.tree_inconsistencias.yview)
        self.tree_inconsistencias.configure(yscrollcommand=scrollbar_inc.set)
        
        self.tree_inconsistencias.pack(side='left', fill='both', expand=True)
        scrollbar_inc.pack(side='right', fill='y')
        
    def criar_aba_logs(self):
        """Cria aba de logs"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚪ 4. Logs (AVANÇADO)")
        
        # Instruções
        instrucoes_frame = tk.Frame(frame, bg='#e2e3e5', relief='solid', bd=1)
        instrucoes_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(instrucoes_frame, 
                text="📝 PASSO 4: Monitore logs detalhados (AVANÇADO - Pode pular)",
                font=('Arial', 12, 'bold'), bg='#e2e3e5', fg='#6c757d').pack(pady=10)
        
        # Controles de logs
        controles_logs = ttk.Frame(frame)
        controles_logs.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(controles_logs, text="🔄 Atualizar Logs", 
                  command=self.atualizar_logs, style='Avancado.TButton').pack(side='left', padx=(0,10))
        ttk.Button(controles_logs, text="🗑️ Limpar Logs", 
                  command=self.limpar_logs, style='Avancado.TButton').pack(side='left', padx=(0,10))
        ttk.Button(controles_logs, text="💾 Exportar Logs", 
                  command=self.exportar_logs, style='Avancado.TButton').pack(side='left')
        
        # Área de logs
        logs_frame = ttk.LabelFrame(frame, text="📋 Logs do Sistema", padding=10)
        logs_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=20, font=('Consolas', 9))
        self.logs_text.pack(fill='both', expand=True)
        
    def criar_barra_status(self):
        """Cria barra de status"""
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Sistema iniciado - Configure o template Excel primeiro", 
                                   bg='#34495e', fg='white', font=('Arial', 9))
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Indicador de modo
        self.modo_label = tk.Label(status_frame, text="Modo: Rápido", 
                                 bg='#27ae60', fg='white', font=('Arial', 9, 'bold'), padx=10)
        self.modo_label.pack(side='right', padx=10, pady=2)
        
    def log_status(self, mensagem: str, nivel: str = "INFO"):
        """Registra status no log e interface"""
        if nivel == "ERROR":
            logging.error(mensagem)
        else:
            logging.info(mensagem)
            
        # Atualiza interface
        if hasattr(self, 'status_label'):
            self.status_label.config(text=mensagem)
            
        if hasattr(self, 'logs_text'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.logs_text.insert(tk.END, f"[{timestamp}] {mensagem}\n")
            self.logs_text.see(tk.END)
            
        self.root.update_idletasks()
        
    def atualizar_opcao_dados(self):
        """Atualiza opções de localização de dados"""
        if self.dados_opcao_var.get() == "padrao":
            self.dados_entry.config(state='disabled')
            self.dados_browse_btn.config(state='disabled')
            self.dados_path_var.set(str(self.pasta_padrao / "dados_entrada"))
        else:
            self.dados_entry.config(state='normal')
            self.dados_browse_btn.config(state='normal')
            
    def abrir_pasta_padrao(self):
        """Abre pasta padrão e cria se necessário"""
        pasta_dados = self.pasta_padrao / "dados_entrada"
        pasta_dados.mkdir(parents=True, exist_ok=True)
        
        try:
            if sys.platform == "win32":
                os.startfile(pasta_dados)
            elif sys.platform == "darwin":
                subprocess.run(["open", pasta_dados])
            else:
                subprocess.run(["xdg-open", pasta_dados])
                
            self.log_status(f"📁 Pasta padrão aberta: {pasta_dados}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta:\n{e}")
            
    def selecionar_template(self):
        """Seleciona arquivo template Excel"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Template Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if arquivo:
            self.template_path_var.set(arquivo)
            self.template_excel_path = Path(arquivo)
            self.log_status(f"📋 Template selecionado: {arquivo}")
            
    def selecionar_dados(self):
        """Seleciona pasta de dados"""
        pasta = filedialog.askdirectory(title="Selecionar Pasta de Dados")
        if pasta:
            self.dados_path_var.set(pasta)
            self.log_status(f"📊 Pasta de dados selecionada: {pasta}")
            
    def analisar_template(self):
        """Analisa template Excel para identificar campos obrigatórios"""
        if not self.template_excel_path or not self.template_excel_path.exists():
            messagebox.showerror("Erro", "Selecione um arquivo template Excel válido primeiro!")
            return
            
        try:
            self.log_status("🔍 Analisando template Excel...")
            
            # Mapear abas Excel para arquivos CSV
            mapeamento_abas = {
                'Agendamentos': 'agend.csv',
                'Veículos': 'Veiculos.csv',
                'Produtos': 'produtos.csv',
                'Pátios': 'patios.csv',
                'Ilhas': 'ilhas.csv',
                'Baias': 'baias.csv',
                'Braços-Produtos': 'bracos-produtos.csv',
                'Grades': 'grades.csv',
                'Grades-Clientes': 'grades-clientes.csv',
                'Grades-Produtos': 'grades-produtos.csv',
                'Grades-Clientes-Produtos': 'grades-clientes-produtos.csv',
                'Grades-Cotas-Clientes': 'grades-cotas-clientes.csv',
                'Grades-Cotas-Produtos': 'grades-cotas-produtos.csv',
                'Grades-Fixação-Horários': 'grades-fixacao-horarios.csv',
                'Horários-Pátios': 'horarios-patios.csv',
                'Produtos-Agend': 'produtos-agend.csv',
                'EV': 'EV.csv',
                'Vazão-Ilhas': 'vazao-ilhas.csv'
            }
            
            self.campos_obrigatorios = {}
            
            # Lê arquivo Excel
            excel_file = pd.ExcelFile(self.template_excel_path)
            
            for aba, arquivo_csv in mapeamento_abas.items():
                if aba in excel_file.sheet_names:
                    df = pd.read_excel(self.template_excel_path, sheet_name=aba)
                    
                    # Identifica campos com dados (não vazios)
                    campos_com_dados = []
                    for coluna in df.columns:
                        if not df[coluna].isna().all() and not (df[coluna] == '').all():
                            campos_com_dados.append(coluna)
                    
                    self.campos_obrigatorios[arquivo_csv] = campos_com_dados
                    self.log_status(f"✅ {arquivo_csv}: {len(campos_com_dados)} campos obrigatórios")
                else:
                    self.campos_obrigatorios[arquivo_csv] = []
                    self.log_status(f"⚠️ Aba '{aba}' não encontrada no template")
            
            total_campos = sum(len(campos) for campos in self.campos_obrigatorios.values())
            arquivos_com_campos = len([arq for arq, campos in self.campos_obrigatorios.items() if len(campos) > 0])
            
            self.log_status(f"✅ Template analisado com sucesso!")
            self.log_status(f"📊 {total_campos} campos obrigatórios em {arquivos_com_campos} arquivos")
            
            messagebox.showinfo("Sucesso", f"Template analisado com sucesso!\n\n"
                               f"• {total_campos} campos obrigatórios encontrados\n"
                               f"• {arquivos_com_campos} arquivos com campos obrigatórios\n"
                               f"• {len(self.campos_obrigatorios)} arquivos mapeados")
            
        except Exception as e:
            self.log_status(f"❌ Erro ao analisar template: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao analisar template:\n{e}")
            
    def detectar_bases(self):
        """Detecta bases disponíveis"""
        if self.dados_opcao_var.get() == "padrao":
            diretorio = Path(self.dados_path_var.get())
        else:
            diretorio = Path(self.dados_path_var.get()) if self.dados_path_var.get() else None
            
        if not diretorio or not diretorio.exists():
            messagebox.showerror("Erro", f"Diretório não encontrado:\n{diretorio}")
            return
            
        try:
            self.log_status("🎯 Detectando bases disponíveis...")
            
            bases = set()
            
            # Estrutura 1: BASE-arquivo.csv
            for arquivo in diretorio.glob("*.csv"):
                if '-' in arquivo.name:
                    base = arquivo.name.split('-')[0]
                    if self._verificar_base_valida(diretorio, base):
                        bases.add(base)
            
            # Estrutura 2: \\BASE\arquivo.csv
            for pasta in diretorio.iterdir():
                if pasta.is_dir():
                    if self._verificar_pasta_base_valida(pasta):
                        bases.add(pasta.name)
            
            self.bases_detectadas = sorted(list(bases))
            
            if self.bases_detectadas:
                self.log_status(f"✅ {len(self.bases_detectadas)} bases detectadas: {', '.join(self.bases_detectadas)}")
                messagebox.showinfo("Bases Detectadas", 
                                   f"{len(self.bases_detectadas)} bases encontradas:\n\n" + 
                                   "\n".join([f"• {base}" for base in self.bases_detectadas]))
                self._atualizar_tree_bases()
            else:
                self.log_status("⚠️ Nenhuma base detectada")
                messagebox.showwarning("Aviso", "Nenhuma base foi detectada no diretório especificado.")
                
        except Exception as e:
            self.log_status(f"❌ Erro ao detectar bases: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao detectar bases:\n{e}")
            
    def _verificar_base_valida(self, diretorio: Path, base: str) -> bool:
        """Verifica se uma base é válida (tem arquivos suficientes)"""
        arquivos_base = list(diretorio.glob(f"{base}-*.csv"))
        return len(arquivos_base) >= 5  # Mínimo de 5 arquivos para ser considerada base válida
        
    def _verificar_pasta_base_valida(self, pasta: Path) -> bool:
        """Verifica se uma pasta contém uma base válida"""
        arquivos_csv = list(pasta.glob("*.csv"))
        return len(arquivos_csv) >= 5  # Mínimo de 5 arquivos CSV
        
    def _atualizar_tree_bases(self):
        """Atualiza tree view com bases detectadas"""
        # Limpa tree
        for item in self.tree_bases.get_children():
            self.tree_bases.delete(item)
            
        # Adiciona bases
        for base in self.bases_detectadas:
            self.tree_bases.insert('', 'end', values=(base, 'Detectada', '-', '-', 'Aguardando processamento'))
            
    def processar_todas_bases(self):
        """Processa todas as bases detectadas"""
        if not self.bases_detectadas:
            messagebox.showerror("Erro", "Nenhuma base detectada! Execute a detecção primeiro.")
            return
            
        if not self.campos_obrigatorios:
            messagebox.showerror("Erro", "Template não analisado! Analise o template Excel primeiro.")
            return
            
        # Atualiza modo de processamento
        self.modo_processamento = self.modo_var.get()
        
        if self.modo_processamento == "rapido":
            self.modo_label.config(text="Modo: Rápido ⚡", bg='#27ae60')
        else:
            self.modo_label.config(text="Modo: Completo 📊", bg='#e74c3c')
            
        # Executa processamento em thread separada
        thread = threading.Thread(target=self._processar_bases_thread)
        thread.daemon = True
        thread.start()
        
    def _processar_bases_thread(self):
        """Thread para processamento das bases"""
        try:
            total_bases = len(self.bases_detectadas)
            
            for i, base in enumerate(self.bases_detectadas):
                self.log_status(f"🔄 Processando base {base} ({i+1}/{total_bases})...")
                
                # Atualiza progresso
                progresso = (i / total_bases) * 100
                self.progress_var.set(progresso)
                self.progress_label.config(text=f"Processando {base}... ({i+1}/{total_bases})")
                
                # Processa base
                if self.modo_processamento == "rapido":
                    resultado = self._processar_base_rapido(base)
                else:
                    resultado = self._processar_base_completo(base)
                    
                self.resultados_validacao[base] = resultado
                
                # Atualiza tree
                self._atualizar_resultado_tree(base, resultado)
                
                # Pequena pausa para feedback visual
                time.sleep(0.5)
                
            # Finaliza processamento
            self.progress_var.set(100)
            self.progress_label.config(text="✅ Processamento concluído!")
            
            # Detecta inconsistências
            self._detectar_inconsistencias_nomenclatura()
            
            self.log_status("✅ Todas as bases foram processadas com sucesso!")
            
            # Mostra resumo
            self._mostrar_resumo_processamento()
            
        except Exception as e:
            self.log_status(f"❌ Erro durante processamento: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro durante processamento:\n{e}")
            
    def _processar_base_rapido(self, base: str) -> Dict:
        """Processamento rápido - apenas validação essencial"""
        diretorio = Path(self.dados_path_var.get())
        
        resultado = {
            'base': base,
            'arquivos_processados': 0,
            'arquivos_validos': 0,
            'total_arquivos': len(self.campos_obrigatorios),
            'problemas': [],
            'campos_faltantes': {},
            'tempo_processamento': 0
        }
        
        inicio = time.time()
        
        # Cria pasta de saída
        pasta_base = self.pasta_padrao / "output" / base
        pasta_input = pasta_base / "input"
        pasta_input.mkdir(parents=True, exist_ok=True)
        
        # Processa cada arquivo
        for arquivo_csv, campos_obrigatorios in self.campos_obrigatorios.items():
            try:
                arquivo_original = self._encontrar_arquivo_original(diretorio, base, arquivo_csv)
                
                if arquivo_original:
                    # Copia arquivo preservando encoding
                    arquivo_destino = pasta_input / arquivo_csv
                    self._copiar_arquivo_preservando_encoding(arquivo_original, arquivo_destino)
                    
                    # Cria vazao-ilhas.csv se for ilhas.csv
                    if arquivo_csv == "ilhas.csv":
                        self._criar_vazao_ilhas(arquivo_destino, pasta_input)
                    
                    # Validação rápida de campos obrigatórios
                    if campos_obrigatorios:
                        campos_faltantes = self._validar_campos_rapido(arquivo_destino, campos_obrigatorios)
                        if campos_faltantes:
                            resultado['campos_faltantes'][arquivo_csv] = campos_faltantes
                        else:
                            resultado['arquivos_validos'] += 1
                    else:
                        resultado['arquivos_validos'] += 1
                        
                    resultado['arquivos_processados'] += 1
                    
                else:
                    resultado['problemas'].append(f"Arquivo {arquivo_csv} não encontrado")
                    
            except Exception as e:
                resultado['problemas'].append(f"Erro ao processar {arquivo_csv}: {e}")
        
        resultado['tempo_processamento'] = time.time() - inicio
        
        # Gera relatório rápido
        self._gerar_relatorio_rapido(resultado, pasta_base)
        
        return resultado
        
    def _processar_base_completo(self, base: str) -> Dict:
        """Processamento completo - com estatísticas e análises"""
        # Primeiro faz processamento rápido
        resultado = self._processar_base_rapido(base)
        
        # Adiciona análises estatísticas
        inicio_stats = time.time()
        
        pasta_base = self.pasta_padrao / "output" / base
        pasta_input = pasta_base / "input"
        
        resultado['estatisticas'] = {}
        resultado['graficos_gerados'] = []
        
        # Análise estatística de cada arquivo
        for arquivo_csv in self.campos_obrigatorios.keys():
            arquivo_path = pasta_input / arquivo_csv
            if arquivo_path.exists():
                try:
                    stats = self._analisar_estatisticas_arquivo(arquivo_path)
                    resultado['estatisticas'][arquivo_csv] = stats
                except Exception as e:
                    self.log_status(f"⚠️ Erro ao analisar estatísticas de {arquivo_csv}: {e}")
        
        # Gera gráficos se solicitado
        if resultado['estatisticas']:
            try:
                graficos = self._gerar_graficos_base(resultado, pasta_base)
                resultado['graficos_gerados'] = graficos
            except Exception as e:
                self.log_status(f"⚠️ Erro ao gerar gráficos: {e}")
        
        resultado['tempo_estatisticas'] = time.time() - inicio_stats
        
        # Gera relatório completo
        self._gerar_relatorio_completo(resultado, pasta_base)
        
        return resultado
        
    def _validar_campos_rapido(self, arquivo_path: Path, campos_obrigatorios: List[str]) -> List[str]:
        """Validação rápida de campos obrigatórios"""
        try:
            # Detecta encoding
            with open(arquivo_path, 'rb') as f:
                raw_data = f.read(1024)
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            # Lê apenas o cabeçalho
            df = pd.read_csv(arquivo_path, encoding=encoding, nrows=0)
            colunas_existentes = set(df.columns)
            
            # Verifica campos faltantes
            campos_faltantes = []
            for campo in campos_obrigatorios:
                if campo not in colunas_existentes:
                    # Verifica variações de nomenclatura
                    campo_encontrado = False
                    for coluna in colunas_existentes:
                        if self._campos_similares(campo, coluna):
                            campo_encontrado = True
                            break
                    
                    if not campo_encontrado:
                        campos_faltantes.append(campo)
            
            return campos_faltantes
            
        except Exception as e:
            return [f"Erro ao validar: {e}"]
            
    def _campos_similares(self, campo1: str, campo2: str) -> bool:
        """Verifica se dois campos são similares (possível inconsistência de nomenclatura)"""
        # Remove espaços e converte para minúsculas
        c1 = re.sub(r'\s+', '', campo1.lower())
        c2 = re.sub(r'\s+', '', campo2.lower())
        
        # Verifica se são iguais sem espaços
        if c1 == c2:
            return True
            
        # Verifica outras variações comuns
        variações = [
            (r'[áàâã]', 'a'), (r'[éèê]', 'e'), (r'[íì]', 'i'),
            (r'[óòôõ]', 'o'), (r'[úù]', 'u'), (r'ç', 'c')
        ]
        
        for padrao, substituto in variações:
            c1 = re.sub(padrao, substituto, c1)
            c2 = re.sub(padrao, substituto, c2)
        
        return c1 == c2
        
    def _encontrar_arquivo_original(self, diretorio: Path, base: str, arquivo_csv: str) -> Optional[Path]:
        """Encontra arquivo original da base"""
        # Estrutura 1: BASE-arquivo.csv
        arquivo_prefixo = diretorio / f"{base}-{arquivo_csv}"
        if arquivo_prefixo.exists():
            return arquivo_prefixo
            
        # Estrutura 2: \\BASE\arquivo.csv
        arquivo_pasta = diretorio / base / arquivo_csv
        if arquivo_pasta.exists():
            return arquivo_pasta
            
        return None
        
    def _copiar_arquivo_preservando_encoding(self, origem: Path, destino: Path):
        """Copia arquivo preservando encoding original"""
        try:
            # Detecta encoding
            with open(origem, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            # Lê com encoding detectado
            with open(origem, 'r', encoding=encoding) as f:
                conteudo = f.read()
            
            # Salva com mesmo encoding
            with open(destino, 'w', encoding=encoding, newline='') as f:
                f.write(conteudo)
                
        except Exception as e:
            # Fallback: copia binário
            shutil.copy2(origem, destino)
            
    def _criar_vazao_ilhas(self, arquivo_ilhas: Path, pasta_destino: Path):
        """Cria arquivo vazao-ilhas.csv a partir de ilhas.csv"""
        try:
            # Detecta encoding
            with open(arquivo_ilhas, 'rb') as f:
                raw_data = f.read(1024)
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            # Lê arquivo ilhas
            df = pd.read_csv(arquivo_ilhas, encoding=encoding)
            
            # Cria vazao-ilhas com estrutura específica
            if 'VazaoMaxima(p95)' in df.columns:
                vazao_df = df[['Codigo', 'DescricaoPatio', 'VazaoMaxima(p95)']].copy()
                
                # Remove coluna VazaoMaxima(p95) do arquivo ilhas original
                df_ilhas_sem_vazao = df.drop('VazaoMaxima(p95)', axis=1)
                df_ilhas_sem_vazao.to_csv(arquivo_ilhas, index=False, encoding=encoding)
                
                # Salva vazao-ilhas
                vazao_path = pasta_destino / "vazao-ilhas.csv"
                vazao_df.to_csv(vazao_path, index=False, encoding=encoding)
                
                self.log_status(f"✅ Arquivo vazao-ilhas.csv criado com {len(vazao_df)} registros")
            else:
                self.log_status("⚠️ Coluna VazaoMaxima(p95) não encontrada em ilhas.csv")
                
        except Exception as e:
            self.log_status(f"❌ Erro ao criar vazao-ilhas.csv: {e}")
            
    def _gerar_relatorio_rapido(self, resultado: Dict, pasta_base: Path):
        """Gera relatório rápido da base"""
        relatorio_path = pasta_base / f"relatorio_validacao_{resultado['base']}.md"
        
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write(f"# Relatório de Validação - Base {resultado['base']}\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Modo:** Processamento Rápido ⚡\n")
            f.write(f"**Tempo:** {resultado['tempo_processamento']:.2f} segundos\n\n")
            
            f.write("## 📊 Resumo Executivo\n\n")
            f.write(f"- **Arquivos Processados:** {resultado['arquivos_processados']}/{resultado['total_arquivos']}\n")
            f.write(f"- **Arquivos Válidos:** {resultado['arquivos_validos']}/{resultado['total_arquivos']}\n")
            f.write(f"- **Taxa de Sucesso:** {(resultado['arquivos_validos']/resultado['total_arquivos']*100):.1f}%\n")
            
            if resultado['arquivos_validos'] == resultado['total_arquivos']:
                f.write(f"- **Status:** ✅ PRONTO PARA PARSER\n\n")
            else:
                f.write(f"- **Status:** ❌ REQUER CORREÇÕES NO MDRIVER\n\n")
            
            if resultado['campos_faltantes']:
                f.write("## ⚠️ Campos Obrigatórios Faltantes\n\n")
                for arquivo, campos in resultado['campos_faltantes'].items():
                    f.write(f"### {arquivo}\n")
                    for campo in campos:
                        f.write(f"- ❌ {campo}\n")
                    f.write("\n")
            
            if resultado['problemas']:
                f.write("## 🚨 Problemas Detectados\n\n")
                for problema in resultado['problemas']:
                    f.write(f"- ❌ {problema}\n")
                f.write("\n")
            
            f.write("## 📁 Localização dos Arquivos\n\n")
            f.write(f"**Pasta de Saída:** `{pasta_base / 'input'}`\n\n")
            f.write("Os arquivos processados estão disponíveis na pasta `input` desta base.\n")
            
    def _gerar_relatorio_completo(self, resultado: Dict, pasta_base: Path):
        """Gera relatório completo da base"""
        # Primeiro gera o relatório rápido
        self._gerar_relatorio_rapido(resultado, pasta_base)
        
        # Adiciona seções estatísticas
        relatorio_path = pasta_base / f"relatorio_completo_{resultado['base']}.md"
        
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write(f"# Relatório Completo - Base {resultado['base']}\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Modo:** Processamento Completo 📊\n")
            f.write(f"**Tempo Total:** {resultado['tempo_processamento'] + resultado.get('tempo_estatisticas', 0):.2f} segundos\n\n")
            
            # Seções do relatório rápido
            f.write("## 📊 Resumo Executivo\n\n")
            f.write(f"- **Arquivos Processados:** {resultado['arquivos_processados']}/{resultado['total_arquivos']}\n")
            f.write(f"- **Arquivos Válidos:** {resultado['arquivos_validos']}/{resultado['total_arquivos']}\n")
            f.write(f"- **Taxa de Sucesso:** {(resultado['arquivos_validos']/resultado['total_arquivos']*100):.1f}%\n")
            
            # Adiciona estatísticas se disponíveis
            if 'estatisticas' in resultado and resultado['estatisticas']:
                f.write("\n## 📈 Análise Estatística Detalhada\n\n")
                for arquivo, stats in resultado['estatisticas'].items():
                    f.write(f"### {arquivo}\n")
                    f.write(f"- **Registros:** {stats.get('total_registros', 'N/A')}\n")
                    f.write(f"- **Colunas:** {stats.get('total_colunas', 'N/A')}\n")
                    f.write(f"- **Campos Vazios:** {stats.get('campos_vazios', 'N/A')}\n")
                    f.write(f"- **Taxa de Preenchimento:** {stats.get('taxa_preenchimento', 'N/A')}%\n\n")
            
            if resultado.get('graficos_gerados'):
                f.write("## 📊 Visualizações Geradas\n\n")
                for grafico in resultado['graficos_gerados']:
                    f.write(f"- {grafico}\n")
                f.write("\n")
                
    def _analisar_estatisticas_arquivo(self, arquivo_path: Path) -> Dict:
        """Analisa estatísticas de um arquivo"""
        try:
            # Detecta encoding
            with open(arquivo_path, 'rb') as f:
                raw_data = f.read(1024)
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            df = pd.read_csv(arquivo_path, encoding=encoding)
            
            stats = {
                'total_registros': len(df),
                'total_colunas': len(df.columns),
                'campos_vazios': df.isnull().sum().sum(),
                'taxa_preenchimento': ((df.size - df.isnull().sum().sum()) / df.size * 100) if df.size > 0 else 0
            }
            
            return stats
            
        except Exception as e:
            return {'erro': str(e)}
            
    def _gerar_graficos_base(self, resultado: Dict, pasta_base: Path) -> List[str]:
        """Gera gráficos para a base"""
        graficos = []
        
        try:
            pasta_graficos = pasta_base / "graficos"
            pasta_graficos.mkdir(exist_ok=True)
            
            # Gráfico de arquivos válidos vs total
            plt.figure(figsize=(10, 6))
            categorias = ['Válidos', 'Com Problemas']
            valores = [resultado['arquivos_validos'], 
                      resultado['total_arquivos'] - resultado['arquivos_validos']]
            cores = ['#27ae60', '#e74c3c']
            
            plt.bar(categorias, valores, color=cores)
            plt.title(f'Status dos Arquivos - Base {resultado["base"]}')
            plt.ylabel('Quantidade de Arquivos')
            
            grafico_path = pasta_graficos / "status_arquivos.png"
            plt.savefig(grafico_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            graficos.append(f"Status dos Arquivos: {grafico_path}")
            
        except Exception as e:
            self.log_status(f"⚠️ Erro ao gerar gráficos: {e}")
            
        return graficos
        
    def _atualizar_resultado_tree(self, base: str, resultado: Dict):
        """Atualiza tree view com resultado do processamento"""
        # Encontra item da base
        for item in self.tree_bases.get_children():
            valores = self.tree_bases.item(item, 'values')
            if valores[0] == base:
                status = "✅ Pronto" if resultado['arquivos_validos'] == resultado['total_arquivos'] else "❌ Problemas"
                observacoes = f"{len(resultado['problemas'])} problemas" if resultado['problemas'] else "OK"
                
                self.tree_bases.item(item, values=(
                    base, 
                    status, 
                    f"{resultado['arquivos_validos']}/{resultado['total_arquivos']}", 
                    resultado['total_arquivos'],
                    observacoes
                ))
                break
                
    def _detectar_inconsistencias_nomenclatura(self):
        """Detecta inconsistências de nomenclatura entre bases"""
        self.inconsistencias_nomenclatura = {}
        
        # Coleta todos os campos encontrados por arquivo
        campos_por_arquivo = {}
        
        for base, resultado in self.resultados_validacao.items():
            pasta_input = self.pasta_padrao / "output" / base / "input"
            
            for arquivo_csv in self.campos_obrigatorios.keys():
                arquivo_path = pasta_input / arquivo_csv
                
                if arquivo_path.exists():
                    try:
                        # Detecta encoding
                        with open(arquivo_path, 'rb') as f:
                            raw_data = f.read(1024)
                            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
                        
                        df = pd.read_csv(arquivo_path, encoding=encoding, nrows=0)
                        
                        if arquivo_csv not in campos_por_arquivo:
                            campos_por_arquivo[arquivo_csv] = {}
                            
                        for coluna in df.columns:
                            if coluna not in campos_por_arquivo[arquivo_csv]:
                                campos_por_arquivo[arquivo_csv][coluna] = []
                            campos_por_arquivo[arquivo_csv][coluna].append(base)
                            
                    except Exception as e:
                        continue
        
        # Detecta inconsistências
        for arquivo_csv, campos_obrigatorios in self.campos_obrigatorios.items():
            if arquivo_csv in campos_por_arquivo:
                for campo_obrigatorio in campos_obrigatorios:
                    # Procura variações do campo obrigatório
                    variações_encontradas = []
                    
                    for campo_encontrado, bases in campos_por_arquivo[arquivo_csv].items():
                        if campo_encontrado != campo_obrigatorio and self._campos_similares(campo_obrigatorio, campo_encontrado):
                            variações_encontradas.append((campo_encontrado, bases))
                    
                    if variações_encontradas:
                        chave = f"{arquivo_csv}_{campo_obrigatorio}"
                        self.inconsistencias_nomenclatura[chave] = {
                            'arquivo': arquivo_csv,
                            'campo_obrigatorio': campo_obrigatorio,
                            'variacoes': variações_encontradas
                        }
        
        # Atualiza tree de inconsistências
        self._atualizar_tree_inconsistencias()
        
    def _atualizar_tree_inconsistencias(self):
        """Atualiza tree view de inconsistências"""
        # Limpa tree
        for item in self.tree_inconsistencias.get_children():
            self.tree_inconsistencias.delete(item)
        
        # Adiciona inconsistências
        for chave, inconsistencia in self.inconsistencias_nomenclatura.items():
            for variacao, bases in inconsistencia['variacoes']:
                tipo_problema = "Espaçamento" if inconsistencia['campo_obrigatorio'].replace(' ', '') == variacao.replace(' ', '') else "Acentuação/Caracteres"
                
                self.tree_inconsistencias.insert('', 'end', values=(
                    inconsistencia['arquivo'],
                    inconsistencia['campo_obrigatorio'],
                    variacao,
                    ', '.join(bases),
                    tipo_problema
                ))
                
    def _mostrar_resumo_processamento(self):
        """Mostra resumo final do processamento"""
        total_bases = len(self.resultados_validacao)
        bases_prontas = sum(1 for r in self.resultados_validacao.values() 
                           if r['arquivos_validos'] == r['total_arquivos'])
        
        inconsistencias = len(self.inconsistencias_nomenclatura)
        
        resumo = f"""Processamento Concluído!

📊 Resumo Geral:
• {total_bases} bases processadas
• {bases_prontas} bases prontas para parser
• {total_bases - bases_prontas} bases com problemas
• {inconsistencias} inconsistências de nomenclatura detectadas

📁 Resultados salvos em:
{self.pasta_padrao / 'output'}

🎯 Próximos Passos:
1. Gere as tabelas Excel na aba Relatórios
2. Revise inconsistências de nomenclatura
3. Solicite correções no MDRIVER para bases com problemas"""

        messagebox.showinfo("Processamento Concluído", resumo)
        
    def processar_base_especifica(self):
        """Processa uma base específica selecionada pelo usuário"""
        if not self.bases_detectadas:
            messagebox.showerror("Erro", "Nenhuma base detectada!")
            return
            
        # Dialog para seleção de base
        dialog = tk.Toplevel(self.root)
        dialog.title("Selecionar Base")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Selecione a base para processar:", font=('Arial', 12)).pack(pady=10)
        
        listbox = tk.Listbox(dialog, font=('Arial', 10))
        for base in self.bases_detectadas:
            listbox.insert(tk.END, base)
        listbox.pack(fill='both', expand=True, padx=20, pady=10)
        
        def processar_selecionada():
            seleção = listbox.curselection()
            if seleção:
                base_selecionada = self.bases_detectadas[seleção[0]]
                dialog.destroy()
                
                # Processa base selecionada
                thread = threading.Thread(target=self._processar_base_especifica_thread, args=(base_selecionada,))
                thread.daemon = True
                thread.start()
            else:
                messagebox.showwarning("Aviso", "Selecione uma base!")
        
        ttk.Button(dialog, text="Processar", command=processar_selecionada).pack(pady=10)
        
    def _processar_base_especifica_thread(self, base: str):
        """Thread para processar base específica"""
        try:
            self.log_status(f"🔄 Processando base específica: {base}")
            
            self.progress_var.set(0)
            self.progress_label.config(text=f"Processando {base}...")
            
            if self.modo_var.get() == "rapido":
                resultado = self._processar_base_rapido(base)
            else:
                resultado = self._processar_base_completo(base)
                
            self.resultados_validacao[base] = resultado
            self._atualizar_resultado_tree(base, resultado)
            
            self.progress_var.set(100)
            self.progress_label.config(text=f"✅ Base {base} processada!")
            
            self.log_status(f"✅ Base {base} processada com sucesso!")
            
            messagebox.showinfo("Sucesso", f"Base {base} processada com sucesso!\n\n"
                               f"Arquivos válidos: {resultado['arquivos_validos']}/{resultado['total_arquivos']}")
            
        except Exception as e:
            self.log_status(f"❌ Erro ao processar base {base}: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao processar base {base}:\n{e}")
            
    def gerar_tabela_campos_obrigatorios(self):
        """Gera tabela Excel com campos obrigatórios"""
        if not self.campos_obrigatorios:
            messagebox.showerror("Erro", "Template não analisado! Analise o template Excel primeiro.")
            return
            
        try:
            self.log_status("📋 Gerando tabela de campos obrigatórios...")
            
            # Prepara dados para tabela
            dados_tabela = []
            
            for arquivo_csv, campos in self.campos_obrigatorios.items():
                for campo in campos:
                    linha = {
                        'Arquivo': arquivo_csv,
                        'Campo': campo,
                        'Obrigatório': 'X'
                    }
                    
                    # Adiciona colunas para cada base processada
                    for base in self.bases_detectadas:
                        if base in self.resultados_validacao:
                            # Verifica se o campo existe na base
                            pasta_input = self.pasta_padrao / "output" / base / "input"
                            arquivo_path = pasta_input / arquivo_csv
                            
                            tem_campo = "❌"
                            if arquivo_path.exists():
                                try:
                                    with open(arquivo_path, 'rb') as f:
                                        raw_data = f.read(1024)
                                        encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
                                    
                                    df = pd.read_csv(arquivo_path, encoding=encoding, nrows=0)
                                    if campo in df.columns:
                                        tem_campo = "✅"
                                    else:
                                        # Verifica variações
                                        for coluna in df.columns:
                                            if self._campos_similares(campo, coluna):
                                                tem_campo = "⚠️"
                                                break
                                except:
                                    tem_campo = "❌"
                            
                            linha[f'Arquivos "{base}"'] = tem_campo
                        else:
                            linha[f'Arquivos "{base}"'] = "❌"
                    
                    dados_tabela.append(linha)
            
            # Cria DataFrame
            df_tabela = pd.DataFrame(dados_tabela)
            
            # Salva Excel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_path = self.pasta_padrao / f"tabela_campos_obrigatorios_{timestamp}.xlsx"
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df_tabela.to_excel(writer, sheet_name='Campos Obrigatórios', index=False)
                
                # Formata planilha
                worksheet = writer.sheets['Campos Obrigatórios']
                
                # Ajusta largura das colunas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            self.log_status(f"✅ Tabela de campos obrigatórios salva: {excel_path}")
            
            messagebox.showinfo("Sucesso", f"Tabela de campos obrigatórios gerada!\n\n"
                               f"Arquivo: {excel_path.name}\n"
                               f"Localização: {excel_path.parent}")
            
            # Pergunta se quer abrir o arquivo
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir a tabela Excel gerada?"):
                try:
                    if sys.platform == "win32":
                        os.startfile(excel_path)
                    elif sys.platform == "darwin":
                        subprocess.run(["open", excel_path])
                    else:
                        subprocess.run(["xdg-open", excel_path])
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao abrir arquivo:\n{e}")
            
        except Exception as e:
            self.log_status(f"❌ Erro ao gerar tabela de campos obrigatórios: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao gerar tabela:\n{e}")
            
    def gerar_tabela_inconsistencias(self):
        """Gera tabela Excel com inconsistências de nomenclatura"""
        if not self.inconsistencias_nomenclatura:
            messagebox.showwarning("Aviso", "Nenhuma inconsistência detectada ou processamento não realizado.")
            return
            
        try:
            self.log_status("⚠️ Gerando tabela de inconsistências...")
            
            # Prepara dados para tabela
            dados_tabela = []
            
            for chave, inconsistencia in self.inconsistencias_nomenclatura.items():
                for variacao, bases in inconsistencia['variacoes']:
                    tipo_problema = "Espaçamento" if inconsistencia['campo_obrigatorio'].replace(' ', '') == variacao.replace(' ', '') else "Acentuação/Caracteres"
                    
                    dados_tabela.append({
                        'Arquivo CSV': inconsistencia['arquivo'],
                        'Campo Obrigatório': inconsistencia['campo_obrigatorio'],
                        'Variação Encontrada': variacao,
                        'Bases Afetadas': ', '.join(bases),
                        'Tipo Problema': tipo_problema,
                        'Recomendação': f"Padronizar para: {inconsistencia['campo_obrigatorio']}"
                    })
            
            # Cria DataFrame
            df_inconsistencias = pd.DataFrame(dados_tabela)
            
            # Salva Excel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_path = self.pasta_padrao / f"tabela_inconsistencias_{timestamp}.xlsx"
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df_inconsistencias.to_excel(writer, sheet_name='Inconsistências Nomenclatura', index=False)
                
                # Formata planilha
                worksheet = writer.sheets['Inconsistências Nomenclatura']
                
                # Ajusta largura das colunas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            self.log_status(f"✅ Tabela de inconsistências salva: {excel_path}")
            
            messagebox.showinfo("Sucesso", f"Tabela de inconsistências gerada!\n\n"
                               f"Arquivo: {excel_path.name}\n"
                               f"Inconsistências encontradas: {len(dados_tabela)}\n"
                               f"Localização: {excel_path.parent}")
            
            # Pergunta se quer abrir o arquivo
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir a tabela Excel gerada?"):
                try:
                    if sys.platform == "win32":
                        os.startfile(excel_path)
                    elif sys.platform == "darwin":
                        subprocess.run(["open", excel_path])
                    else:
                        subprocess.run(["xdg-open", excel_path])
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao abrir arquivo:\n{e}")
            
        except Exception as e:
            self.log_status(f"❌ Erro ao gerar tabela de inconsistências: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao gerar tabela:\n{e}")
            
    def gerar_graficos_estatisticas(self):
        """Gera gráficos e estatísticas avançadas"""
        if not self.resultados_validacao:
            messagebox.showwarning("Aviso", "Nenhum processamento realizado ainda.")
            return
            
        try:
            self.log_status("📈 Gerando gráficos e estatísticas...")
            
            # Cria pasta de gráficos
            pasta_graficos = self.pasta_padrao / "graficos_gerais"
            pasta_graficos.mkdir(exist_ok=True)
            
            # Gráfico 1: Status das bases
            plt.figure(figsize=(12, 8))
            
            bases = list(self.resultados_validacao.keys())
            arquivos_validos = [r['arquivos_validos'] for r in self.resultados_validacao.values()]
            total_arquivos = [r['total_arquivos'] for r in self.resultados_validacao.values()]
            
            x = range(len(bases))
            width = 0.35
            
            plt.bar([i - width/2 for i in x], arquivos_validos, width, label='Arquivos Válidos', color='#27ae60')
            plt.bar([i + width/2 for i in x], total_arquivos, width, label='Total Arquivos', color='#3498db')
            
            plt.xlabel('Bases')
            plt.ylabel('Quantidade de Arquivos')
            plt.title('Status de Validação por Base')
            plt.xticks(x, bases, rotation=45)
            plt.legend()
            plt.tight_layout()
            
            grafico1_path = pasta_graficos / "status_bases.png"
            plt.savefig(grafico1_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            # Gráfico 2: Distribuição de problemas
            plt.figure(figsize=(10, 6))
            
            total_problemas = sum(len(r['problemas']) for r in self.resultados_validacao.values())
            bases_com_problemas = sum(1 for r in self.resultados_validacao.values() if r['problemas'])
            bases_sem_problemas = len(self.resultados_validacao) - bases_com_problemas
            
            labels = ['Bases sem Problemas', 'Bases com Problemas']
            sizes = [bases_sem_problemas, bases_com_problemas]
            colors = ['#27ae60', '#e74c3c']
            
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('Distribuição de Problemas nas Bases')
            plt.axis('equal')
            
            grafico2_path = pasta_graficos / "distribuicao_problemas.png"
            plt.savefig(grafico2_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.log_status(f"✅ Gráficos salvos em: {pasta_graficos}")
            
            messagebox.showinfo("Sucesso", f"Gráficos e estatísticas gerados!\n\n"
                               f"Localização: {pasta_graficos}\n"
                               f"Arquivos gerados:\n"
                               f"• status_bases.png\n"
                               f"• distribuicao_problemas.png")
            
            # Pergunta se quer abrir a pasta
            if messagebox.askyesno("Abrir Pasta", "Deseja abrir a pasta com os gráficos?"):
                self.abrir_pasta_graficos()
            
        except Exception as e:
            self.log_status(f"❌ Erro ao gerar gráficos: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao gerar gráficos:\n{e}")
            
    def abrir_pasta_resultados(self):
        """Abre pasta de resultados"""
        pasta_output = self.pasta_padrao / "output"
        pasta_output.mkdir(exist_ok=True)
        
        try:
            if sys.platform == "win32":
                os.startfile(pasta_output)
            elif sys.platform == "darwin":
                subprocess.run(["open", pasta_output])
            else:
                subprocess.run(["xdg-open", pasta_output])
                
            self.log_status(f"📁 Pasta de resultados aberta: {pasta_output}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta:\n{e}")
            
    def abrir_pasta_logs(self):
        """Abre pasta de logs"""
        pasta_logs = Path("logs")
        pasta_logs.mkdir(exist_ok=True)
        
        try:
            if sys.platform == "win32":
                os.startfile(pasta_logs)
            elif sys.platform == "darwin":
                subprocess.run(["open", pasta_logs])
            else:
                subprocess.run(["xdg-open", pasta_logs])
                
            self.log_status(f"📁 Pasta de logs aberta: {pasta_logs}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta:\n{e}")
            
    def abrir_pasta_graficos(self):
        """Abre pasta de gráficos"""
        pasta_graficos = self.pasta_padrao / "graficos_gerais"
        pasta_graficos.mkdir(exist_ok=True)
        
        try:
            if sys.platform == "win32":
                os.startfile(pasta_graficos)
            elif sys.platform == "darwin":
                subprocess.run(["open", pasta_graficos])
            else:
                subprocess.run(["xdg-open", pasta_graficos])
                
            self.log_status(f"📁 Pasta de gráficos aberta: {pasta_graficos}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta:\n{e}")
            
    def atualizar_logs(self):
        """Atualiza área de logs"""
        try:
            # Lê logs mais recentes
            log_dir = Path("logs")
            if log_dir.exists():
                log_files = list(log_dir.glob("validador_v8_*.log"))
                if log_files:
                    log_file = max(log_files, key=lambda x: x.stat().st_mtime)
                    
                    with open(log_file, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                        
                    self.logs_text.delete(1.0, tk.END)
                    self.logs_text.insert(1.0, conteudo)
                    self.logs_text.see(tk.END)
                    
                    self.log_status("🔄 Logs atualizados")
                else:
                    self.logs_text.delete(1.0, tk.END)
                    self.logs_text.insert(1.0, "Nenhum log encontrado.")
            else:
                self.logs_text.delete(1.0, tk.END)
                self.logs_text.insert(1.0, "Pasta de logs não encontrada.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar logs:\n{e}")
            
    def limpar_logs(self):
        """Limpa logs do sistema"""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todos os logs?"):
            try:
                self.logs_text.delete(1.0, tk.END)
                
                # Remove arquivos de log
                log_dir = Path("logs")
                if log_dir.exists():
                    for log_file in log_dir.glob("*.log"):
                        log_file.unlink()
                        
                self.log_status("🗑️ Logs limpos")
                messagebox.showinfo("Sucesso", "Logs limpos com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar logs:\n{e}")
                
    def exportar_logs(self):
        """Exporta logs para arquivo"""
        try:
            conteudo_logs = self.logs_text.get(1.0, tk.END)
            
            if not conteudo_logs.strip():
                messagebox.showwarning("Aviso", "Nenhum log para exportar.")
                return
                
            arquivo = filedialog.asksaveasfilename(
                title="Exportar Logs",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if arquivo:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo_logs)
                    
                self.log_status(f"💾 Logs exportados: {arquivo}")
                messagebox.showinfo("Sucesso", f"Logs exportados para:\n{arquivo}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar logs:\n{e}")
            
    def executar(self):
        """Executa o sistema"""
        try:
            self.log_status("🚀 Sistema de Validação v8.0 Otimizado iniciado")
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Erro fatal: {e}")
            messagebox.showerror("Erro Fatal", f"Erro fatal no sistema:\n{e}")

def main():
    """Função principal"""
    try:
        print("🚀 Iniciando Sistema de Validação de Dados Logísticos v8.0...")
        print("⚡ Versão Otimizada com Processamento Rápido/Completo")
        print("🎯 Interface com Guia Visual de Prioridades")
        print()
        
        app = ValidadorLogisticoOtimizado()
        app.executar()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar sistema: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()

