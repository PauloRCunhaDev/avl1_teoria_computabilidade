def fatorial(n):
    # Condição-base de parada
    if n == 0:
        return 1
    # Chamada recursiva
    return n * fatorial(n - 1)

def main():
    n = int(input("Digite um número inteiro não-negativo: "))

    if n < 0:
        print("Erro: entrada inválida (n deve ser >= 0).")
        return

    resultado = fatorial(n)
    print(f"Resultado: {n}! = {resultado}")

if __name__ == "__main__":
    main()
