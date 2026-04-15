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
