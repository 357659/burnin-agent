# Burn-in Agent

Sistema de Burn-in para testar e validar computadores.

O projeto executa testes de hardware, identifica a máquina, gera um resultado estruturado e apresenta o resultado através de uma interface web.

Neste momento o projeto é um MVP local.

A persistência atual é feita em JSON e a próxima evolução planejada é SQLite.

---

# 1. Visão geral

O sistema funciona seguindo este fluxo:

    Usuário
       |
       v
    Frontend
    Streamlit
       |
       v
    burnin.py
       |
       +----------------+
       |                |
       v                v
    CPU Test          RAM Test
       |                |
       +--------+-------+
                |
                v
          BurnInResult
                |
                v
         JsonRepository
                |
                v
             JSON

O ponto mais importante para entender o projeto é:

> O frontend não executa os testes diretamente.
> O frontend chama o agente.
> O agente executa os testes.
> Os testes retornam resultados.
> O agente junta os resultados em um BurnInResult.
> O repository salva o resultado.

---

# 2. Estrutura do projeto

A estrutura atual é:

    burnin-agent/
    |
    +-- agent/
    |   |
    |   +-- burnin.py
    |   |
    |   +-- system_info.py
    |   +-- system_result.py
    |   |
    |   +-- tests/
    |   |   |
    |   |   +-- cpu_test.py
    |   |   +-- ram_test.py
    |   |   +-- test_result.py
    |   |   +-- burnin_result.py
    |   |
    |   +-- storage/
    |       |
    |       +-- json_repository.py
    |
    +-- frontend/
    |   |
    |   +-- app.py
    |
    +-- data/
    |   |
    |   +-- burnin_runs/
    |
    +-- requirements.txt
    +-- run.bat
    +-- .gitignore
    +-- README.md

---

# 3. O que cada parte faz

## agent/

É o núcleo do sistema.

Não existe interface gráfica aqui.

O código dentro de `agent/` deve funcionar independentemente do Streamlit.

---

# 4. agent/burnin.py

Este é o orquestrador principal.

É o arquivo que coordena uma execução completa.

A função principal é:

    run_burnin()

Ela faz aproximadamente isto:

    1. Identifica a máquina
    2. Executa teste de CPU
    3. Executa teste de RAM
    4. Junta os resultados
    5. Calcula PASS/FAIL geral
    6. Cria BurnInResult
    7. Salva o resultado
    8. Retorna BurnInResult

Fluxo:

    run_burnin()
          |
          v
    get_system_info()
          |
          v
    run_cpu_test()
          |
          v
    run_ram_test()
          |
          v
    results = [cpu_result, ram_result]
          |
          v
    BurnInResult
          |
          v
    JsonRepository.save()
          |
          v
    arquivo JSON

Esse arquivo é o "maestro" do sistema.

Ele não deve conter a implementação detalhada dos testes.

Por exemplo:

ERRADO:

    burnin.py
        código de stress de CPU
        código de alocação de RAM
        código de leitura de MAC
        código de banco

CORRETO:

    burnin.py
        chama get_system_info()
        chama run_cpu_test()
        chama run_ram_test()
        monta resultado
        salva resultado

---

# 5. agent/system_info.py

Responsável pela identificação da máquina.

A função principal é:

    get_system_info()

Ela retorna um objeto `SystemInfo`.

Atualmente são coletadas informações como:

    machine_id
    mac_address
    hostname
    operating_system
    os_version
    cpu
    cpu_count
    ram_total_gb

Exemplo:

    machine_id       : 22-28-4D-03-73-55
    mac_address      : 22-28-4D-03-73-55
    hostname         : DESKTOP-PDDK6JH
    operating_system : Windows
    os_version       : 10.0.26200
    cpu              : AMD Ryzen 5 5500
    cpu_count        : 12
    ram_total_gb     : 15.89

---

# 6. agent/system_result.py

Define a estrutura dos dados da máquina.

Atualmente:

    @dataclass
    class SystemInfo:
        machine_id: str
        mac_address: str
        hostname: str
        operating_system: str
        os_version: str
        cpu: str
        cpu_count: int
        ram_total_gb: float

Esse arquivo é um modelo de dados.

Ele não deve executar testes.

---

# 7. agent/tests/

Esta pasta contém os testes individuais.

A ideia é:

    um arquivo = um teste

Atualmente:

    cpu_test.py
    ram_test.py

No futuro poderemos ter:

    ssd_test.py
    gpu_test.py
    network_test.py
    temperature_test.py

etc.

---

# 8. agent/tests/cpu_test.py

Executa o teste de CPU.

A função principal é:

    run_cpu_test()

Ela executa carga na CPU e coleta métricas.

O resultado não deve ser simplesmente:

    "PASS"

ou:

    True

O teste retorna um `TestResult`.

Exemplo:

    TestResult(
        test="CPU",
        status="PASS",
        errors=[],
        metrics={
            "cpu_average": 100.0,
            "cpu_max": 100.0,
            "ram_initial": 48.4,
            "ram_final": 48.4
        }
    )

---

# 9. agent/tests/ram_test.py

Executa o teste de memória RAM.

A função principal é:

    run_ram_test()

Ela aloca memória e acompanha o comportamento durante o teste.

Também retorna `TestResult`.

Exemplo:

    TestResult(
        test="RAM",
        status="PASS",
        errors=[],
        metrics={
            "ram_max": 58.6
        }
    )

---

# 10. agent/tests/test_result.py

Define o resultado de um teste individual.

Estrutura conceitual:

    TestResult
        |
        +-- test
        +-- status
        +-- errors
        +-- metrics

Exemplo:

    TestResult(
        test="CPU",
        status="PASS",
        errors=[],
        metrics={
            "cpu_average": 100.0
        }
    )

`status`:

    PASS
    FAIL

`errors`:

    lista de erros encontrados

`metrics`:

    dados coletados durante o teste

---

# 11. Por que usar TestResult?

Porque o sistema precisa crescer.

Hoje temos:

    CPU
    RAM

Amanhã:

    CPU
    RAM
    SSD
    GPU
    REDE

Se cada teste retornar uma coisa diferente, o sistema fica difícil de manter.

Todos devem seguir o mesmo contrato:

    TestResult

Assim o Burn-in Agent consegue tratar todos os testes da mesma maneira.

---

# 12. agent/tests/burnin_result.py

`BurnInResult` representa uma execução completa do Burn-in.

Ele contém:

    status
    system
    tests

Exemplo conceitual:

    BurnInResult(
        status="PASS",
        system=system_info,
        tests=[
            cpu_result,
            ram_result
        ]
    )

Portanto:

    TestResult
        = resultado de UM teste

    BurnInResult
        = resultado de UMA EXECUÇÃO completa

---

# 13. Diferença entre TestResult e BurnInResult

Essa diferença é importante.

Imagine uma máquina:

    Ryzen 5 5500
    16 GB RAM

Executamos:

    CPU -> PASS
    RAM -> PASS

Temos:

    TestResult CPU
    TestResult RAM

Depois juntamos:

    BurnInResult

Representação:

    BurnInResult
    |
    +-- system
    |     |
    |     +-- CPU
    |     +-- RAM
    |     +-- Machine ID
    |
    +-- tests
          |
          +-- CPU TestResult
          |
          +-- RAM TestResult

---

# 14. Como o PASS/FAIL é calculado

O agente recebe todos os resultados:

    results = [
        cpu_result,
        ram_result
    ]

Depois verifica se algum teste falhou.

Regra atual:

    Se qualquer teste = FAIL
        Burn-in = FAIL

    Se nenhum teste = FAIL
        Burn-in = PASS

Exemplo:

    CPU = PASS
    RAM = PASS

    Resultado geral = PASS


Outro exemplo:

    CPU = PASS
    RAM = FAIL

    Resultado geral = FAIL

---

# 15. agent/storage/

Esta pasta contém a persistência dos resultados.

Atualmente usamos:

    JsonRepository

A ideia de Repository é importante.

O restante do sistema não deveria precisar saber se estamos salvando em:

    JSON
    SQLite
    PostgreSQL
    API

O agente deveria apenas dizer:

    repository.save(result)

---

# 16. agent/storage/json_repository.py

É a implementação atual de persistência.

Ele salva cada execução em:

    data/burnin_runs/

Exemplo:

    2026-08-15_12-47-04_22-28-4D-03-73-55.json

O nome possui:

    data
    hora
    machine_id

Isso facilita identificar as execuções.

---

# 17. Histórico

O repository também possui:

    get_history(machine_id)

Exemplo:

    repository = JsonRepository()

    history = repository.get_history(
        "22-28-4D-03-73-55"
    )

O retorno é uma lista de `BurnInResult`.

Exemplo:

    EXECUÇÕES: 2

    PASS
    PASS

---

# 18. Por que Repository?

Porque a próxima evolução é SQLite.

Hoje:

    BurnInResult
         |
         v
    JsonRepository
         |
         v
       JSON

Futuramente:

    BurnInResult
         |
         v
    SQLiteRepository
         |
         v
       SQLite

O `burnin.py` não deveria precisar conhecer os detalhes do SQLite.

Essa separação é importante.

---

# 19. frontend/app.py

É a interface visual.

Utiliza Streamlit.

O frontend apresenta:

    Identificação da máquina

    CPU
    RAM
    quantidade de CPUs
    Machine ID

    Botão:
        INICIAR BURN-IN

    Resultado:

        CPU     PASS
        RAM     PASS
        GERAL   PASS

    Métricas

    Histórico

O frontend não deve implementar os testes.

---

# 20. Como o frontend executa o Burn-in

Quando o usuário clica:

    INICIAR BURN-IN

o frontend chama:

    run_burnin()

O fluxo é:

    Streamlit
       |
       v
    run_burnin()
       |
       +---- get_system_info()
       |
       +---- run_cpu_test()
       |
       +---- run_ram_test()
       |
       +---- BurnInResult
       |
       +---- save()
       |
       v
    resultado
       |
       v
    Streamlit apresenta

Portanto o frontend é apenas a camada de apresentação.

---

# 21. Execução pelo terminal

O agente pode ser executado sem o frontend:

    python -m agent.burnin

Isso é importante.

O sistema de testes não depende do Streamlit.

Ao executar:

    python -m agent.burnin

esperamos algo parecido com:

    BURN-IN AGENT

    ID da Máquina       : 22-28-4D-03-73-55
    Endereço MAC        : 22-28-4D-03-73-55
    CPU                 : AMD Ryzen 5 5500
    Quantidade de CPUs  : 12
    Memória RAM Total   : 15.89

    Iniciando teste de CPU...

    CPU : PASS

    Iniciando teste de RAM...

    RAM : PASS

    RESULTADO GERAL : PASS

E o resultado é salvo.

---

# 22. Execução do frontend

Para iniciar o dashboard:

    python -m streamlit run frontend/app.py

O navegador abrirá a interface do sistema.

O frontend chama o mesmo `run_burnin()` utilizado no terminal.

Isso significa que:

    Terminal
        |
        +----> run_burnin()


    Streamlit
        |
        +----> run_burnin()

Os dois utilizam o mesmo núcleo.

---

# 23. Ambiente virtual

O projeto pode ser desenvolvido utilizando `.venv`.

Porém, a execução do projeto não deve depender de uma ativação manual do ambiente virtual.

Exemplo:

    python -m agent.burnin

ou:

    python -m streamlit run frontend/app.py

O `run.bat` também pode ser utilizado para facilitar a execução.

---

# 24. Dependências

As dependências estão em:

    requirements.txt

Para instalar:

    python -m pip install -r requirements.txt

Se uma biblioteca nova for adicionada ao código, ela deve ser adicionada ao `requirements.txt`.

Não instalar dependências apenas na máquina e esquecer o arquivo.

---

# 25. Como executar um teste individual

CPU:

    python -c "from agent.tests.cpu_test import run_cpu_test; r=run_cpu_test(1); print(r)"

RAM:

    python -c "from agent.tests.ram_test import run_ram_test; r=run_ram_test(1); print(r)"

Informações da máquina:

    python -m agent.system_info

Burn-in completo:

    python -m agent.burnin

---

# 26. Como testar o histórico

Exemplo:

    python -c "from agent.storage.json_repository import JsonRepository; r=JsonRepository(); h=r.get_history('22-28-4D-03-73-55'); print('EXECUÇÕES:', len(h))"

Para acessar um resultado:

    h[0].status

CPU:

    h[0].system.cpu

Testes:

    [t.test for t in h[0].tests]

---

# 27. Fluxo completo de uma execução

Este é o fluxo que deve ser entendido antes de modificar o projeto.

## Etapa 1

O usuário inicia:

    python -m agent.burnin

ou clica no botão do frontend.

---

## Etapa 2

`burnin.py` chama:

    get_system_info()

Resultado:

    SystemInfo

---

## Etapa 3

Executa:

    run_cpu_test()

Resultado:

    TestResult("CPU")

---

## Etapa 4

Executa:

    run_ram_test()

Resultado:

    TestResult("RAM")

---

## Etapa 5

Os resultados são agrupados:

    [
        cpu_result,
        ram_result
    ]

---

## Etapa 6

O sistema calcula:

    PASS
    ou
    FAIL

---

## Etapa 7

É criado:

    BurnInResult

---

## Etapa 8

O resultado é salvo:

    JsonRepository.save()

---

## Etapa 9

O frontend apresenta o resultado.

---

# 28. Onde adicionar um novo teste

Suponha que queremos adicionar teste de SSD.

Criar:

    agent/tests/ssd_test.py

Com uma função:

    run_ssd_test()

Ela deve retornar:

    TestResult(
        test="SSD",
        status="PASS",
        errors=[],
        metrics={}
    )

Depois o `burnin.py` deverá incluir:

    ssd_result = run_ssd_test()

E adicionar:

    results = [
        cpu_result,
        ram_result,
        ssd_result
    ]

O resultado geral continuará funcionando porque o agente trabalha com uma lista de testes.

Depois o frontend deverá ser atualizado para apresentar o SSD.

---

# 29. Onde NÃO adicionar o novo teste

Não colocar o código do SSD em:

    frontend/app.py

Não colocar o código do SSD diretamente dentro de:

    burnin.py

O código do teste deve ficar em:

    agent/tests/ssd_test.py

O `burnin.py` apenas chama o teste.

---

# 30. Próxima evolução: SQLite

A próxima tarefa importante é substituir a persistência baseada somente em arquivos JSON por SQLite.

Arquitetura atual:

    BurnInResult
         |
         v
    JsonRepository
         |
         v
    arquivos JSON

Arquitetura desejada:

    BurnInResult
         |
         v
    Repository
         |
         v
    SQLite
         |
         v
    banco.db

---

# 31. Banco SQLite planejado

Uma possível estrutura inicial:

    machines

    id
    machine_id
    mac_address
    hostname
    operating_system
    os_version
    cpu
    cpu_count
    ram_total_gb


    executions

    id
    machine_id
    timestamp
    status


    tests

    id
    execution_id
    test
    status
    errors
    metrics

Relacionamento:

    machine
       |
       | 1:N
       v
    executions
       |
       | 1:N
       v
    tests

---

# 32. Importante sobre SQLite

Não alterar tudo de uma vez.

A evolução deve ser incremental.

Primeiro:

    criar SQLiteRepository

Depois:

    testar save()

Depois:

    testar get_history()

Depois:

    alterar o frontend para utilizar SQLite

Depois:

    decidir se o JSON continuará como backup/exportação.

O sistema atual deve continuar funcionando durante a migração.

---

# 33. Princípio de desenvolvimento

A regra principal deste projeto é:

    Separar responsabilidades.

Exemplo:

    system_info.py
        identifica a máquina

    cpu_test.py
        testa CPU

    ram_test.py
        testa RAM

    burnin.py
        coordena os testes

    test_result.py
        representa resultado de um teste

    burnin_result.py
        representa resultado completo

    repository
        salva/consulta dados

    frontend
        apresenta dados

Não misturar essas responsabilidades sem necessidade.

---

# 34. Antes de modificar qualquer arquivo

Primeiro entender onde a mudança pertence.

Pergunte:

    Isso é identificação da máquina?
        -> system_info.py

    Isso é um novo teste?
        -> agent/tests/

    Isso é coordenação?
        -> burnin.py

    Isso é estrutura de resultado?
        -> test_result.py
        -> burnin_result.py

    Isso é armazenamento?
        -> agent/storage/

    Isso é interface?
        -> frontend/

---

# 35. Procedimento para desenvolver

Antes:

    git pull

Depois:

    git status

Executar o projeto atual.

Fazer uma alteração pequena.

Testar.

Depois verificar:

    git diff --check

Depois:

    git status

Somente então fazer commit.

---

# 36. Regra de ouro

Não fazer uma alteração grande sem testar o fluxo completo.

Depois de qualquer alteração importante, executar:

    python -m agent.burnin

E verificar:

    CPU
    RAM
    PASS/FAIL
    Machine ID
    arquivo salvo

Se alterar o frontend:

    python -m streamlit run frontend/app.py

E verificar:

    identificação
    botão
    execução
    resultado
    histórico

---

# 37. Objetivo da próxima etapa

O objetivo imediato não é criar uma aplicação totalmente nova.

É evoluir o sistema existente.

Estado atual:

    [OK] Identificação
    [OK] CPU
    [OK] RAM
    [OK] Resultado
    [OK] JSON
    [OK] Histórico
    [OK] Frontend

Próximo:

    [ ] SQLite
    [ ] SQLiteRepository
    [ ] Histórico usando SQLite

Depois:

    [ ] novos testes
    [ ] API
    [ ] comunicação entre máquinas
    [ ] banco central
    [ ] dashboard de múltiplas máquinas

---

# 38. Visão futura

O objetivo final é transformar:

    uma máquina
        +
    execução local

em:

    várias máquinas
          |
          v
    Burn-in Agents
          |
          v
       API
          |
          v
    Banco central
          |
          v
      Dashboard

Com capacidade de acompanhar aproximadamente 40 máquinas.

Exemplo:

    MACHINE 001    PASS
    MACHINE 002    TESTANDO
    MACHINE 003    FAIL
    MACHINE 004    PASS
    MACHINE 005    PASS
    ...
    MACHINE 040    TESTANDO

Cada máquina continuará utilizando o mesmo conceito atual:

    identificar
        ↓
    testar
        ↓
    gerar resultado
        ↓
    registrar resultado

A diferença será que o resultado deixará de ficar apenas localmente e passará a ser enviado para uma estrutura central.

---

# 39. Resumo para quem está começando

Se você acabou de entrar no projeto, leia nesta ordem:

    1. README.md
    2. agent/system_result.py
    3. agent/system_info.py
    4. agent/tests/test_result.py
    5. agent/tests/cpu_test.py
    6. agent/tests/ram_test.py
    7. agent/tests/burnin_result.py
    8. agent/burnin.py
    9. agent/storage/json_repository.py
    10. frontend/app.py

Depois execute:

    python -m agent.system_info

Depois:

    python -m agent.burnin

Depois:

    python -m streamlit run frontend/app.py

Somente depois comece a modificar o código.

---

# 40. Estado de entrega

O projeto entregue neste momento é um:

    MVP LOCAL FUNCIONAL

Ele já consegue:

    identificar a máquina
    executar Burn-in
    testar CPU
    testar RAM
    gerar PASS/FAIL
    salvar resultados
    consultar histórico
    apresentar resultados no frontend

A próxima grande tarefa é:

    SQLITE

A partir daí o projeto começa a evoluir da execução local para uma arquitetura preparada para múltiplas máquinas.
