import re

class PatternRules:
    """
    Classe responsável pela definição de regras heurísticas e expressões regulares
    para identificação de dados pessoais comuns no contexto brasileiro.
    """
    
    def __init__(self):
        # Padrões compilados para performance
        
        # CPF: Com ou sem pontuação. Formatos 000.000.000-00 ou 00000000000
        self.cpf_pattern = re.compile(r'(?:\d{3}\.?\d{3}\.?\d{3}-?\d{2})')
        
        # E-mail: Padrão robusto para identificação de e-mails
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        
        # Telefones BR: Celulares e Fixos, com ou sem DDD, com ou sem máscara
        self.phone_pattern = re.compile(r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[ -]?\d{4}')
        
        # RG: Padrões comuns. Obs: RG é difícil via regex puro devido à variação estadual.
        # Captura formatos como 1.234.567-X
        self.rg_pattern = re.compile(r'(?:\d{1,2}\.?\d{3}\.?\d{3}-?[\d|X|x]{1})')

    def check_sensitive_patterns(self, text):
        """
        Retorna dicionário com contagens de matches e booleanos.
        Focada em EXPLICABILIDADE: O avaliador saberá por que caiu na regra.
        """
        if not isinstance(text, str):
            return {}

        metrics = {
            'match_cpf': len(self.cpf_pattern.findall(text)),
            'match_email': len(self.email_pattern.findall(text)),
            'match_phone': len(self.phone_pattern.findall(text)),
            'match_rg': len(self.rg_pattern.findall(text))
        }
        
        # Flag global se alguma regra forte for ativada
        metrics['rule_hit_total'] = sum(metrics.values())
        return metrics