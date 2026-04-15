# avl1_teoria_computabilidade

Projeto com implementações da função fatorial em Python e C.

### Equipe:
- João Pedro Follmann
- Yuri Fernandes
- Paulo Ricardo da Rocha

## Arquivos e objetivo

- `fatorial_iterativo.py`: calcula fatorial com repetição (loop).
- `fatorial_recursivo.py`: calcula fatorial com chamadas recursivas.
- `maquina_tracos_fatorial.py`: representa o cálculo com uma lógica de máquina de traços.
- `fatorial_monolitico.c`: versão em C com implementação direta em um único fluxo.

Todos os programas resolvem o mesmo problema: receber um valor inteiro não negativo `n` e retornar `n!`.

## Requisitos minimos

- Python 3 instalado.
- Compilador C (ex.: GCC/MinGW) para executar o arquivo em C.

## Execucao (PowerShell)

1. Entre na pasta do projeto:

```powershell
cd .\avl1_teoria_computabilidade
```

2. Execute os programas Python:

```powershell
python .\fatorial_iterativo.py
python .\fatorial_recursivo.py
python .\maquina_tracos_fatorial.py
```

3. Compile e execute o programa em C:

```powershell
gcc .\fatorial_monolitico.c -o .\fatorial_monolitico.exe
.\fatorial_monolitico.exe
```

## Comportamento esperado

- Entrada: um numero inteiro `n`.
- Restricao: `n >= 0`.
- Saida: valor de `n!`.

Exemplos:

- `0! = 1`
- `3! = 6`
- `5! = 120`

## Função implementada

Todos os programas calculam a função fatorial definida por:

$$
f(n) = n! =
\begin{cases}
1, & \text{se } n = 0 \\
n \cdot (n-1)!, & \text{se } n > 0
\end{cases}
$$

Forma expandida (para `n > 0`):

$$
n! = n \cdot (n-1) \cdot (n-2) \cdot \dots \cdot 2 \cdot 1
$$

## Observações

- O código do programa monolítico na linguagem C e o código da máquina fatorial foram feitos com a ajuda de inteligência artificial. No caso do programa monolítico, pedimos para a IA Claude "converter" o código original monolítico em Python para C e então avaliamos a sua execução e estrututa. Para a máquina de traços, juntamos todos os programas e pedimos para a IA GPT 5.4 realizar o processo da máquina de traços em cada um dos programas, criando assim um código único que executa a máquina de traços para cada programa e faz as devidas comparações no final.
