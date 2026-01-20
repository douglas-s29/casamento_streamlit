"""
Módulo para cálculos financeiros
"""


def calcular_total_orcado(items):
    """
    Calcula o total orçado somando os preços de todos os itens
    
    Args:
        items: Lista de dicionários com itens do casamento
        
    Returns:
        Total orçado (float)
    """
    return sum(item.get('preco', 0.0) for item in items)


def calcular_reserva(orcamento_maximo, total_orcado):
    """
    Calcula a reserva disponível
    
    Args:
        orcamento_maximo: Orçamento máximo total
        total_orcado: Total já orçado
        
    Returns:
        Reserva disponível (float)
    """
    return orcamento_maximo - total_orcado


def calcular_porcentagem_usada(orcamento_maximo, total_orcado):
    """
    Calcula a porcentagem do orçamento já utilizada
    
    Args:
        orcamento_maximo: Orçamento máximo total
        total_orcado: Total já orçado
        
    Returns:
        Porcentagem utilizada (float)
    """
    if orcamento_maximo == 0:
        return 0.0
    return (total_orcado / orcamento_maximo) * 100


def calcular_investimento_mensal(valor_inicial, valor_final_desejado, taxa_juros, numero_meses):
    """
    Calcula o valor de investimento mensal necessário
    
    Usa a fórmula de valor futuro com aportes mensais:
    VF = VP * (1 + i)^n + PMT * [((1 + i)^n - 1) / i]
    
    Onde:
    VF = Valor Final desejado
    VP = Valor Presente (inicial)
    PMT = Pagamento mensal (o que queremos calcular)
    i = taxa de juros mensal
    n = número de meses
    
    Resolvendo para PMT:
    PMT = (VF - VP * (1 + i)^n) * i / ((1 + i)^n - 1)
    
    Args:
        valor_inicial: Valor disponível inicialmente
        valor_final_desejado: Valor que se deseja atingir
        taxa_juros: Taxa de juros mensal (decimal, ex: 0.0035 para 0,35%)
        numero_meses: Número de meses para atingir o objetivo
        
    Returns:
        Valor de investimento mensal recomendado (float)
    """
    if numero_meses == 0 or taxa_juros == 0:
        # Caso sem juros ou sem tempo, apenas divide a diferença
        diferenca = valor_final_desejado - valor_inicial
        if numero_meses == 0:
            return 0.0
        return diferenca / numero_meses
    
    # Calcula o valor futuro do valor inicial
    fator_crescimento = (1 + taxa_juros) ** numero_meses
    valor_futuro_inicial = valor_inicial * fator_crescimento
    
    # Diferença que precisa ser coberta com aportes mensais
    diferenca = valor_final_desejado - valor_futuro_inicial
    
    # Se já temos mais do que o necessário, não precisa aportar
    if diferenca <= 0:
        return 0.0
    
    # Calcula o aporte mensal necessário
    pmt = diferenca * taxa_juros / (fator_crescimento - 1)
    
    return max(0.0, pmt)


def formatar_moeda(valor):
    """
    Formata um valor como moeda brasileira
    
    Args:
        valor: Valor numérico
        
    Returns:
        String formatada (ex: "R$ 1.234,56")
    """
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def calcular_porcentagem_tarefas(tasks):
    """
    Calcula a porcentagem de tarefas concluídas
    
    Args:
        tasks: Lista de dicionários com tarefas
        
    Returns:
        Porcentagem de conclusão (float)
    """
    if not tasks:
        return 0.0
    
    concluidas = sum(1 for task in tasks if task.get('concluida', False))
    return (concluidas / len(tasks)) * 100
