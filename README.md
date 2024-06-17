# Multiple Choice Grader
Esta ferramenta essencialmente acrescenta ferramentas que permitem a melhor utilização do [OMR Checker](https://github.com/Udayraj123/OMRChecker). Toda a parte "difícil" do código, i.e. processamento de imagem e identificação das respostas escolhidas é feita inteiramente por esse código. Este repositório é um _wrapper_ sobre esse repositório. Permite criar folhas de respostas para qualquer número de respostas e opções e permite que toda a interação com o OMR Checker seja feita via ficheiro excel. Permite a criação de relatórios de avaliação individuais que podem ser enviados a cada aluno. Contém também uma ferramenta para enviar esses relatórios para cada aluno por e-mail. Esta ferramenta foi feita com o sistema Fénix do Instituto Superior Técnico em mente. Não será muito difícil de adaptar a outras situações. Esta ferramenta foi desenvolvida em Mac OS. Tipicamente também funcionará em Linux. Em Windows também deverá funcionar, mas não posso garantir.

## Instalação
É necessário instalar todos os pré-requisitos do OMR Checker, mais alguns packages de python.
<details><summary><b>1. Python e OpenCV</b></summary>

  Recomendo a utilização de um ambiente virtual (por exemplo conda), uma vez que é necessário instalar bastantes packages, alguns com versões específicas.

  É preciso ter Python instalado. Tentei pôr isto a funcionar com as versões 3.7, 3.8, 3.12 e 3.11. Entre estas apenas a 3.11 funciona por uma razão ou outra. Para criar um ambiente virtual e instalar a versão 3.11 do Python utilizando o conda faz-se:
  ```bash
  conda create --name nome_do_env
  conda activate nome_do_env
  conda install python=3.11
  conda install pip
  ```

  Para verificar que a instalação foi feita corretamente basta fazer
  ```bash
  python --version
  pip --version
  ```

  **Atenção:** o comando `python` tem de funcionar. Não basta ter, por exemplo, o comando `python3`.
  
  Para instalar o OpenCV basta fazer
  
  ```bash
  pip install opencv-python-headless --verbose
  ```
  Esta instalação demoram bastante tempo (para mim entre 30 a 60 min). A tag `--verbose` está lá apenas para garantir que o computador não empancou na instalação.
  </details>
  
</details>

<details><summary><b>2. Instalar bibliotecas de Python necessárias</b></summary>
Inclui tanto as necessárias para correr o OMR Checker como para correr o restante código. Para as instalar basta utilizar o ficheiro `requirements.txt` como se segue.
  
```bash
pip install -r requirements.txt
```

</details>

<details><summary><b>3. Instalar</b> $\LaTeX$</summary>

É necessário que o utilizador tenha instalado na linha de comandos o comando `pdflatex`. Instalar LaTeX é todo um bicho de sete cabeças, mas não será muito difícil de perceber como fazê-lo com a ajuda da internet. Para verificar que a instalação está bem feita basta verificar se o seguinte comando apresenta a versão instalada:
```bash
pdflatex --version
```

</details>

## Guia de utilização
A preparação e correção de um exame consiste em 6 passos.
<details>
   <summary><b> 0. Configuração</b></summary>
  Várias destas etapas têm passos de configuração que serão delineados nas mesmas. Um ficheiro de configuração estará sempre na pasta `config`.
  
  ### `config/config.json`
  
  - `exam_name`: Nome do exame. Necessário para o passo 4 (aparece no relatório de avaliação). Exemplo: "Exame Época Normal".
  - `exam_date`: Data e hora do exame. Necessário para o passo 4 (aparece no relatório de avaliação).
  - `number_of_questions`: Número de perguntas de escolha múltipla. Necessário para o passo 1. Esta ferramenta aceita um máximo de 60 perguntas.
  - `options_per_question`: Número de opções de resposta em cada escolha múltipla. Necessário para o passo 1. Exemplo: 4 se for de A a D. Esta ferramenta aceitra um máximo de 6 opções.
  - `number_of_versions`: Número de versões do exame. Necessário para o passo 1. Cada versão é identificada com uma letra. O máximo de versões é 6. Ou seja, no máximo há versões de A a F.
  - `answer_keys`: Um dicionário contendo as chaves de resposta para cada versão do exame. Necessário para o passo 4. Exemplo:
  
  ```
  "answer_keys" : {
		"A" : ["E", "C", "C", "B", "D", "A", "A", "D", "A", "B", "B", "A", "D", "D", "E", "C", "C", "E", "BE", "A"],
		"B" : ["E", "A", "A", "D", "A", "B", "B", "A", "B", "C", "B", "A", "A", "A", "E", "D", "C", "E", "CE", "B"],
		"C" : ["C", "C", "E", "B", "D", "A", "D", "A", "B", "A", "B", "A", "D", "D", "E", "C", "C", "BE", "E", "A"],
		"D" : ["A", "E", "A", "D", "A", "B", "A", "B", "C", "B", "B", "A", "A", "E", "D", "A", "CE", "C", "E", "B"]
	}
  ```

   Ou seja, a versão A tem como respostas corretas E, C, C, B, D, etc. Esta ferramenta permite que duas (ou mais) hipóteses sejam consideradas corretas como se vê, por exemplo, na penúltima pergunta da versão A. Basta escrever todas as opções corretas. Alternativamente pode-se declarar as respostas certas numa única string, mas nesse caso apenas se pode indicar uma resposta certa por pergunta. Exemplo:

  ```
  "A" : "ECCBDAADABBADDECCEEA"
  ```

  ### `config/bubble_sheet_template.tex`

  Necessário para o passo 1. É o template LaTeX utilizado para gerar as folhas de respostas. Aqui pode ser configurado o cabeçalho da folha de respostas. Certas linhas não devem ser alteradas. Estão devidamente identificadas com comentários LaTeX.

  ### `config/evaluation_report_template.tex`
  Necessário para o passo 4. É o template LaTeX utilizado para gerar os relatórios de avaliação. Pode ser alterado caso haja alguma informação importante a transmitir (exemplo: a fórmula de cálculo da nota é ... ou na pergunta x duas respostas foram consideradas corretas). Não é um ficheiro LaTeX puro. Contém placeholders que são substituídos por valores. São da forma `{<atributo>}`. As chavetas têm então de ser escapadas. Utilizam-se duas chavetas para escapar uma. Ou seja, `{{` é interpretado como `{`.

 ### `config/grading_function.py`
Necessério para o passo 4. Ficheiro que deve conter uma função Python `grading_function` que recebe o número de respostas certas, incorretas e não respondidas e retorna a nota do teste. Exemplo
```python
def grading_function(correct, incorrect, unanswered):
    return max((correct - 4) * 1.25, 0)
```


### `config/email_text.txt`
 	Necessário para o passo 5. Um ficheiro de texto que contém o subject e o corpo do e-mail enviado aos alunos. A primeira linha do ficheiro é o subject, as restantes são o corpo.

 
</details>
<details>
   <summary><b> 1. Geração de folhas de resposta (bubbles)</b></summary>

  Fazendo `cd` para a pasta do multiple choice grader basta correr o comando
  ```bash
  python mcg.py bubbles
  ```
  No final da execução serão gerados
  - As folhas de respostas que se encontrarão na pasta `answer_sheets`. Um dos ficheiros não terá a versão preenchida (nesse caso o aluno deve preencher a versão do teste que tem), os restantes terão uma das versões já preenchidas. A ideia é que se pode dar a cada aluno uma folha de respostas correspondente à versão do exame que recebe.
  - os ficheiros `aux/OMR_input/reference.png` e `aux/OMR_input/template.json` estes ficheiros serão essenciais ao funcionamento do OMR checker (basicamente indicam onde cada bola está), mas o utilizador não terá de mexer neles.
</details>

<details>
   <summary><b> 2. Realização do teste e digitalização</b></summary>
   Algumas indicações relativamente ao preenchimento da folha de respostas que devem ser transmitidas aos alunos:

   - Todas as bolas devem ser pintadas completamente de maneira nítida para que o exame possa ser corrigido automaticamente.
   - A folha de respostas pode ser preenchida a lápis ou a caneta (a não ser que se decida que o preenchimento deve ser obrigatoriamente a caneta).
   - O número de aluno deve ser preenchido nos 6 retângulos a seguir de "Número:" e as bolas correspondentes devem ser pintadas ([ver exemplo](folha_de_respostas_exemplo.jpg)). Se o número de aluno tiver apenas 5 dígitos, devem-se utilizar apenas os primeiros 5 retângulos. (Os números nos retângulos não serão reconhecidos pelo software, apenas estão lá por questões de redundância. No caso do número de aluno ter 5 dígitos, também se podem preencher os 5 últimos retêngulos ou os 6 retângulos prefixando um zero ao número de aluno)
   - Em caso de engano, no caso de se ter respondido a lápis, deve-se apagar a resposta antiga e pintar a resposta nova. No caso de se ter respondido a caneta, deve-se riscar a resposta antiga e pintar a resposta nova ou indicar a resposta nova de maneira equivalente e inequívoca (ver perguntas 19 e 20 no [exemplo](folha_de_respostas_exemplo.jpg)). Deve-se evitar fazer isto uma vez que uma resposta riscada não consegue ser corrigida automaticamente.

   Depois de se ter resolvido o teste todas as folhas de respostas devem ser digitalizadas em formato .jpg. Cada ficheiro deve conter exatamente uma folha de respostas. Os ficehiros devem ser colocados na pasta `input`. Nessa mesma pasta deve-se colocar um ficheiro Excel (.xls) com a lista de todos os alunos da cadeira. Este é o excel que se obtém no Fénix fazendo Gestão > Alunos > Gerar folha de cálculo.
  
</details>

<details>
   <summary><b> 3. Leitura (reader)</b></summary>

  Correr o comando
  ```bash
  python mcg.py reader
  ```
  Na pasta `output` será gerado o ficheiro excel `reading_results.xls`. Este ficheiro contém uma tabela com todas as respostas registadas. Qualquer erro de leitura que possa ter sido cometido deverá ser corrigido pelo utilizador neste ficheiro. O passo de avaliação utilizará apenas este ficheiro como input.
  
  Quando o programa
  - Não reconheceu a versão de um exame;
  - Reconhece um determinado número de aluno que não se encontra na lista de alunos;
  - Reconhece o mesmo número de aluno em dois testes diferentes.
  Então um erro é gerado. É identificado a vermelho na folha excel. Um erro corresponde a um erro de leitura (com 100% de probabilidade) e tem de ser corrigido para poder avançar para o passo de avaliação.

  Quando o programa, para uma dada questão,
  - Não reconheceu nenhuma resposta assinalada;
  - Reconheceu mais do que uma resposta assinalada.
  Então um aviso (warning) é gerado. É identificado a amarelo na folha excel. Um aviso corresponde a um *provável* erro de leitura. Por exemplo, se para uma dada questão não é identificada nenhuma resposta assinalada, é mais provável que a bola esteja pintada levemente do que o aluno não tenha respondido. No caso de se reconhecer mais do que uma resposta assinalada, o mais provável é que o aluno tenha riscado uma das opções. Claro que é possível que o aluno de facto não tenha respondido a uma questão. Nesse caso deve-se simplesmente ignorar o aviso.

  Nas linhas que contenham um erro ou um aviso o utilizador deverá consultar o ficheiro de digitalização original e corrigir os erros de leitura.

</details>

<details>
   <summary><b> 4. Avaliação (grader)</b></summary>

   O passo de avaliação utiliza apenas o ficheiro `output/reading_results.xls`. Todos os erros de leitura devem ser corrigidos nesse ficheiro antes de correr o script de avaliação. Para isso basta correr o comando 
  ```bash
  python mcg.py grader
  ```

  Os dados presentes em `output/reading_results.xls` são agora processados de acordo com as chaves de resposta e função de avaliação explicitadas na configuração.
  Na pasta `output` serão gerados os seguintes ficheiros:
  - `graded_results.xls` é um ficheiro excel que contém os resultados detalhados do exame após a correção. A sheet "Pauta" contém uma lista de todos os alunos e a nota do exame daqueles que entregaram. Tipicamente será esta a sheet a publicar no Fénix.
  - A diretoria `evaluation_reports`. Dentro dela encontra-se um documento pdf por cada teste. O nome do documento contém o número do aluno correspondente. Cada relatório de avaliação tem duas páginas. Na primeira o alumo encontra uma tabela com as respostas que foram lidas pelo script, assim como a sua nota no exame. Na segunda encontra a digitalização do seu teste. A ideia é que estes ficheiros sejam distribuídos pelos alunos para facilitar a revisão de provas.
  - Será ainda gerado o ficheiro `evaluation_reports/email_adresses.json`. Este ficheiro é utilizado no passo 5 para enviar os relatórios de avaliação aos alunos.
</details>

<details>
   <summary><b> 5. Envio dos relatórios de avaliação (sender)</b></summary>

   Os relatórios de avaliação gerados no passo anterior são enviados por e-mail individualmente a cada aluno. O endereço de e-mail de cada aluno utilizado é o presente na lista de alunos. Para tal é necessário fornecer os detalhes (e-mail e password) de uma conta de e-mail do Técnico (@tecnico.ulisboa.pt). Se o utilizador não confia a sua password ao meu script então sugiro que encontre outra maneira automática de distribuir n documentos pdf. Aproveite para me dizer qual porque procurei bastante e não encontrei.
   
   O script demora algum tempo pois espera 5 segundos entre o envio de cada e-mail. Se demasiados e-mails forem enviados num curto espaço de tempo o servidor do Técnico faz birra. Não sei se 5 segundos é o tempo mais pequeno possível, não testei. Para correr o script:
   ```bash
  python mcg.py sender
  ```
  E seguir as instruções.

  **Atenção:** se por alguma razão este processo for parado a meio então apenas alguns dos alunos receberão os e-mails. Não é gerada uma lista dos alunos a quem um e-mail foi enviado, pelo que depois todos os e-mails terão de ser enviados de novo.
  
</details>
