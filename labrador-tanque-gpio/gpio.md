# Usando o GPIO para controlar o tanque

Como citado na [página](../roverreadme/mf.html) sobre a montagem foi utilizada uma ponte H L298 para controlar a rotação do motor. Alimentando as portas de controle da ponte H com a combinação correta fará com que o motor rotacione em determinada direção, freie ou fique em ponto morto. O L298 aind possui portas que controlam se o motor está habilitado ou não, essas portas podem ser utilizadas para aumentar ou diminuir a velocidade de rotação das esteiras por meio de um pwm.

## Controle digital simples

Um controle digital para o carrinho, ou seja, contendo apenas comandos para ir para frente/trás e rodar no lugar para a direita/esquerda. Nessa primeira abordagem não haverá controle de velocidade e o tanque terá de fazer paradas para mudar de direção.

## Programação GPIO

Informações relevantes para a programação GPIO podem ser encontradas [aqui](https://wiki.caninosloucos.org.br/index.php/Programa%C3%A7%C3%A3o_GPIO). Essas informações serão utilizadas para criar um Software de controle simples.

## Programa em C

### Configurando GPIO
A primeira grande tarefa do algoritmo de controle é configurar o GPIO indicando as portas que serão usadas e se serão usadas como input ou como output.

A seguir um exemplo de inicialização possível:


``` c
#include <wiringPi.h>

#define P1 5 
#define P2 3
#define P3 15
#define P4 13

void initBoard () {
  	wiringPiSetupPhys () ;

	//define os pinos de controle do motor esquerdo como output
	pinMode (P1, OUTPUT);
	pinMode (P2, OUTPUT);

	//define os pinos de controle do motor direito como output
	pinMode (P3, OUTPUT);
	pinMode (P4, OUTPUT);

}
```

Observe que o número das portas utilizadas foram definidas como constantes no começo do código, esse tipo de prática facilita no caso de eventuais mudanças.Para saber a localização das portas na Labrador olhe na [documentação](https://wiki.caninosloucos.org.br/index.php/Programa%C3%A7%C3%A3o_GPIO)

### Atribuindo valores

Com os outputs definidos podemos escrever funções que atribuem valores nos pinos de saída para que o tanque faça algum movimento específico.

Para escrever no pinos de saída utilizamos a função digitalWrite (valor digital):

    digitalWrite(PINO, VALOR);

O "PINO" corresponde ao endereço do pino no qual se deseja escrever o valor e o "VALOR" corresponde ao valor a ser atribuído que, no caso de sinal digital, pode ser HIGH ou LOW.

A seguir estão as funções básicas para a movimentação do tanque:

``` c
void goForward() {
	printStatus("Going Forward");
	digitalWrite (P1, HIGH);
	digitalWrite (P2, LOW);
	digitalWrite (P3, HIGH);
	digitalWrite (P4, LOW);
}

void goBackward() {
	printStatus("Going Backward");
	digitalWrite (P1, LOW);
	digitalWrite (P2, HIGH);
	digitalWrite (P3, LOW);
	digitalWrite (P4, HIGH);
}

void goLeft() {
	printStatus("Turning Left");
	digitalWrite (P1, LOW);
	digitalWrite (P2, HIGH);
	digitalWrite (P3, HIGH);
	digitalWrite (P4, LOW);
}

void goRight() {
	printStatus("Turning Right");
	digitalWrite (P1, HIGH);
	digitalWrite (P2, LOW);
	digitalWrite (P3, LOW);
	digitalWrite (P4, HIGH);
}

void stopRover() {
	printStatus("Stopped");
	digitalWrite (P1, HIGH);
	digitalWrite (P2, HIGH);
	digitalWrite (P3, HIGH);
	digitalWrite (P4, HIGH);

}
```

### Input de dados e função principal (main)

Existem algumas funções que permitem leitura de dados do teclado. Aqui será feita uma sugestão utilizando a biblioteca 'ncurses' que basicamente oferece ferramentas para desenvolver interfaces no modo texto e permite a leitura de teclas especiais como, por exemplo, as setas de direção sem muita dificuldade.

A seguir encontra-se um possível código: 

``` c
#include <ncurses.h>
#include <string.h>

void initEnvironment() {
	//inicia UI 
	initscr();
	cbreak();
	noecho();
	keypad(stdscr,TRUE);
}

int main (void)
{
	//Temporary variable for saving kbrd input
	int c;

	initBoard();
	initEnvironment();

    //Desenha a interface do programa
	drawWelcomeScreen();
	//Manda comando de parar 
	stopRover();
  
    //Verifica tecla pressionada
	while('q' != (c=getch())) {
		switch (c)
		{
			case KEY_LEFT:
				goLeft();
				break;
			case KEY_RIGHT:
				goRight();
				break;
			case KEY_UP:
				goForward();
				break;
			case KEY_DOWN:
				goBackward();
				break;
			case 'a':
				goLeft();
				break;
			case 'd':
				goRight();
				break;
			case 'w':
				goForward();
				break;
			case 's':
				goBackward();
				break;
		}
        //mantém comando ativo e dentro do laço até que a tecla seja solta
	 	if (halfdelay(5) != ERR) {
			while(getch() == c)
				if(halfdelay(1) ==ERR) break; }
        //após sair do laço, envia comando de parada
		stopRover();
		cbreak(); }
		endwin();
	return 0;
}
```

### Interface de usuário

Como falado anteriormente foi utilizada a biblioteca *nCurses* para permitir a captura das teclas direcionais. Essa biblioteca também facilita o desenvolvimento de interfaces no modo texto.

A seguir estão algumas das funções escritas com o objetivo de criar uma interface básica com instruções para o usuário:

``` c

void printLineCentered(int lineNumber, char msg[]) {
	int remaining;
	remaining = strlen(msg);
	if (remaining>COLS) {
		mvaddstr(lineNumber, 0, msg);
	} else {
		remaining = COLS - remaining;
		remaining = remaining/2;
		mvaddstr(lineNumber, remaining, msg);
	}
}

void printBreak(int lineNumber, char separator) {
	int x;
	for (x=0;x<COLS;x++) {
		mvaddch(lineNumber,x,separator);
	}
}

void drawWelcomeScreen () {
	printBreak(0,'-');
	printBreak(1,'-');
	printBreak(2,'-');
	printLineCentered(1," ROVER CONTROL ");
	mvaddstr(5, TAB, "Use the directional Keys (or the keys a,s,d,w) to control the Rover");
	mvaddstr(6, TAB, "Press q to quit");
	printBreak(8,'-');
	printBreak(9,'-');
	printBreak(10,'-');
	printLineCentered(9," CURRENT STATUS ");
	
}

void printStatus(char c[]) {
	printBreak(STATUS_LINE,' ');
	mvaddstr(STATUS_LINE, TAB, c);
}

void goForward() {
	printStatus("Going Forward");
	digitalWrite (P1, HIGH);
	digitalWrite (P2, LOW);
	digitalWrite (P3, HIGH);
	digitalWrite (P4, LOW);
}
```

### Compilando e testando
Para compilar basta utilizar o seguinte comando:

    gcc NOME_ARQUIVO.c -o NOME_OUTPUT -I/usr/local/include -L/usr/local/lib -lwiringPi -lncurses

Para executar basta digitar:

    sudo ./NOME_OUTPUT

É essencial, nesse caso, utilizar o administrador para executar o comando (sudo) pois a função wiringPiSetupPhys exige esse tipo de privilégio.








