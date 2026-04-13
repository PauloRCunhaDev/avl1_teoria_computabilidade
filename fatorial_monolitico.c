#include <stdio.h>

int main() {
    int n;
    long long resultado;
    int contador;

    printf("Programa Monolitico - Fatorial\n");
    printf("Digite um numero inteiro nao-negativo: ");
    scanf("%d", &n);

    /* Inicializacao */
    resultado = 1;
    contador  = n;

    /* Teste inicial: n < 0 => indefinido */
    if (n < 0) goto ERRO;

    /* Teste: n == 0 ou n == 1 => resultado = 1 */
    if (contador == 0) goto FIM;

LOOP_INICIO:
    /* Teste de parada: contador == 0? */
    if (contador == 0) goto FIM;

    /* Operacao: resultado = resultado * contador */
    resultado = resultado * contador;

    /* Operacao: contador = contador - 1 */
    contador = contador - 1;

    /* Desvio incondicional de volta ao inicio do laco */
    goto LOOP_INICIO;

ERRO:
    printf("Erro: entrada invalida (n deve ser >= 0)\n");
    goto ENCERRAR;

FIM:
    printf("Resultado: %d! = %lld\n", n, resultado);

ENCERRAR:
    return 0;
}
