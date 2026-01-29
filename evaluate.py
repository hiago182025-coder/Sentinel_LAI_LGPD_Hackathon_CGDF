import os
import sys

# ==============================================================================
# ☢️ BLOCO NUCLEAR DE LIMPEZA DE TERMINAL (SÓ EXECUTA EM HACKATHONS/DEMOS)
# ==============================================================================
# 1. Configura a variável de ambiente antes de qualquer coisa
os.environ["PYTHONWARNINGS"] = "ignore"

# 2. Importa warnings e aniquila o método warn
import warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
warnings.showwarning = warn
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore")

# 3. Silencia logs internos do C++ (Tensorflow/Sklearn backend)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
# ==============================================================================

import time
import argparse
import pandas as pd

# Imports Scikit-Learn (Agora eles obedecerão o silêncio)
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

# Rich Interface
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn
from rich.theme import Theme
from rich.align import Align
from rich import box

# Locais
from src.model import AccessInfoClassifier
from src.reporter import generate_professional_excel

# --- TEMA VISUAL DO CGDF ---
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold white on red",   # Vermelho sólido com texto branco
    "success": "bold white on green", # Verde sólido com texto branco
    "header": "bold white on #003366",
    "label_danger": "bold red",
    "label_success": "bold green"
})
console = Console(theme=custom_theme)

def main():
    # Limpa tela para inicio triunfal
    os.system('cls' if os.name == 'nt' else 'clear')

    console.print(Panel.fit(
        Align.center("[bold white]Sentinel LAI/LGPD[/bold white]\n"
                     "[cyan]Desafio Participa DF - Edital 10/2025[/cyan]"),
        box=box.HEAVY, style="header", padding=1
    ))
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='data/raw/dataset_gigante_lai.csv')
    args = parser.parse_args()

    # --- PASSO 1: CARGA DE DADOS ---
    try:
        if not os.path.exists(args.input):
            console.print(f"[bold red]❌ Arquivo {args.input} não encontrado![/]\n[yellow]Execute: python generate_data.py[/]")
            return
        
        with console.status("[bold blue]Carregando base de dados...", spinner="dots"):
            time.sleep(0.5) 
            df = pd.read_csv(args.input)
            
            # Validação básica
            X = df.iloc[:, 0].astype(str)
            y = df.iloc[:, 1].astype(bool) if df.shape[1] > 1 else pd.Series([False]*len(df))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
    except Exception as e:
        console.print(f"[bold red]ERRO CRÍTICO NO IO:[/bold red] {e}")
        return

    console.print(f"✔ Dataset carregado: [bold]{len(df)} registros[/bold]. Auditoria em: [bold]{len(X_test)} pedidos[/bold].", style="dim")

    # --- PASSO 2: TREINAMENTO E PROCESSAMENTO ---
    clf = AccessInfoClassifier()
    
    # Barra de progresso unificada para treinamento
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40, complete_style="blue", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        # Simula etapa de calibração NLP
        task_nlp = progress.add_task("Calibrando Pipeline Híbrido (NLP)...", total=100)
        for _ in range(30):
            time.sleep(0.02)
            progress.update(task_nlp, advance=3.4)
            
        # Treinamento REAL (Ocorre instantaneamente após delay visual)
        clf.train(X_train, y_train) 
        progress.update(task_nlp, completed=100)

    console.print("✔ Modelo Operacional e Calibrado (RegEx + Logistic Regression).", style="dim")
    print("") # Pula linha

    # --- PASSO 3: INFERÊNCIA COM VISUAL DE SCANNER ---
    console.rule("[bold white]INICIANDO VARREDURA DE DADOS PESSOAIS (LGPD)[/bold white]")
    print("") 

    y_pred = []
    # Criação de chunks para efeito visual da barra
    chunks = [X_test[i:i+100] for i in range(0, len(X_test), 100)]
    full_preds = []

    for batch in track(chunks, description="[bold cyan]Auditando pedidos LAI...[/]", console=console):
        # Aqui o Scikit-Learn gera o aviso chato. Com o BLOCO NUCLEAR lá em cima, ele será silenciado.
        batch_pred = clf.predict(batch)
        full_preds.extend(batch_pred)
        # time.sleep(0.01) # Removido delay para ficar rapido, o aviso deve sumir
        
    y_pred = full_preds

    # --- PASSO 4: RELATÓRIO TÉCNICO ---
    # Calcular metricas
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    
    # TABELA DE KPIs
    print("")
    metrics_table = Table(title="📊 [bold]INDICADORES DE DESEMPENHO (KPIs)[/bold]", box=box.ROUNDED)
    metrics_table.add_column("Métrica", style="cyan", no_wrap=True)
    metrics_table.add_column("Resultado", style="bold white", justify="right")
    metrics_table.add_column("Avaliação Técnica", justify="center")
    
    def status_kpi(val):
        if val >= 0.99: return "[bold green]EXCELENTE[/]"
        if val >= 0.90: return "[bold yellow]SATISFATÓRIO[/]"
        return "[bold red]CRÍTICO[/]"

    metrics_table.add_row("Precisão (Precision)", f"{precision:.2%}", status_kpi(precision))
    metrics_table.add_row("Recall (Segurança)", f"{recall:.2%}", status_kpi(recall))
    metrics_table.add_row("F1-Score", f"{f1:.2%}", status_kpi(f1))

    # PREPARANDO TEXTOS
    label_map = {True: 'DADO PESSOAL', False: 'DADO PÚBLICO'}
    pred_labels = [label_map[x] for x in y_pred]
    
    # Dataframe para exportação (Texto Amigável)
    output_df = pd.DataFrame({'Texto_Analise': X_test, 'Status_Predito': pred_labels})

    # TABELA DE AMOSTRAS
    print("")
    samples_table = Table(title="🔍 [bold]AUDITORIA AMOSTRAL (TEMPO REAL)[/bold]", box=box.SIMPLE_HEAD, show_lines=True)
    samples_table.add_column("#", style="dim", width=4)
    samples_table.add_column("Conteúdo do Pedido (Snippet)", width=80)
    samples_table.add_column("Status LGPD", justify="center", width=20)

    # Pegar 5 exemplos variados (Risco e Seguro)
    sample_df = output_df.head(6) 
    
    i = 1
    for _, row in sample_df.iterrows():
        txt = row['Texto_Analise']
        label = row['Status_Predito']
        
        if label == "DADO PESSOAL":
            tag = f"[danger] {label} [/]" 
            # Destaque em amarelo se for muito longo
            snippet = f"[white]{txt[:75]}...[/]" 
        else:
            tag = f"[success] {label}  [/]" # Espaço extra p alinhar
            snippet = f"[dim]{txt[:75]}...[/]"
            
        samples_table.add_row(str(i), snippet, tag)
        i+=1

    console.print(metrics_table)
    console.print(samples_table)

    # --- PASSO 5: EXCEL LINDO ---
    print("")
    with console.status("[bold cyan]Compilando relatório Excel Profissional...", spinner="earth"):
        output_path = 'data/processed/Relatorio_Auditoria_ParticipaDF.xlsx'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        generate_professional_excel(output_df, output_path)
        time.sleep(1) # Só para mostrar o status

    console.print(Panel(
        f"✅ [bold]RELATÓRIO DE AUDITORIA DISPONÍVEL![/bold]\n\n"
        f"📂 Local: [underline yellow]{output_path}[/underline yellow]\n"
        f"📅 Data: {time.strftime('%d/%m/%Y %H:%M')}",
        border_style="green",
        expand=False
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🚫 Interrompido pelo usuário.")
