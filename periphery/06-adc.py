"""
# Detalhamento dos Endereços do ADC no AM335x

## Informações Gerais
O ADC do AM335x suporta até 8 canais de entrada (AIN0 a AIN7), permitindo leituras de sinais analógicos de 12 bits. Ele é configurado e gerenciado através de registradores mapeados na memória.

## Endereço Base do ADC
| Endereço Base  | 0x44E0D000 |
- Essa é a região de memória onde o subsistema ADC está localizado.

## Tabela de Endereços do ADC
| Offset   | Endereço Completo     | Função                                      | Valores Possíveis                     | Descrição                                                                                                                                                     |
|----------|-----------------------|---------------------------------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x00     | 0x44E0D000            | Revisão do ADC                              | Inteiros                              | Informações sobre a revisão do módulo.                                                                                                                       |
| 0x04     | 0x44E0D004            | Configuração do ADC                         | Bits de configuração                  | Controla o modo de operação do ADC.                                                                                                                          |
| 0x40     | 0x44E0D040            | Status de interrupção                       | Flags                                 | Indica o status das interrupções do ADC.                                                                                                                     |
| 0x44     | 0x44E0D044            | Limpar interrupções                         | Bits                                 | Limpa as interrupções pendentes.                                                                                                                             |
| 0x48     | 0x44E0D048            | Seleção de canal                            | Canal ativo (AIN0 a AIN7)             | Define qual canal está ativo para a próxima conversão.                                                                                                       |
| 0x50     | 0x44E0D050            | Configuração de step                        | Bits de step                          | Configuração dos passos de conversão.                                                                                                                        |
| 0x54     | 0x44E0D054            | Status do FIFO0                             | Dados FIFO                            | Mostra o estado do FIFO0 (FIFO primário).                                                                                                                    |
| 0x58     | 0x44E0D058            | Dados do FIFO0                              | Dados de conversão                    | Resultados da conversão A/D para leitura.                                                                                                                    |
| 0x5C     | 0x44E0D05C            | Status do FIFO1                             | Dados FIFO                            | Mostra o estado do FIFO1 (FIFO secundário).                                                                                                                  |
| 0x60     | 0x44E0D060            | Dados do FIFO1                              | Dados de conversão                    | Resultados da conversão A/D no FIFO secundário.                                                                                                              |
| 0x70     | 0x44E0D070            | Configuração de clock                       | Frequência do clock                   | Define a frequência do clock do ADC para conversão.                                                                                                          |
| 0x74     | 0x44E0D074            | Configuração de tensão de referência        | Níveis de tensão                      | Configura o nível de tensão de referência (VREFP e VREFN).                                                                                                   |

| Canal    | Pino Físico (Header) | Função GPIO Associada   | Descrição                                                                    |
|----------|-----------------------|-------------------------|-------------------------------------------------------------------------------|
| AIN0     | 9                    | GPIOC0                 | Entrada analógica 0, usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN1     | 11                   | GPIOC1                 | Entrada analógica 1, usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN2     | 13                   | GPIOC4                 | Entrada analógica 2, usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN3     | 33                   | GPIOB16                | Entrada analógica 3, usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN4     | 35                   | GPIOB15                | Entrada analógica 4, usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN5     | 37                   | GPIOB10                | Entrada analógica 5, usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN6     | 39                   | GPIOB0                 | Entrada analógica 6, usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN7     | 7                    | GPIOB1                 | Entrada analógica 7, usada para medições de sinais analógicos conectados ao pino correspondente.  |

## Observações Adicionais
1. **Tensão de Referência (VREF):**
   - As entradas analógicas aceitam tensões entre **0V** e **VREFP**. A tensão de referência negativa é geralmente conectada ao **GND (VREFN)**.
   - Certifique-se de que a tensão de entrada não exceda os níveis de referência configurados para evitar danos ao ADC.

2. **FIFO (First-In-First-Out):**
   - O ADC suporta dois buffers FIFO (FIFO0 e FIFO1) para armazenar os resultados das conversões, permitindo leituras eficientes.

3. **Configuração de Steps:**
   - O ADC suporta configurações detalhadas para cada passo de conversão, incluindo qual canal ler, a tensão de referência, e os modos de operação.

4. **Clock:**
   - A frequência do clock do ADC pode ser ajustada para balancear precisão e velocidade de conversão. Consulte o datasheet para frequências recomendadas.

## Requisitos
- **Privilégios:** Acessar diretamente esses endereços requer permissões de root ou acesso via drivers dedicados.
- **Referência:** Consulte o datasheet do AM335x para detalhes completos sobre os bits de cada registrador.

"""

from periphery import MMIO
import time
import os, sys
if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

# Base de endereço e offset do ADC
ADC_BASE_ADDR = 0x44E0D000  # Exemplo para AM335x
ADC_STEPENABLE_OFFSET = 0x54  # Offset do registrador STEPENABLE
ADC_FIFO0DATA_OFFSET = 0x100  # Offset do FIFO0DATA (resultado ADC)

# Mapear a memória do ADC (tamanho típico de 4KB)
mmio = MMIO(ADC_BASE_ADDR, 0x1000)

# Habilitar o ADC (ajustar conforme o datasheet)
mmio.write32(ADC_STEPENABLE_OFFSET, 0x1)  # Habilita o passo 1 do ADC

try:
   while(1):

 # Ler dados do FIFO0DATA
    adc_value = mmio.read32(ADC_FIFO0DATA_OFFSET) & 0xFFF  # Considerar apenas os 12 bits de dados
    voltage = (adc_value / 4096.0) * 3.0  # Converter para tensão (0 a 3V)
    print(f"ADC Value: {adc_value}, Voltage: {voltage:.3f} V")
    time.sleep(1)  # Taxa de leitura

finally:
   # Fechar o mapeamento de memória
   mmio.close()
