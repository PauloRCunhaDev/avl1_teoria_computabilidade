# fatorial_iterativo.py
# Programa ITERATIVO — Cálculo do Fatorial
# Teoria da Computabilidade - AV1
#
# Estilo iterativo: uso explícito de estrutura de repetição (for).
# O estado é atualizado a cada iteração do laço.
#
# Função computada: f(n) = n! para n >= 0

def main():
    n = int(input("Digite um número inteiro não-negativo: "))

    if n < 0:
        print("Erro: entrada inválida (n deve ser >= 0).")
        return

    resultado = 1

    # Estrutura de repetição explícita
    for i in range(1, n + 1):
        resultado = resultado * i

    print(f"Resultado: {n}! = {resultado}")

if __name__ == "__main__":
    main()
