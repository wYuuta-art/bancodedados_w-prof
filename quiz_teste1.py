import psycopg2
import pygame
import sys

# BANCO DE DADO
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="yuuta123"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz (
    id SERIAL PRIMARY KEY,
    pergunta TEXT UNIQUE NOT NULL,
    alternativa_a TEXT NOT NULL,
    alternativa_b TEXT NOT NULL,
    alternativa_c TEXT,
    alternativa_d TEXT,
    resposta_correta CHAR(1) NOT NULL,
    dificuldade VARCHAR(20),
    assunto VARCHAR(50),
    explicacao TEXT,
    tipo VARCHAR(10) DEFAULT 'normal'
);
""")
conn.commit()

#PYGAME
pygame.init()
tela = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Quiz Zona A4")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

#MENU
def menu_principal():
    opcoes = ["Jogar", "Adicionar Pergunta", "Editar Pergunta", "Excluir Pergunta", "Sair"]
    while True:
        tela.fill((30,30,30))
        tela.blit(font.render("MENU PRINCIPAL", True, (255,255,255)), (300, 80))
        botoes = []
        for i, op in enumerate(opcoes):
            ret = pygame.Rect(200, 180 + i*70, 400, 50)
            pygame.draw.rect(tela, (70,130,180), ret)
            tela.blit(font.render(op, True, (255,255,255)), (320, 195 + i*70))
            botoes.append((ret, op))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for ret, op in botoes:
                    if ret.collidepoint(event.pos):
                        return op
        clock.tick(60)

#FUNÇÕES
class CaixaDeTexto:
    def __init__(self, x, y, largura, altura, texto=''):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_inativa = (150,150,150)
        self.cor_ativa = (70,130,180)
        self.cor = self.cor_inativa
        self.texto = texto
        self.superficie_texto = font.render(texto, True, (255,255,255))
        self.ativa = False

    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # ativa se clicar dentro da caixa
            self.ativa = self.rect.collidepoint(evento.pos)
            self.cor = self.cor_ativa if self.ativa else self.cor_inativa
        if evento.type == pygame.KEYDOWN and self.ativa:
            if evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                self.texto += evento.unicode
            self.superficie_texto = font.render(self.texto, True, (255,255,255))

    def desenhar(self, tela):
        # desenhar o texto
        tela.blit(self.superficie_texto, (self.rect.x+5, self.rect.y+5))
        # desenhar a borda da caixa
        pygame.draw.rect(tela, self.cor, self.rect, 2)


def adicionar_pergunta_pygame():
    # criar caixas de texto
    campos = [
        ("Pergunta", CaixaDeTexto(50, 50, 700, 40)),
        ("Alternativa A", CaixaDeTexto(50, 110, 700, 40)),
        ("Alternativa B", CaixaDeTexto(50, 170, 700, 40)),
        ("Alternativa C", CaixaDeTexto(50, 230, 700, 40)),
        ("Alternativa D", CaixaDeTexto(50, 290, 700, 40)),
        ("Resposta Correta", CaixaDeTexto(50, 350, 100, 40)),
        ("Dificuldade", CaixaDeTexto(50, 410, 200, 40)),
        ("Assunto", CaixaDeTexto(50, 470, 400, 40)),
    ]

    botao_salvar = pygame.Rect(50, 540, 150, 50)
    botao_cancelar = pygame.Rect(220, 540, 150, 50)

    rodando = True
    while rodando:
        tela.fill((30,30,30))

        # desenhar campos de texto
        for rotulo, caixa in campos:
            tela.blit(font.render(rotulo, True, (255,255,255)), (caixa.rect.x, caixa.rect.y-25))
            caixa.desenhar(tela)

        # desenhar botões
        pygame.draw.rect(tela, (0,200,0), botao_salvar)
        tela.blit(font.render("Salvar", True, (255,255,255)), (botao_salvar.x+30, botao_salvar.y+15))

        pygame.draw.rect(tela, (200,0,0), botao_cancelar)
        tela.blit(font.render("Cancelar", True, (255,255,255)), (botao_cancelar.x+20, botao_cancelar.y+15))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # tratar eventos de cada caixa
            for _, caixa in campos:
                caixa.tratar_evento(evento)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_salvar.collidepoint(evento.pos):
                    # salvar no banco de dados
                    conn = psycopg2.connect(
                        host="localhost",
                        database="postgres",
                        user="postgres",
                        password="yuuta123"
                    )
                    cursor = conn.cursor()
                    valores = [caixa.texto for _, caixa in campos]
                    cursor.execute("""
                        INSERT INTO quiz (pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d,
                        resposta_correta, dificuldade, assunto)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, valores)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    rodando = False

                elif botao_cancelar.collidepoint(evento.pos):
                    rodando = False
def excluir_pergunta():
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="yuuta123")
    cursor = conn.cursor()
    print("\n--- EXCLUIR PERGUNTA ---")
    cursor.execute("SELECT id, pergunta FROM quiz;")
    perguntas = cursor.fetchall()
    for p in perguntas:
        print(f"{p[0]} - {p[1]}")
    id_excluir = input("Digite o ID da pergunta que deseja excluir: ")
    cursor.execute("DELETE FROM quiz WHERE id = %s;", (id_excluir,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Pergunta removida!\n")

def editar_pergunta():
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="yuuta123")
    cursor = conn.cursor()
    print("\n--- EDITAR PERGUNTA ---")
    cursor.execute("SELECT id, pergunta FROM quiz;")
    perguntas = cursor.fetchall()
    for p in perguntas:
        print(f"{p[0]} - {p[1]}")
    id_editar = input("Digite o ID da pergunta que deseja editar: ")
    nova_pergunta = input("Nova pergunta: ")
    dificuldade = input("Nova dificuldade: ")
    assunto = input("Novo assunto: ")
    explicacao = input("Nova explicação: ")
    cursor.execute("""
    UPDATE quiz
    SET pergunta=%s, dificuldade=%s, assunto=%s, explicacao=%s
    WHERE id=%s
    """, (nova_pergunta, dificuldade, assunto, explicacao, id_editar))
    conn.commit()
    cursor.close()
    conn.close()
    print("Pergunta atualizada!\n")

#ESCOLHER ASSUNTO
def escolher_assunto():
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="yuuta123")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT assunto FROM quiz;")
    assuntos = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    while True:
        tela.fill((30,30,30))
        tela.blit(font.render("Escolha um assunto:", True, (255,255,255)), (50,50))
        botoes = []
        for i, assunto in enumerate(assuntos):
            ret = pygame.Rect(50, 150 + i*70, 700, 50)
            pygame.draw.rect(tela, (70,130,180), ret)
            tela.blit(font.render(assunto, True, (255,255,255)), (60,160+i*70))
            botoes.append((ret, assunto))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for ret, assunto in botoes:
                    if ret.collidepoint(event.pos):
                        return assunto
        clock.tick(60)

# ---------------------- BARRA DE PROGRESSO ----------------------
def desenhar_barra_progresso(atual, total):
    largura_total = 700
    altura = 25
    x, y = 50, 650
    largura = int(largura_total * (atual/total))
    pygame.draw.rect(tela, (80,80,80), (x,y,largura_total,altura))
    pygame.draw.rect(tela, (0,200,0), (x,y,largura,altura))
    tela.blit(font.render(f"{atual}/{total}", True, (255,255,255)), (x+310, y-30))

#EXPLICAÇÃO
def mostrar_explicacao(texto):
    while True:
        tela.fill((30,30,30))
        tela.blit(font.render("Você errou!", True, (255,80,80)), (50,50))
        tela.blit(font.render("Saiba mais:", True, (255,255,255)), (50,120))
        tela.blit(font.render(texto, True, (200,200,200)), (50,170))
        botao = pygame.Rect(50,260,200,50)
        pygame.draw.rect(tela,(70,130,180),botao)
        tela.blit(font.render("Continuar",True,(255,255,255)),(80,275))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(event.pos):
                    return

#FUNÇÃO PERGUNTA
def desenhar_pergunta(q):
    tela.fill((30,30,30))
    tela.blit(font.render(q[1], True, (255,255,255)), (50,50) if q[0] else (50,50))
    botoes = []

    if q[-1] == "vf":
        alternativas = [q[2], q[3]]  # V e F
        for i, alt in enumerate(alternativas):
            ret = pygame.Rect(50,150+i*70,700,50)
            pygame.draw.rect(tela,(70,130,180),ret)
            letra = "V" if i==0 else "F"
            tela.blit(font.render(f"{letra}) {alt}", True, (255,255,255)), (60,160+i*70))
            botoes.append(ret)
    else:
        for i, alt in enumerate(q[2:6]):
            ret = pygame.Rect(50,150+i*70,700,50)
            pygame.draw.rect(tela,(70,130,180),ret)
            tela.blit(font.render(f"{chr(65+i)}) {alt}", True, (255,255,255)), (60,160+i*70))
            botoes.append(ret)

    desenhar_barra_progresso(current, len(perguntas))
    return botoes
#LOOP PRINCIPAL
while True:
    escolha_menu = menu_principal()
    if escolha_menu == "Jogar":
        break
    elif escolha_menu == "Adicionar Pergunta":
        adicionar_pergunta_pygame()
    elif escolha_menu == "Editar Pergunta":
        editar_pergunta()
    elif escolha_menu == "Excluir Pergunta":
        excluir_pergunta()
    elif escolha_menu == "Sair":
        pygame.quit()
        sys.exit()

# Seleciona assunto
assunto_escolhido = escolher_assunto()

# Busca perguntas
conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="yuuta123")
cursor = conn.cursor()
cursor.execute("""
SELECT id, pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta, explicacao, tipo
FROM quiz
WHERE assunto = %s
ORDER BY RANDOM()
""", (assunto_escolhido,))
perguntas = cursor.fetchall()
cursor.close()
conn.close()

current = 0
score = 0

# Loop quiz
while True:
    if current >= len(perguntas):
        tela.fill((30,30,30))
        tela.blit(font.render(f"Quiz concluído! Pontuação: {score}/{len(perguntas)}", True, (255,255,255)), (150,200))
        botao_menu = pygame.Rect(250,350,300,60)
        pygame.draw.rect(tela,(70,130,180),botao_menu)
        tela.blit(font.render("Voltar ao Menu",True,(255,255,255)),(300,370))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and botao_menu.collidepoint(event.pos):
                current = score = 0
                escolha_menu = menu_principal()
                if escolha_menu == "Jogar":
                    assunto_escolhido = escolher_assunto()
                    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="yuuta123")
                    cursor = conn.cursor()
                    cursor.execute("""
                    SELECT id, pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta, explicacao, tipo
                    FROM quiz
                    WHERE assunto = %s
                    ORDER BY RANDOM()
                    """, (assunto_escolhido,))
                    perguntas = cursor.fetchall()
                    cursor.close()
                    conn.close()
        clock.tick(60)
        continue

    botoes = desenhar_pergunta(perguntas[current])
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, ret in enumerate(botoes):
                if ret.collidepoint(event.pos):
                    q = perguntas[current]
                    if q[-1] == "vf":
                        escolha = "V" if i==0 else "F"
                    else:
                        escolha = chr(65+i)
                    if escolha == q[6]:
                        score += 1
                    else:
                        mostrar_explicacao(q[7])
                    current += 1
                    pygame.time.wait(200)
    clock.tick(60)