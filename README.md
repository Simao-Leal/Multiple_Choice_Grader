# Multiple Choice Grader
Esta ferramenta essencialmente acrescenta ferramentas que permitem a melhor utilização do [OMR Checker](https://github.com/Udayraj123/OMRChecker). Toda a parte "difícil" do código, i.e. processamento de imagem e identificação das respostas escolhidas é feita inteiramente por esse código. Este repositório é um _wrapper_ sobre esse repositório. Permite criar folhas de respostas para qualquer número de respostas e opções e permite que toda a interação com o OMR Checker seja feita via ficheiro excel. Permite a criação de relatórios de avaliação individuais que podem ser enviados a cada aluno. Contém também uma ferramenta para enviar esses relatórios para cada aluno por e-mail. Esta ferramenta foi feita com o sistema Fénix do Instituto Superior Técnico em mente. Não será muito difícil de adaptar a outras situações. Esta ferramenta foi desenvolvida em Mac OS. Tipicamente também funcionará em Linux. Em Windows também deverá funcionar, mas não posso garantir.

## Instalação
É necessário instalar todos os pré-requisitos do OMR Checker, mais alguns packages de python. Algumas das instruções abaixo estão em inglês porque foram copiadas do OMR Checker.
<details><summary><b>1. Python e OpenCV</b></summary>

  ![opencv 4.0.0](https://img.shields.io/badge/opencv-4.0.0-blue.svg) ![python 3.5+](https://img.shields.io/badge/python-3.5+-blue.svg)
  
  To check if python3 and pip is already installed:
  
  ```bash
  python3 --version
  python3 -m pip --version
  ```
  
  <details>
  	<summary><b>Install Python3</b></summary>
  
  To install python3 follow instructions [here](https://www.python.org/downloads/)
  
  To install pip - follow instructions [here](https://pip.pypa.io/en/stable/installation/)
  
  </details>
  <details>
  <summary><b>Install OpenCV</b></summary>
  
  **Any installation method is fine.**
  
  Recommended:
  
  ```bash
  python3 -m pip install --user --upgrade pip
  python3 -m pip install --user opencv-python
  python3 -m pip install --user opencv-contrib-python
  ```
  
  More details on pip install openCV [here](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/).
  
  </details>
  
  <details>
  
  <summary><b>Extra steps(for Linux users only)</b></summary>
  
  <b>Installing missing libraries(if any):</b>
  
  On a fresh computer, some of the libraries may get missing in event after a successful pip install. Install them using following commands[(ref)](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/):
  
  ```bash
  sudo apt-get install -y build-essential cmake unzip pkg-config
  sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
  sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
  sudo apt-get install -y libatlas-base-dev gfortran
  ```
  
  </details>
</details>

<details><summary><b>2. Instalar bibliotecas de Python necessárias</b></summary>
Inclui tanto as necessárias para correr o OMR Checker como para correr o restante código. Para as instalar basta utilizar o ficheiro `requirements.txt` como se segue. Eventualmente o utilizador quererá utilizar um ambiente virtual para isto (pesquisar sobre conda).
  
```bash
python3 -m pip install --user -r requirements.txt
```

</details>

## Guia de utilização
A preparação e correção de um exame consiste em 5 passos.
<details>
   <summary><b> 0. Configuração</b></summary>
  Várias destas etapas têm passos de configuração que serão delineados nas mesmas. Um ficheiro de configuração estará sempre na pasta `config`.
  
  ### `config/config.json`
  
  - `exam_name`: Nome do exame. Necessário para o passo 3 (aparece no relatório de avaliação). Exemplo: "Exame Época Normal".
  - `exam_date`: Data e hora do exame. Necessário para o passo 3 (aparece no relatório de avaliação).
  - `number_of_questions`: Número de perguntas de escolha múltipla. Necessário para o passo 1. Esta ferramenta aceita um máximo de 60 perguntas.
  - `options_per_question`: Número de opções de resposta em cada escolha múltipla. Necessário para o passo 1. Exemplo: 4 se for de A a D. Esta ferramenta aceitra um máximo de 6 opções.
  - `number_of_versions`: Número de versões do exame. Necessário para o passo 1. Cada versão é identificada com uma letra. O máximo de versões é 6. Ou seja, no máximo há versões de A a F.
  - `answer_keys`: Um dicionário contendo as chaves de resposta para cada versão do exame. Necessário para o passo 3. Exemplo:
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

  Necessário para o passo 1. É o template LaTeX utilizado para gerar as folhas de respostas. Aqui pode ser configurado o cabeçalho da folha de respostas. Certas linhas não devem ser alteradas. Estão devidamente identificadas com comentários.

  ### `config/evaluation_report_template.tex`
  Necessário para o passo 3. É o template LaTeX utilizado para gerar os relatórios de avaliação. Pode ser alterado caso haja alguma informação importante a transmitir (exemplo: na pergunta x duas respostas foram consideradas corretas). Não é um ficheiro LaTeX puro. Contém placeholders que são substituídos por valores. São da forma `{<atributo>}`. As chavetas têm então de ser escapadas. Utilizam-se duas chavetas para escapar uma. Ou seja, `{{` é interpretado como `{`.
</details>

<details>
   <summary><b> 1. Geração de folhas de resposta</b></summary>

