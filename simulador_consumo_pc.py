import os
import matplotlib.pyplot as plt # Importa a biblioteca para gráficos

# --- Constantes ---
PRECO_KWH = 0.80  # Preço do kWh em R$/kWh. Definido como constante em maiúsculas.

# --- Funções de Validação e Entrada ---
def get_int_input(prompt, min_val, max_val):
    """
    Solicita um número inteiro ao usuário, valida se está dentro de um intervalo
    específico e repete a solicitação até que uma entrada válida seja fornecida.

    Args:
        prompt (str): A mensagem a ser exibida para o usuário.
        min_val (int): O valor mínimo permitido para a entrada.
        max_val (int): O valor máximo permitido para a entrada.

    Returns:
        int: O valor inteiro válido inserido pelo usuário.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Ops! O valor precisa estar entre {min_val} e {max_val}. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite apenas números inteiros.")

def get_validated_string_input(prompt, validator_func, error_message):
    """
    Solicita uma string ao usuário e a valida usando uma função de validação fornecida,
    repetindo a solicitação até que uma entrada válida seja fornecida.

    Args:
        prompt (str): A mensagem a ser exibida para o usuário.
        validator_func (callable): Uma função que recebe a entrada do usuário e retorna True se válida, False caso contrário.
        error_message (str): A mensagem de erro a ser exibida se a validação falhar.

    Returns:
        str: O valor string válido inserido pelo usuário.
    """
    while True:
        value = input(prompt)
        if validator_func(value):
            return value
        else:
            print(error_message)

def valida_nome_computador(nome):
    """
    Valida o comprimento do nome do computador.
    Retorna True se o nome for válido, False caso contrário.
    """
    return 3 <= len(nome) <= 20

# --- Funções de Cálculo ---
def calcular_consumo_mensal(potencia, horas_por_dia, dias_por_mes, preco_kwh):
    """
    Calcula o consumo mensal de energia em kWh e o custo mensal em Reais.

    Args:
        potencia (int): A potência do computador em Watts.
        horas_por_dia (int): O número de horas por dia que o computador fica ligado.
        dias_por_mes (int): O número de dias por mês que o computador fica ligado.
        preco_kwh (float): O preço do quilowatt-hora (kWh).

    Returns:
        tuple: Uma tupla contendo (consumo_mensal_kwh, custo_mensal).
    """
    consumo_mensal_kwh = (potencia * horas_por_dia * dias_por_mes) / 1000
    custo_mensal = consumo_mensal_kwh * preco_kwh
    return consumo_mensal_kwh, custo_mensal

# --- Funções Utilitárias ---
def limpa_tela():
    """Limpa a tela do console."""
    comando = 'cls' if os.name == 'nt' else 'clear'
    os.system(comando)

def exibir_resultados_individuais(computadores):
    """Exibe os detalhes do consumo de energia para cada computador inserido."""
    limpa_tela()
    print("--- Detalhes Individuais dos Computadores ---\n")
    if not computadores:
        print("Nenhum computador foi adicionado ainda.")
        return

    for comp in computadores:
        print(f"Nome do Computador: {comp['nome']}")
        print(f"Potência configurada: {comp['potencia']} W")
        print(f"Consumo mensal estimado: {comp['consumo_kwh']:.2f} kWh")
        print(f"Custo mensal estimado: R${comp['custo']:.2f}\n")
    input("\nPressione Enter para continuar e ver a comparação...") # Pausa para o usuário ler

def exibir_comparacao_tabela(computadores):
    """Exibe uma comparação de consumo e custo entre os computadores inseridos em formato de tabela."""
    limpa_tela()
    print("--- Comparativo de Consumo de Energia (Tabela) ---\n")

    if not computadores:
        print("Nenhum computador para comparar.")
        return

    # Cabeçalho da tabela
    print(f"{'Nome':<20} {'Potência (W)':<15} {'Consumo (kWh)':<15} {'Custo (R$)':<15}")
    print("-" * 65)

    # Dados de cada computador
    for comp in computadores:
        print(f"{comp['nome']:<20} {comp['potencia']:<15} {comp['consumo_kwh']:.2f}{'':<13} {comp['custo']:.2f}{'':<13}")
    print("-" * 65)

    # Encontrar o mais e menos eficiente
    if len(computadores) > 1:
        mais_economico = min(computadores, key=lambda x: x['custo'])
        menos_economico = max(computadores, key=lambda x: x['custo'])
        print(f"\nO computador mais econômico é: {mais_economico['nome']} (R${mais_economico['custo']:.2f}/mês)")
        print(f"O computador menos econômico é: {menos_economico['nome']} (R${menos_economico['custo']:.2f}/mês)")
    input("\nPressione Enter para continuar e ver o gráfico...") # Pausa para o usuário ler

def gerar_grafico_comparacao(computadores):
    """
    Gera um gráfico de barras comparando o custo mensal de cada computador.
    """
    if not computadores:
        print("\nNão há dados de computadores para gerar o gráfico.")
        return

    nomes = [comp['nome'] for comp in computadores]
    custos = [comp['custo'] for comp in computadores]

    limpa_tela() # Limpa a tela antes de mostrar o gráfico

    plt.figure(figsize=(10, 6)) # Define o tamanho da figura (largura, altura)
    plt.bar(nomes, custos, color='skyblue') # Cria o gráfico de barras
    plt.xlabel('Nome do Computador') # Rótulo do eixo X
    plt.ylabel('Custo Mensal (R$)') # Rótulo do eixo Y
    plt.title('Comparativo de Custo Mensal de Energia por Computador') # Título do gráfico
    plt.xticks(rotation=45, ha='right') # Rotaciona os rótulos do eixo X para melhor visualização
    plt.grid(axis='y', linestyle='--', alpha=0.7) # Adiciona um grid no eixo Y
    plt.tight_layout() # Ajusta o layout para evitar sobreposição de rótulos
    plt.show() # Mostra o gráfico

# --- Execução Principal ---
if __name__ == "__main__":
    limpa_tela()
    print("| CALCULADORA DE CONSUMO DE ENERGIA DO COMPUTADOR |\n")

    computadores_registrados = [] # Lista para armazenar os dados de cada computador

    while True:
        print(f"\n--- Adicionando Computador #{len(computadores_registrados) + 1} ---")

        # Coleta e valida o nome do computador
        nome_computador = get_validated_string_input(
            "Qual nome você gostaria de dar para este computador? \n",
            valida_nome_computador,
            "Poxa! O nome do computador deve ter entre 3 e 20 caracteres."
        )

        # Coleta e valida os dados de consumo
        potencia = get_int_input(
            "Qual é a potência do computador em WATTS (ex: 300, 500, 750)?\n", 1, 1000
        )
        horas_por_dia = get_int_input(
            "Quantas horas por dia o computador fica ligado (1 a 24 horas)?\n", 1, 24
        )
        dias_por_mes = get_int_input(
            "Quantos dias por mês o computador fica ligado (1 a 30 dias)?\n", 1, 30
        )

        # Realiza o cálculo do consumo e custo
        try:
            consumo_kwh, custo = calcular_consumo_mensal(
                potencia, horas_por_dia, dias_por_mes, PRECO_KWH
            )

            # Armazena as informações em um dicionário
            info_computador = {
                "nome": nome_computador,
                "potencia": potencia,
                "horas_por_dia": horas_por_dia,
                "dias_por_mes": dias_por_mes,
                "consumo_kwh": consumo_kwh,
                "custo": custo
            }
            computadores_registrados.append(info_computador)

            while True:
                continuar = input("\nDeseja adicionar outro computador? (s/n): ").lower()
                if continuar in ['s', 'n']:
                    break
                else:
                    print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")
            if continuar == 'n':
                break

        except Exception as e:
            print(f"\nOcorreu um erro inesperado ao calcular: {e}")
            break # Sai do loop em caso de erro grave

    # Exibe os resultados individuais, depois a comparação em tabela e, por fim, o gráfico
    if computadores_registrados:
        exibir_resultados_individuais(computadores_registrados)
        exibir_comparacao_tabela(computadores_registrados)
        gerar_grafico_comparacao(computadores_registrados)
    else:
        print("\nNenhum computador foi configurado. Encerrando o programa.")