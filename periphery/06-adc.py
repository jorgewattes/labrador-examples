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

## Função de Canais (AIN)
Os canais analógicos são referenciados como **AIN0** a **AIN7**. Cada canal pode ser configurado para medições independentes.

| Canal    | Pino GPIO Associado | Função                                     | Descrição                                                                    |
|----------|----------------------|--------------------------------------------|-------------------------------------------------------------------------------|
| AIN0     | GPIO32               | Entrada analógica 0                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN1     | GPIO33               | Entrada analógica 1                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN2     | GPIO34               | Entrada analógica 2                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN3     | GPIO35               | Entrada analógica 3                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN4     | GPIO36               | Entrada analógica 4                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN5     | GPIO37               | Entrada analógica 5                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN6     | GPIO38               | Entrada analógica 6                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |
| AIN7     | GPIO39               | Entrada analógica 7                        | Usada para medições de sinais analógicos conectados ao pino correspondente.  |

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

# Endereço base e tamanho da região do ADC
ADC_BASE = 0x44E0D000
ADC_SIZE = 0x1000

# Mapear a memória do ADC
adc_mmio = MMIO(ADC_BASE, ADC_SIZE)

# Configurar o ADC (habilitar e configurar tensão de referência)
adc_mmio.write32(0x04, 0x01)  # Configuração básica do ADC

# Selecionar canal AIN0
adc_mmio.write32(0x48, 0x00)  # Selecionar canal 0 (AIN0)

try:
   while(1):
      # Iniciar uma conversão e ler o valor
      adc_mmio.write32(0x50, 0x01)  # Configurar step para iniciar conversão
      adc_value = adc_mmio.read32(0x58)  # Ler o valor convertido do FIFO0

      # Imprimir o valor lido
      print("ADC Value (AIN0):", adc_value)
finally:
   # Fechar o mapeamento de memória
   adc_mmio.close()
