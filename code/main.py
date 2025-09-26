from settings import *
from RedeNeural import *
from button import *
from instruction import *

#======================== Classe Jogo ========================

class Game():
    def __init__(self):
        #======================== Setup inicial ========================
        pygame.init()
        #--Define tamanho da tela--
        self.display_surface = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
        
        #--Carrega o icone--
        Icon_surf = pygame.image.load(join("assets","Icone.png")).convert_alpha()
        pygame.display.set_icon(Icon_surf)
        #--Define o nome da janela--
        pygame.display.set_caption("Prototipo 01")
        #--Variável que mantem o jogo rodando--
        self.running = True
        self.clock = pygame.time.Clock()
        #--Variável para guardar palpites--
        self.GUESS = ""
        #--Variável que contem o momento que a rodada começa para calcular o tempo do jogo--
        self.Start_game_time = pygame.time.get_ticks() // 1000
        

        #======================== Drawing_Space setup ========================
        #--Define tamanho do espaço de desenho--
        self.Drawing_Space_position = (WINDOW_WIDHT-25,WINDOW_HEIGHT-40)
        self.Drawing_Space_image = pygame.Surface((465,465))
        self.Drawing_Space_rect = self.Drawing_Space_image.get_frect(bottomright=self.Drawing_Space_position)
        self.Drawing_Space_image.fill((142, 120, 96))
        #--Inicia a lista de coordenadas, usadas para desenhar--
        #--Lista de linhas desenhadas, formada de listas de coordenadas (Coordinate_list) cada vez que o jogador desenha uma nova linha
        self.Coordinate_lists = []
        #--Lista de coordenadas de uma linha desenhada pelo jogador. É adicionada a Coordinate_lists toda vez que o jogador termina de desenhar uma linha
        self.Coordinate_list = []
        #--Variável para a lógica de desenho
        self.Is_drawning = False
        #--Variáveis da cor da linha--
        self.Line_Color = pygame.color.Color(255,255,255)
        self.Outline_Color = pygame.color.Color(200,200,200)
        self.color_up = [False,False,False]
        #--Coordenadas de mouse--
        #--Lista de coordenadas completa de um desenho, gerada após o jogador confirmar que o desenho está pronto--
        self.Drawing_Coordinates = []
        self.mouse_pos = pygame.mouse.get_pos()
        self.last_mouse_position = self.mouse_pos

        #======================== Imports ========================
        Circulo_surf = pygame.image.load(join("assets","Circulo.png")).convert_alpha()
        Coroa_surf = pygame.image.load(join("assets","Coroa.png")).convert_alpha()
        Baixo_surf = pygame.image.load(join("assets","Seta_baixo.png")).convert_alpha()
        Cima_surf = pygame.image.load(join("assets","Seta_cima.png")).convert_alpha()
        Esquerda_surf = pygame.image.load(join("assets","Seta_esquerda.png")).convert_alpha()
        Direita_surf = pygame.image.load(join("assets","Seta_direita.png")).convert_alpha()
        self.Background = pygame.image.load(join("assets","fundo.png")).convert_alpha()
        self.Background_menu = pygame.image.load(join("assets","fundo_embacado.png")).convert_alpha()


        self.Instruction_surfs = [Circulo_surf,Coroa_surf,Baixo_surf,Cima_surf,Direita_surf,Esquerda_surf]

        #---Texto jogo--
        self.instruc_text = pygame.image.load(join("assets","instrucoes.png")).convert_alpha()
        self.pontos_text = pygame.image.load(join("assets","pontos.png")).convert_alpha()

        #--Texto Menu--
        self.botao_jogar = pygame.image.load(join("assets","botao_jogar.png")).convert_alpha()
        self.botao_sair = pygame.image.load(join("assets","botao_sair.png")).convert_alpha()
        self.titulo = pygame.image.load(join("assets","titulo.png")).convert_alpha()

        #--Texto fim de jogo--
        self.botao_jogar_de_novo = pygame.image.load(join("assets","botao_jogar_de_novo.png")).convert_alpha()
        self.botao_menu_principal = pygame.image.load(join("assets","botao_menu_principal.png")).convert_alpha()
        self.pontuacao = pygame.image.load(join("assets","pontuacao.png")).convert_alpha()

        #======================== Sprites ========================
        self.All_Sprites = pygame.sprite.Group()
        self.Instruction_sprites = pygame.sprite.Group()

        #======================== Botões ========================
        self.Btn_jogar = Button(self.botao_jogar,(WINDOW_WIDHT/2,292),self.display_surface)
        self.Btn_sair = Button(self.botao_sair,(WINDOW_WIDHT/2,410),self.display_surface)

        self.Btn_menu_principal = Button(self.botao_menu_principal,(WINDOW_WIDHT/2,410),self.display_surface)
        self.Btn_jogar_de_novo = Button(self.botao_jogar_de_novo,(WINDOW_WIDHT/2,292),self.display_surface)

        #======================== Rede Neural ========================
        self.CNN = RedeNeural()

        #======================== outras variaveis ========================
        self.Full_timer = 15 
        self.points = 0
        self.points_to_gain = 0

    #======================= Funções ===================================
    #--Telas--
    #--Tela de jogo--
    def run_game(self):
        #--Zera variáveis do jogo--
        self.Full_timer = 15 
        self.points = 0
        self.points_to_gain = 0
        self.Start_game_time = pygame.time.get_ticks() // 1000

        #--Cria as instruções--
        self.Instruction_list()

        #--Game loop--
        while self.running:
            #Delta time (ms)
            dt = self.clock.tick() / 1000

            #Event loop
            for event in pygame.event.get():
                #--Fecha o jogo quando fecha a janela--
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                #--Finaliza a rodada quando pressiona ESC--
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        for sprite in self.Instruction_sprites.sprites():
                            sprite.kill()
                        #Zera as coordenadas
                        self.Coordinate_lists = []
                        self.Coordinate_list = []
                        self.end_game()

            #Checa se as instruções foram concluidas e cria novas caso necessário
            #Também adiciona mais tempo no timer baseado no número de instruções concluidas
            if not self.Instruction_sprites.sprites():
                self.Full_timer += self.points_to_gain * 2
                self.points += self.points_to_gain * 100
                self.points_to_gain = 0
                self.Instruction_list()

            #Atualiza o timer
            #O tempo é calculado com o valor base do timer, que é incrementado sempre que uma sequência de instruções é concluida
            #menos o tempo que se passou desde que a rodada começou (Momento em que a rodada começou subtraido do tempo que o jogo está rodando)
            Time_Value = self.Full_timer + self.Start_game_time - pygame.time.get_ticks()//1000 

            #==============Drawing the game=================
            #--Coloca o background--
            self.display_surface.blit(self.Background)
            #--Desenha os sprites, nesse caso as instruções--
            self.All_Sprites.draw(self.display_surface)
            #--Desenha o espaço para desenhar--
            self.display_surface.blit(self.Drawing_Space_image,self.Drawing_Space_rect)
            #--Contorno do drawing space
            pygame.draw.rect(self.display_surface, (95,74,17), self.Drawing_Space_rect.inflate(10,10), 5, 15)
            #--Desenha o timer--
            self.Display_time(Time_Value)
            #--Desenha o palpite--
            self.Display_guess(self.GUESS)
            #--Desenha os pontos--
            points_text = str(self.points)
            self.Display_points_2(points_text)
            #--Desenha as instruções--
            self.Display_instrunctions_2()

            #--Da update nos sprites--
            self.All_Sprites.update(dt)
            self.Update_Drawing_Space(dt)

            #--Checa se o tempo acabou. Caso o tempo tenha acabado encerra a rodada--
            if Time_Value <= 0:
                for sprite in self.Instruction_sprites.sprites():
                    sprite.kill()
                #Zera as coordenadas
                self.Coordinate_lists = []
                self.Coordinate_list = []
                self.end_game()

            #Update display
            pygame.display.update()

        #--Quando sai do loop do jogo, encerra o programa--
        pygame.quit()

    #--Tela do menu--
    def main_menu(self):
        while self.running:
            #Delta time (ms)
            dt = self.clock.tick() / 1000

            #Event loop
            for event in pygame.event.get():
                #--Fecha o jogo quando fecha a janela--
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                #--Checa se os botões foram pressionados e roda suas respectivas funções--
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.Btn_jogar.check_click(pygame.mouse.get_pos()):
                        self.run_game()
                    elif self.Btn_sair.check_click(pygame.mouse.get_pos()):
                        self.running = False
                        sys.exit()

            #--Desenha o background--
            self.display_surface.blit(self.Background_menu)

            #--Titulo--
            titulo_rect = self.titulo.get_frect(center= (WINDOW_WIDHT/2,120))
            self.display_surface.blit(self.titulo,titulo_rect)
            #--Instruções--
            self.Display_instrunctions_2()

            #botoes
            self.Btn_jogar.draw()
            self.Btn_sair.draw()

            #Update display
            pygame.display.update()

        pygame.quit()
    
    def end_game(self):
        while self.running:
            #Delta time (ms)
            dt = self.clock.tick() / 1000

            #Event loop
            for event in pygame.event.get():
                #--Fecha o jogo quando fecha a janela--
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                #--Checa se os botões foram pressionados e roda suas respectivas funções--
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.Btn_jogar_de_novo.check_click(pygame.mouse.get_pos()):
                        self.run_game()
                    elif self.Btn_menu_principal.check_click(pygame.mouse.get_pos()):
                        self.main_menu()

            #--Desenha o background--
            self.display_surface.blit(self.Background_menu)

            #--Pontuacao texto--
            pontuacao_rect = self.pontuacao.get_frect(center= (WINDOW_WIDHT/2,120))
            self.display_surface.blit(self.pontuacao,pontuacao_rect)
            #--Pontuação valor--
            points_surf = pygame.font.Font(size=50).render(str(self.points), True, (46,21,1))
            points_rect = points_surf.get_frect(center=(WINDOW_WIDHT/2,195))
            self.display_surface.blit(points_surf, points_rect)

            #botoes
            self.Btn_jogar_de_novo.draw()
            self.Btn_menu_principal.draw()

            #Update display
            pygame.display.update()

        pygame.quit()

    #--Cria uma lista de instruções aleatórias, de tamanho variável (1 a 4) 
    def Instruction_list(self):
        Instruction_numbers = randint(1,4)
        position = pygame.math.Vector2(20,20)
        while Instruction_numbers:
            number = randint(0,5)
            Instruction(number,pygame.transform.rotozoom(self.Instruction_surfs[number],0,0.75),position,(self.All_Sprites,self.Instruction_sprites))
            Instruction_numbers -= 1
            position.x += 100

    #--Faz várias checagens no Drawing space--
    def Update_Drawing_Space(self,dt):
        #Pega informações sobre as teclas pressionadas
        keys = pygame.key.get_just_pressed()
        #Limpa a lista de coordenadas do último palpite para que possa ser preenchida de novo caso ESPAÇO seja pressionado
        self.Drawing_Coordinates.clear()
        #Checa se espaço foi pressionado e caso seja, junta as listas de coordenadas na variável Drawing_Coordinates para que seja feita a previsão com a rede neural
        if keys[pygame.K_SPACE]:
            for i in range(len(self.Coordinate_lists)):
                self.Drawing_Coordinates.extend(self.Coordinate_lists[i])
            #Só avança se a lista não estiver vazia
            if self.Drawing_Coordinates:
                self.Prediciton()
                self.Coordinate_list.clear()
                self.Coordinate_lists.clear()
            
        #Pega a posição do mouse no frame atual
        self.mouse_pos = pygame.mouse.get_pos()

        #Se o jogador estava desenhando e tira o mouse do Drawing space ou solta o clique
        #Atualiza a variavel Is_drawing para False e coloca a ultima linha desenhanda na lista de linhas (Coordinate_lists) e limpa a lista de coordenadas da linha
        if self.Is_drawning and ((not self.Drawing_Space_rect.collidepoint(self.mouse_pos)) or (not pygame.mouse.get_pressed()[0])):
            self.Is_drawning = False
            self.Coordinate_lists.append(self.Coordinate_list.copy()) 
            self.Coordinate_list.clear()
        #Se o jogador está com o mouse no Drawing space e está clicando com o botão esquerdo do mouse
        #Atualiza a variável Is_drawing e salva as coordenadas do mouse na lista de coordenadas da linha atual
        elif self.Drawing_Space_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.Is_drawning = True
            if self.mouse_pos != self.last_mouse_position:
                self.Coordinate_list.append(self.mouse_pos)
                self.last_mouse_position = self.mouse_pos

        #Atualiza a cor da linha
        self.Update_Line_Color(dt)
        #Desenha as linhas para que o jogador possa ver oque foi desenhado
        self.Draw_Figure()
    
    def Update_Line_Color(self,dt):
        #O valor de cada cor varia de 0 a 255, de maneira crescente e decrescente alternadamente
        #A variável color_up guarda os 3 valores, um para cada cor, que registra quando cada variável tem que subir e quando tem que descer
        #O novo valor e calculado antes de ser aplicado. Caso o valor calculado não esteja entre os valores estabelecidos
        #Ele é recalibrado e a variável color_up é atualizada

        #Variação da cor vermelha
        if self.color_up[0]:
            new_red = self.Line_Color.r + int(600 * dt)
        else:
            new_red = self.Line_Color.r - int(600 * dt)
        while not (new_red >= 0 and new_red <= 255):
            if new_red > 255:
                new_red = 255 - (new_red-255)
                self.color_up[0] = False
            elif new_red < 0:
                new_red = - new_red
                self.color_up[0] = True
        self.Line_Color.r = new_red

        #Variação da cor verde
        if self.color_up[1]:
            new_green = self.Line_Color.g + int(400 * dt)
        else:
            new_green = self.Line_Color.g - int(400 * dt)
        while not (new_green >= 0 and new_green <= 255):
            if new_green > 255:
                new_green = 255 - (new_green-255)
                self.color_up[1] = False
            elif new_green < 0:
                new_green = - new_green
                self.color_up[1] = True
        self.Line_Color.g = new_green

        #Variação da cor azul
        if self.color_up[2]:
            new_blue = self.Line_Color.b + int(400 * dt)
        else:
            new_blue = self.Line_Color.b - int(400 * dt)
        while not (new_blue >= 0 and new_blue <= 255):
            if new_blue > 255:
                new_blue = 255 - (new_blue-255)
                self.color_up[2] = False
            elif new_blue < 0:
                new_blue = - new_blue
                self.color_up[2] = True
        self.Line_Color.b = new_blue

    def Draw_Figure(self):
        #Desenhando o contorno branco
        #Se o jogador está desenhando uma linha e essa linha tem mais de um ponto
        if self.Coordinate_list and len(self.Coordinate_list)>1:
            #Usa a função draw para ligar os pontos da linha
            pygame.draw.lines(self.display_surface,self.Outline_Color,False,self.Coordinate_list,15)
            #Desenha um ponto em cada ponto da linha para melhorar a linha visualmente
            for point in self.Coordinate_list:
                pygame.draw.circle(self.display_surface,self.Outline_Color,point,7)
        
        #Para cada linha na lista de linhas desenhadas previamente
        for Line in self.Coordinate_lists:
            if len(Line)>1:
                #Liga os pontos da linha se ela tiver mais de um ponto
                pygame.draw.lines(self.display_surface,self.Outline_Color,False,Line,15)
            for point in Line:
                #Desenha os pontos da linha
                pygame.draw.circle(self.display_surface,self.Outline_Color,point,7)

        #Desenhando com cor
        #Se o jogador está desenhando uma linha e essa linha tem mais de um ponto
        if self.Coordinate_list and len(self.Coordinate_list)>1:
            #Usa a função draw para ligar os pontos da linha
            pygame.draw.lines(self.display_surface,self.Line_Color,False,self.Coordinate_list,10)
            #Desenha um ponto em cada ponto da linha para melhorar a linha visualmente
            for point in self.Coordinate_list:
                pygame.draw.circle(self.display_surface,self.Line_Color,point,4)

        #Para cada linha na lista de linhas desenhadas previamente
        for Line in self.Coordinate_lists:
            #Se a linha tiver mais de um ponto
            if len(Line)>1:
                #Liga os pontos da linha se ela tiver mais de um ponto
                pygame.draw.lines(self.display_surface,self.Line_Color,False,Line,10)
            for point in Line:
                #Desenha os pontos da linha
                pygame.draw.circle(self.display_surface,self.Line_Color,point,4)
    
    def Prediciton(self):
        #Função checa a lista de coordenadas para fazer a previsão com a rede neural
        
        #Se a lista de coordenadas não for pequena demais
        if len(self.Drawing_Coordinates) > 10:
            #Manda as coordenadas para a rede neural e faz a previsão
            Pred_answer, Pred_value = self.NeuralNetworkPred(self.CNN,self.Drawing_Coordinates)
            #Transforma a resposta em int para poder ser usada para comparação
            Pred_answer = int(Pred_answer)
            #Cada resposta representa, de 0 a 5 = ["Circulo","Coroa","Baixo","Cima","Direita","Esquerda"]
            #A função CheckAnswer é usada para identificar se o desenho identificado pela rede é a resposta para a próxima instrução da lista de instruções
            #Cada desenho tem um valor necessário de Pred_value para que a identificação seja considerada
            if Pred_answer == 0 and Pred_value >= 20:
                self.CheckAnswer(Pred_answer)
            elif Pred_answer == 1 and Pred_value >= 16:
                self.CheckAnswer(Pred_answer)
            elif Pred_answer == 2 and Pred_value >= 15:
                self.CheckAnswer(Pred_answer)
            elif Pred_answer == 3 and Pred_value >= 15:
                self.CheckAnswer(Pred_answer)
            elif Pred_answer == 4 and Pred_value >= 15:
                self.CheckAnswer(Pred_answer)
            elif Pred_answer == 5 and Pred_value >= 15:
                self.CheckAnswer(Pred_answer)
            #Se o valor de Pred_value não estiver acima do estabelecido para a classe ela não é identificada e o tempo é diminuido
            else:
                self.Change_Guess("Não Identificado")
                self.Full_timer -= 1
        #Se a lista de coordenadas for pequena demais o desenho é rejeitado automaticamente
        else:
            self.Change_Guess("Desenho muito pequeno")
            self.Full_timer -= 1

    def ImageNormalization(self,Coordinates):
        #Separa as coordenadas em 2 vetores, um para X e um para Y
        X_Coords =[]
        Y_Coords = []
        for pair in Coordinates:
            X_Coords.append(pair[0])
            Y_Coords.append(pair[1])

        #Pega os valores máximos e mínimos
        X_max = max(X_Coords)
        X_min = min(X_Coords)
        Y_max = max(Y_Coords)
        Y_min = min(Y_Coords)

        #Calcula a amplitude de cada eixo
        XAmplitude = X_max - X_min
        YAmplitude = Y_max - Y_min

        if XAmplitude > YAmplitude:
            # Altera as coordenadas para ir de 0 ate a aplitude maxima e centraliza a amplitude menor
            Amp = XAmplitude
            for i in range(len(X_Coords)):
                X_Coords[i] = X_Coords[i] - X_min
                Y_Coords[i] = Y_Coords[i] - Y_min + (Amp/2) - (YAmplitude/2)
        else:
            # Altera as coordenadas para ir de 0 ate a aplitude maxima e centraliza a amplitude menor
            Amp = YAmplitude
            for i in range(len(X_Coords)):
                X_Coords[i] = X_Coords[i] - X_min + (Amp/2) - (XAmplitude/2)
                Y_Coords[i] = Y_Coords[i] - Y_min

        DrawSmall = []
        for i in range(len(X_Coords)):
            # Reduz a amplitude para 28x28 com 2 pixels de borda e arredonda os resultados
            newpair = []
            newpair.append(((23/Amp)*X_Coords[i]) + 2)
            newpair.append(((23/Amp)*Y_Coords[i]) + 2) 
            newpairR = np.int32(np.rint(newpair))
            DrawSmall.append(newpairR)
        # Deixa apenas os pares únicos, excluindo os repetidos após o arredondamento
        DrawSmall = np.unique(DrawSmall,axis=0)

        #Desenha a imagem 28x28
        imgSmall = np.full((28,28), 0, dtype=np.uint8)
        for pair in DrawSmall:
            imgSmall[pair[1]][pair[0]] = 255

        #Retorna o desenho nas dimensões 28x28

        return imgSmall
    
    def NeuralNetworkPred(self,CNN,Coordinates):
        #Recebe as coordenadas do desenho, transforma em uma imagem de 28x28 com a função ImageNormalization e retorna a previsão da rede neural
        Drawing = self.ImageNormalization(Coordinates)
        return CNN.Prediciton(Drawing)
    
    def CheckAnswer(self,Answer):
        #Pega a primeira instrução da lista
        sprite = self.Instruction_sprites.sprites()[0]
        #Se a resposta recebida for correspondente a da instrução
        #Aumenta os pontos que o jogador vai ganhar em 100 e apaga a instrução, alem de encerrar a função
        if Answer == sprite.type:
            self.Change_Guess("Correto")
            self.points_to_gain += 1
            sprite.kill()
            return
        #Se a resposta recebida não corresponder o tempo é diminuido
        self.Change_Guess("Incorreto")
        self.Full_timer -= 1
    
    def Display_time(self,Time):
        #Desenha o timer com o valor recebido
        text_surf = pygame.font.Font(size=100).render(str(Time), True, (46,21,1))
        text_rect = text_surf.get_frect(midbottom= (WINDOW_WIDHT/2,WINDOW_HEIGHT-50))
        pygame.draw.rect(self.display_surface, (255,248,231), text_rect.inflate(20,20).move(0,-7), 0, 15)
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, (46,21,1), text_rect.inflate(20,20).move(0,-7), 5, 15)

    def Display_guess(self,Text):
        #Desenha o texto correspondente ao ultimo palpite
        text_surf = pygame.font.Font(size=50).render(str(Text), True, (46,21,1))
        text_rect = text_surf.get_frect(center=(1000,170))
        self.display_surface.blit(text_surf, text_rect)

    def Display_points(self,Points):
        #Desenha os pontos na tela
        text_surf = pygame.font.Font(size=50).render(str(Points), True, (46,21,1))
        text_rect = text_surf.get_frect(bottomleft=(15,WINDOW_HEIGHT-100))
        self.display_surface.blit(text_surf, text_rect)
    
    def Display_points_2(self,Points):
        #Desenha os pontos na tela
        pontos_rect = self.pontos_text.get_frect(topleft=(23,376))
        text_surf = pygame.font.Font(size=50).render(str(Points), True, (46,21,1))
        text_rect = text_surf.get_frect(topleft=(205,376))
        self.display_surface.blit(text_surf, text_rect)
        self.display_surface.blit(self.pontos_text,pontos_rect)

    def Change_Guess(self,text):
        #Muda o palpite
        self.GUESS = text

    def Display_instrunctions(self):
        #Desenha as instruções na tela
        Text1 = "Desenhe os símbolos nas instruções"
        Text2 = "Desenhe na ordem"
        Text3 = "Pressione ESPAÇO para confirmar"
        text1_surf = pygame.font.Font(size=30).render(str(Text1), True, (46,21,1))
        text2_surf = pygame.font.Font(size=30).render(str(Text2), True, (46,21,1))
        text3_surf = pygame.font.Font(size=30).render(str(Text3), True, (46,21,1))
        text1_rect = text1_surf.get_frect(bottomleft=(15,WINDOW_HEIGHT-200))
        text2_rect = text2_surf.get_frect(bottomleft=(15,WINDOW_HEIGHT-175))
        text3_rect = text3_surf.get_frect(bottomleft=(15,WINDOW_HEIGHT-150))
        self.display_surface.blit(text1_surf, text1_rect)
        self.display_surface.blit(text2_surf, text2_rect)
        self.display_surface.blit(text3_surf, text3_rect)

    def Display_instrunctions_2(self):
        #Desenha as instruções na tela
        instruc_rect = self.instruc_text.get_frect(topleft = (15,448))
        self.display_surface.blit(self.instruc_text,instruc_rect)


if __name__ == "__main__":
    game = Game()
    game.main_menu()