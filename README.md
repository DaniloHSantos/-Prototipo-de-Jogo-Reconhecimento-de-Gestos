<h1 align="center">Prototipo: Jogo com Reconhecimento de Gestos</h1>
<img alt="Static Badge" src="https://img.shields.io/badge/license-MIT-green">

Repósitório do meu projeto de graduação, um protótipo de um jogo que usa rede neural para identificar símbolos desenhados pelo jogador

# Funcionalidades

Esse projeto é constituido por um jogo simples. Esse jogo é representado por 3 telas:

<p align="center">Tela de menu principal</p>
<img alt="Tela de menu principal" src="https://github.com/DaniloHSantos/Prototipo-Jogo-Reconhecimento-de-Gestos/blob/main/ImgREADME/telaMenu.png?raw=true">
No canto inferior esquerdo da tela se encontram as instruções de como jogar. No meio da tela estão localizados os 2 botões principais, o botão de jogar, para iniciar o jogo e o botão de sair, para fechar a aplicação.

<p align="center">Tela de Jogo</p>
<img alt="Tela de menu principal" src="https://github.com/DaniloHSantos/Prototipo-Jogo-Reconhecimento-de-Gestos/blob/main/ImgREADME/telaJogo.png?raw=true">
Nessa tela as instruções continuam visíveis, no mesmo lugar que se encontram no menu principal. Logo acima das instruções é mostrado os pontos que o jogador fez na rodada. No canto superior esquerdo ficam as instruções que o jogador deve desenhar, na ordem da esquerda para a direita. Na parte central inferior da tela se encontra o timer que mostra quanto tempo resta na rodada. No canto direito da tela fica a área de desenho, onde o jogador deve fazer um desenho para tentar corresponder a instrução dada pelo jogo. Logo acima da área de desenho fica a resposta do jogo em relação ao ultimo desenho confirmado pelo jogador, dizendo se foi correto, incorreto ou não identificado.

<p align="center">Tela de Fim de Jogo</p>
<img alt="Tela de menu principal" src="https://github.com/DaniloHSantos/Prototipo-Jogo-Reconhecimento-de-Gestos/blob/main/ImgREADME/telaFimdejogo.png?raw=true">
Na tela de fim de jogo é mostrada a pontuação alcançada pelo jogador na ultima rodada. Além disso no centro da tela existem 2 botões, um para jogar outra rodada e outro par voltar ao menu principal.

# Como rodar a aplicação

Para rodar a aplicação é necessário seguir os seguintes passos:
- Certifique-se de ter uma versão igual ou superior a 3.12.8 do Python instalada. O download pode ser realizado no site: [Download Python | Python.org](https://www.python.org/downloads/)
- Clone esse repositório em um diretório de sua escolha.
- Apesar de não ser necessário, é recomendado que você crie um ambiente virtual para o projeto.
- Abra o terminal no diretório do repositório e digite o comando:
```pip install -r requirements.txt``` para instalar as dependências do projeto.
- Para iniciar a aplicação vá entre na pasta ```code``` execute o arquivo ```main.py```.

# Tecnologias Utilizadas

- ```Pyhton```
- ```Machine Learning```
- ```Redes neurais```

# Autor

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/117547163?v=4" width=115><br><sub>Danilo Honorio dos Santos</sub>](https://github.com/DaniloHSantos) |
| :---: |