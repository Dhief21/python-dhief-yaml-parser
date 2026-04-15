# Python YAML Parser - Case 2
Ola pessoal, esta  e a solução proposta para o case 2, escolhi este case por ter mais familiriade com oque tinha ja visto e tambem por ter pouca dependecia de libs externas.

Abaixo vou listar alguns pontos que considero pertinentes para a solução proposta.

Foi criado um ambiente virtual pra isolar o projeto e garantir que ele execute em qualquer lugar instalando os pacotes do PyYAML para trabalharos com leitura do arquivo yaml e o pytest para os testes automatizados.

A estrutura abaixo em modulos separados e para facilitar manutencao: ex:  loader, resolver, validator, service e cli. 

## Estrutura
- `examples/input_case.yaml `: esse arquivo e o exemplo que foi sugerido no case e usamos como padrao
- `src/yaml_parser/loader.py`: aqui basicamente tem o codigo que faz leitura do YAML
- `src/yaml_parser/resolver.py`: aqui temos a detecção de ciclos de herença (recursividade), e faz merge profundo (herança de configurações) 
- `src/yaml_parser/validator.py`: validacoes de schema (constantes) com o yaml para detectar fora de padrao, demais validações..
- `src/yaml_parser/service.py`: pipeline principal, aqui ele que orquestra a ordem e execução do fluxo do programa
- `src/yaml_parser/cli.py`: interface de linha de comando mais amigavel para apresentar as validações e saidas.
- `tests/test_parser.py`: testes automatizados
- `src/yaml_parser/errors.py`: padroniza a saida dos erros que e mostrado na saida da cli mais amigavel pra leitura.


Com essa estrutura conseguimos dividir bem os papeis, criar um aculumador de erros em lote para permitir diagnostico completo em uma unica execucao, assim ele não para no primeiro erro e segue ate o final.

tambem temos validação da resolução de herança preservando valores herdados em objetos aninhados. Temos uma ordenação dos erros para melhorar previsibilidade em testes e execucao. Por fim uma CLI com codigo de saida 0 sem erros e 1 com erros

## O que este programa valida

- Heranca entre secoes com `_inherits`
- Merge profundo de objetos (ex.: `database`)
- Deteccao de ciclos de heranca
- Referencias de heranca inexistentes
- Tipos invalidos
- Valores fora de intervalo
- Chaves desconhecidas

## Formato de saida da CLI
- Resumo com total de ambientes resolvidos
- Total de erros encontrados
- Separacao entre erros de heranca/resolucao e erros de validacao
- Lista completa de erros (sem parar no primeiro)
- Configuracoes finais resolvidas em JSON

Codigo de saida esperado:

- `0`: execucao sem erros de validacao
- `1`: execucao com erros de validacao/heranca
- `2`: erro de uso (ex.: arquivo inexistente ou entrada invalida)

## Instalaçao 
Execute os comandos anaixo pra criar o ambiente virtual e instalar os pacotes necessarios.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execucao

Exemplo usando o arquivo oficial do case. Como esse arquivo contem erros intencionais, o processo termina com codigo de saida `1`, o que e esperado:

```bash
PYTHONPATH=src python3 -m yaml_parser.cli examples/input_case.yaml
```

## Testes

```bash
PYTHONPATH=src python3 -m pytest -q
```

# Considerações finais
Pessoal, foi um grante desafio e agradeço muito a oportunidade de participar deste processo seletivo.

Fazia muito tempo que não programava, e voltar trouxe uma otima sensação e boas lembranças.

tive algumas dificuldades que foram superadas, sendo honesto, tambem gostaria de compartilhar que usei auxilio de IA.

Espero que de certo, pode contar com minha dedicação e esforço para entrar de cabeça nessa area e contribuir com esse time o mais rapido possivel, crescer junto com voces e a Serasa.

Obrigado
Dhieferson Paixão
