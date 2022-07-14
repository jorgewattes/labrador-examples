# Montagem Física

A montagem do tanque é feita de maneira muito simples. O desenvolvedor possui liberdade para alterar o projeto de acordo com suas preferências.

Para montar o Tanque Foram usadas as seguintes partes componentes:

- Chassi OSEPP Tank Kit
- Labrador
- Ponte H L298
- Pilhas (6), cabos e conectores

## Chassi

O Chassi utilizado já vem pronto para uso com motores e suporte de pilha instalados facilitando a montagem do Tanque. Outra vantagem do chassi utilizado é que ele possui inúmeros furos nos quais é possível fixar as placas de controle adicionais por meio de espaçadores.

![Chassi](/imagens/chassi.png)

## Labrador

A Labrador é basicamente a central de comando do Tanque. Ela foi fixada utilizando espaçadores M3 presos ao chassi. Foram feitas as seguintes conexões à placa:
1. Alimentação: Ligada diretamente à saída do conjunto de pilhas
2. Sinais de controle: É possível escolher pinos arbitrários de GPIO que são ligados às entradas de controle da ponte H
3. Sinal 5V: O pino de 5 volts é ligado à ponte H na porta de referência.

## Ponte H

A ponte H possui conexão a todos os elementos do sistema:

- Motores: Os motores são conectados um de cada lado da ponte H
- Alimentação
- Referência de tensão: Obtida da placa de controle (Labrador)
- Sinais de controle: responsáveis por controlar o estado do motor e, eventualmente, sua velocidade de rotação

![Ponte H](/imagens/ponth.jpg)

## Alimentação

O chassi utilizado acompanha um suporte para pilhas AA, entretanto pode ser interessante substituí-las por baterias recarregáveis.