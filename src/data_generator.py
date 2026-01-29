import pandas as pd
import random
from faker import Faker
from rich.console import Console
from rich.progress import track

# Configuração Visual
console = Console()

class LaiDataGenerator:
    def __init__(self, seed=42):
        self.fake = Faker('pt_BR')
        Faker.seed(seed)
        random.seed(seed)
        
        # --- CONTEXTOS DE PEDIDOS (SEM DADOS PESSOAIS - CLASSE 0) ---
        self.public_templates = [
            "Solicito cópia integral do contrato nº {num}/{ano} referente à licitação de limpeza urbana.",
            "Gostaria de saber o valor total gasto com publicidade institucional no ano de {ano}.",
            "Requeiro a lista de cargos em comissão ativos na Secretaria de Saúde em {mes}/{ano}.",
            "Qual o cronograma previsto para a reforma da escola classe {num} da Ceilândia?",
            "Solicito o inteiro teor do parecer jurídico sobre a inexigibilidade de licitação {num}.",
            "Gostaria de acessar as atas das reuniões do conselho de saúde realizadas em {ano}.",
            "Quantos leitos de UTI estão disponíveis atualmente no Hospital de Base?",
            "Peço planilha com a execução orçamentária do projeto Brasília Iluminada.",
            "Qual a quantidade de médicos pediatras efetivos na rede pública?",
            "Solicito dados estatísticos sobre acidentes de trânsito na EPTG no último semestre.",
            "Gostaria de saber os critérios para seleção dos beneficiários do programa social X.",
            "Cópia do edital de chamamento público nº {num} para credenciamento de clínicas.",
            "Há previsão para concurso público para o cargo de Auditor de Controle Interno?",
            "Gostaria do organograma atualizado da Secretaria de Obras.",
            "Solicito o valor do repasse federal recebido para merenda escolar este mês."
        ]

        # --- TEMPLATES DE INJEÇÃO DE DADOS PESSOAIS (COM RISCO - CLASSE 1) ---
        self.sensitive_templates = [
            # Auto-identificação excessiva (Risco Clássico)
            "Olá, meu nome é {nome}, portador do CPF {cpf}, gostaria de saber o andamento do meu processo.",
            "Eu, {nome}, RG {rg}, venho requerer minha ficha financeira de 2023.",
            "Minha mãe, {nome}, está aguardando cirurgia. O CPF dela é {cpf}. Qual a posição na fila?",
            "Solicito meu histórico funcional. Segue meus dados: {nome}, matrícula {num}, tel {celular}.",
            
            # Dados de Contato no corpo (Vazamento acidental)
            "Qualquer dúvida, liguem para o meu celular pessoal: {celular} ou fixo {fixo}.",
            "Por favor enviar a resposta exclusivamente para o email pessoal: {email}.",
            "Moro na {endereco} e quero denunciar um buraco na porta da minha casa.",
            
            # Denúncias nominadas (Risco a terceiros)
            "Quero denunciar o servidor {nome}, que bate o ponto e vai embora.",
            "Gostaria de saber o salário exato do meu vizinho {nome}, que trabalha aí.",
            
            # Mistura confusa
            "Segue em anexo meus documentos (CPF {cpf}) para provar que sou eu pedindo sobre a licitação {num}.",
            "Estou enviando meu RG {rg} e comprovante de residência na {endereco} para atualização cadastral."
        ]

    def generate(self, num_samples=500, ratio_sensitive=0.4):
        """
        Gera um DataFrame com n exemplos.
        ratio_sensitive: porcentagem de dados que terão risco (default 40%).
        """
        data = []
        labels = [] # False = Público, True = Sensível
        
        # Calcular quantidades
        n_sensitive = int(num_samples * ratio_sensitive)
        n_public = num_samples - n_sensitive
        
        console.print(f"[cyan]Gerando {n_public} pedidos públicos e {n_sensitive} com dados pessoais...[/cyan]")
        
        # 1. Gerar Pedidos Públicos (Seguros)
        for _ in track(range(n_public), description="Criando dados públicos..."):
            tpl = random.choice(self.public_templates)
            # Preencher com dados sintéticos genéricos (não pessoais)
            text = tpl.format(
                num=random.randint(10, 9999),
                ano=random.randint(2018, 2025),
                mes=self.fake.month_name(),
                orgao=self.fake.company()
            )
            data.append(text)
            labels.append(False)
            
        # 2. Gerar Pedidos Sensíveis (Com PII)
        for _ in track(range(n_sensitive), description="Criando dados sensíveis..."):
            tpl = random.choice(self.sensitive_templates)
            # Preencher com Fake PII (Personal Identifiable Information)
            text = tpl.format(
                nome=self.fake.name(),
                cpf=self.fake.cpf(),
                rg=self.fake.rg(),
                email=self.fake.free_email(),
                celular=self.fake.cellphone_number(),
                fixo=self.fake.phone_number(),
                endereco=self.fake.street_address(),
                num=random.randint(100, 99999)
            )
            data.append(text)
            labels.append(True)
            
        # Embaralhar o dataset
        df = pd.DataFrame({'texto_pedido': data, 'contem_dados_pessoais': labels})
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return df

if __name__ == "__main__":
    # Teste rápido se rodar o script direto
    gen = LaiDataGenerator()
    df_sample = gen.generate(10)
    print(df_sample)
