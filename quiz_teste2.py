import psycopg2
import pygame
import sys


# banco
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
    alternativa_c TEXT NOT NULL,
    alternativa_d TEXT NOT NULL,
    resposta_correta CHAR(1) NOT NULL,
    dificuldade VARCHAR(20),
    assunto VARCHAR(50)
);
""")

cursor.execute("""
ALTER TABLE quiz
ADD COLUMN IF NOT EXISTS explicacao TEXT;
""")
conn.commit()

# Inserção de dados (uma única vez)
cursor.executemany("""
INSERT INTO quiz 
(pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta, dificuldade, assunto)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (pergunta) DO NOTHING;
""", [
    ("A Zona Bioclimática A4 é caracterizada por:", "Clima frio e úmido", "Clima quente e seco", "Clima quente e úmido", "Clima temperado", "C", "Fácil", "Clima e Temperatura"),
    ("Na Zona A4, a estratégia principal de conforto térmico é:", "Aquecimento artificial", "Ventilação natural e sombreamento", "Uso de lareiras", "Fechamento total das aberturas", "B", "Médio", "Conforto Térmico"),
("O uso de brises na Zona A4 tem como objetivo:",
 "Aumentar o calor interno",
 "Controlar radiação solar direta",
 "Reduzir ventilação",
 "Aumentar umidade interna",
 "B",
 "Fácil",
 "Conforto Térmico"),

("Materiais recomendados para Zona A4 geralmente possuem:",
 "Alta inércia térmica",
 "Baixo isolamento térmico",
 "Alta condutividade térmica",
 "Estrutura metálica leve",
 "A",
 "Difícil",
 "Materiais e Construção"),

("Na Zona A4, as edificações devem priorizar:",
 "Ambientes totalmente fechados",
 "Grandes áreas envidraçadas sem proteção",
 "Ventilação cruzada",
 "Ausência de aberturas",
 "C",
 "Médio",
 "Ventilação e Ventos"),

("Qual estratégia ajuda a reduzir o uso de ar-condicionado em edificações da Zona A4?",
 "Pintura de paredes externas com cores claras",
 "Aumentar o tamanho das janelas sem proteção",
 "Instalar lareiras internas",
 "Fechar todas as portas e janelas",
 "A",
 "Fácil",
 "Conforto Térmico"),

("Para manter temperatura agradável durante o dia, qual recurso é mais eficiente?",
 "Brises orientados corretamente",
 "Uso de tapetes internos",
 "Paredes de vidro sem proteção",
 "Telhados escuros",
 "A",
 "Médio",
 "Conforto Térmico"),

("Em construções da Zona A4, materiais com alta massa térmica servem para:",
 "Acelerar aquecimento interno",
 "Armazenar calor do dia para liberar à noite",
 "Reduzir ventilação natural",
 "Aumentar a umidade",
 "B",
 "Fácil",
 "Materiais e Construção"),

("Qual material seria adequado para minimizar o calor interno em dias quentes?",
 "Concreto claro com isolamento",
 "Madeira sem tratamento",
 "Metais escuros",
 "Vidro sem proteção",
 "A",
 "Médio",
 "Materiais e Construção"),

("A disposição de janelas opostas em um cômodo permite:",
 "Evitar a entrada de vento",
 "Criar ventilação cruzada eficiente",
 "Aumentar ganho de calor",
 "Reduzir iluminação natural",
 "B",
 "Fácil",
 "Ventilação e Ventos"),

("Brises horizontais instalados na fachada servem para:",
 "Aumentar incidência direta de sol",
 "Proteger do vento predominante e controlar luz solar",
 "Evitar ventilação interna",
 "Criar sombras internas apenas à noite",
 "B",
 "Médio",
 "Ventilação e Ventos"),

("Durante períodos de chuva intensa na Zona A4, qual recurso ajuda a evitar umidade interna excessiva?",
 "Telhados inclinados com beirais",
 "Janelas fixas grandes",
 "Pisos de madeira sem tratamento",
 "Paredes de vidro sem proteção",
 "A",
 "Fácil",
 "Clima e Temperatura"),

("Qual fator climático é determinante para o conforto nas edificações da Zona A4?",
 "Direção predominante do vento e radiação solar",
 "Presença de rios próximos",
 "Tipo de solo",
 "Quantidade de árvores na rua",
 "A",
 "Médio",
 "Clima e Temperatura"),

("A ventilação cruzada em edifícios da Zona A4 serve para:",
 "Reduzir ventilação",
 "Aumentar circulação de ar e conforto térmico",
 "Bloquear vento frio",
 "Aumentar umidade interna",
 "B",
 "Fácil",
 "Ventilação e Ventos"),

("O uso de isolamento térmico em paredes externas tem como objetivo:",
 "Aumentar calor interno",
 "Reduzir transferência de calor",
 "Bloquear a luz natural",
 "Reduzir ventilação natural",
 "B",
 "Médio",
 "Materiais e Construção"),

("Brises verticais instalados nas janelas são usados para:",
 "Aumentar incidência direta de sol",
 "Bloquear vento e controlar luz lateral",
 "Aumentar ventilação",
 "Melhorar isolamento acústico",
 "B",
 "Fácil",
 "Conforto Térmico"),

("Telhados claros em edificações da Zona A4 ajudam a:",
 "Aumentar absorção de calor",
 "Refletir radiação solar e reduzir calor interno",
 "Melhorar a ventilação",
 "Reduzir a luz natural",
 "B",
 "Médio",
 "Clima e Temperatura"),

("Paredes com alta inércia térmica servem para:",
 "Liberar calor rapidamente",
 "Armazenar calor do dia para liberar à noite",
 "Evitar ventilação",
 "Aumentar ganho de umidade",
 "B",
 "Difícil",
 "Materiais e Construção"),

("Janelas com sombreamento adequado têm como função:",
 "Bloquear ventilação",
 "Reduzir radiação solar direta e aquecimento interno",
 "Aumentar entrada de luz e calor",
 "Evitar circulação de ar",
 "B",
 "Fácil",
 "Conforto Térmico")

])

conn.commit()

cursor.execute("SELECT DISTINCT assunto FROM quiz;")
assuntos = [row[0] for row in cursor.fetchall()]

# -pygame
pygame.init()
tela = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Quiz Zona A4")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

#menu principal e funcoes da pergunta

def menu_principal():
    opcoes = ["Jogar", "Adicionar Pergunta", "Editar Pergunta", "Excluir Pergunta", "Sair"]

    while True:
        tela.fill((30, 30, 30))
        tela.blit(font.render("MENU PRINCIPAL", True, (255,255,255)), (300, 80))

        botoes = []
        for i, op in enumerate(opcoes):
            ret = pygame.Rect(200, 180 + i * 70, 400, 50)
            pygame.draw.rect(tela, (70,130,180), ret)
            tela.blit(font.render(op, True, (255,255,255)), (320, 195 + i * 70))
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

def adicionar_pergunta():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="yuuta123"
    )
    cursor = conn.cursor()

    print("\n--- ADICIONAR PERGUNTA ---")
    pergunta = input("Pergunta: ")
    a = input("Alternativa A: ")
    b = input("Alternativa B: ")
    c = input("Alternativa C: ")
    d = input("Alternativa D: ")
    correta=''
    while correta not in ["A","B","C","D"]:
        correta = input("Digite apenas A, B, C ou D: ").upper()
    dificuldade = input("Dificuldade: ")
    assunto = input("Assunto: ")

    cursor.execute("""
        INSERT INTO quiz 
        (pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta, dificuldade, assunto)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (pergunta, a, b, c, d, correta, dificuldade, assunto))

    conn.commit()
    cursor.close()
    conn.close()

    print("Pergunta adicionada com sucesso!\n")


def excluir_pergunta():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="yuuta123"
    )
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
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="yuuta123"
    )
    cursor = conn.cursor()

    print("\n--- EDITAR PERGUNTA ---")

    cursor.execute("SELECT id, pergunta FROM quiz;")
    perguntas = cursor.fetchall()

    for p in perguntas:
        print(f"{p[0]} - {p[1]}")

    id_editar = input("Digite o ID da pergunta que deseja editar: ")

    nova_pergunta = input("Nova pergunta: ")

    cursor.execute("""
    UPDATE quiz
    SET pergunta=%s,
    alternativa_a=%s,
    alternativa_b=%s,
    alternativa_c=%s,
    alternativa_d=%s,
    resposta_correta=%s,
    dificuldade=%s,
    assunto=%s
    WHERE id=%s
    """, (...))
    conn.commit()
    cursor.close()
    conn.close()

    print("Pergunta atualizada!\n")

def desenhar_barra_progresso(atual, total):
    largura_total = 700
    altura = 25
    x = 50
    y = 650

    progresso = atual / total
    largura = int(largura_total * progresso)

    # fundo
    pygame.draw.rect(tela, (80,80,80), (x, y, largura_total, altura))

    # progresso
    pygame.draw.rect(tela, (0,200,0), (x, y, largura, altura))

    # texto
    texto = font.render(f"{atual}/{total}", True, (255,255,255))
    tela.blit(texto, (x + 310, y - 30))



def mostrar_explicacao(texto):

    while True:

        tela.fill((30,30,30))

        titulo = font.render("Você errou!", True, (255,80,80))
        tela.blit(titulo,(50,50))

        saiba = font.render("Saiba mais:", True, (255,255,255))
        tela.blit(saiba,(50,120))

        explicacao = font.render(texto, True, (200,200,200))
        tela.blit(explicacao,(50,170))

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
def escolher_assunto():

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="yuuta123"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT assunto FROM quiz;")
    assuntos = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    while True:
        tela.fill((30, 30, 30))
        tela.blit(font.render("Escolha um assunto:", True, (255, 255, 255)), (50, 50))

        botoes = []
        for i, assunto in enumerate(assuntos):
            ret = pygame.Rect(50, 150 + i * 70, 700, 50)
            pygame.draw.rect(tela, (70, 130, 180), ret)
            tela.blit(font.render(assunto, True, (255, 255, 255)), (60, 160 + i * 70))
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

while True:
    escolha_menu = menu_principal()

    if escolha_menu == "Jogar":
        break

    elif escolha_menu == "Adicionar Pergunta":
        adicionar_pergunta()

    elif escolha_menu == "Editar Pergunta":
        editar_pergunta()

    elif escolha_menu == "Excluir Pergunta":
        excluir_pergunta()

    elif escolha_menu == "Sair":
        pygame.quit()
        sys.exit()

assunto_escolhido = escolher_assunto()

#buscar perguntas
cursor.execute("""
SELECT pergunta, alternativa_a, alternativa_b, alternativa_c,
       alternativa_d, resposta_correta, explicacao
FROM quiz
WHERE assunto = %s
ORDER BY RANDOM()
""", (assunto_escolhido,))
perguntas = cursor.fetchall()

cursor.close()
conn.close()

#quiz
current = 0
score = 0

def desenhar_pergunta(q):


    tela.fill((30,30,30))
    tela.blit(font.render(q[0], True, (255,255,255)), (50,50))

    botoes = []
    for i, alt in enumerate(q[1:5]):
            ret = pygame.Rect(50,150+i*70,700,50)
            pygame.draw.rect(tela,(70,130,180),ret)
            tela.blit(font.render(f"{chr(65+i)}) {alt}",True,(255,255,255)),(60,160+i*70))
            botoes.append(ret)
    desenhar_barra_progresso(current, len(perguntas))
    return botoes

rodando = True

while True:

    if current >= len(perguntas):

        tela.fill((30,30,30))
        tela.blit(
            font.render(
                f"Quiz concluído! Pontuação: {score}/{len(perguntas)}",
                True,
                (255,255,255)
            ),
            (150,200)
        )

        botao_menu = pygame.Rect(250,350,300,60)
        pygame.draw.rect(tela,(70,130,180),botao_menu)
        tela.blit(font.render("Voltar ao Menu",True,(255,255,255)),(300,370))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_menu.collidepoint(event.pos):

                    # volta pro menu
                    current = 0
                    score = 0

                    escolha_menu = menu_principal()

                    if escolha_menu == "Jogar":
                        assunto_escolhido = escolher_assunto()

                        conn = psycopg2.connect(
                            host="localhost",
                            database="postgres",
                            user="postgres",
                            password="yuuta123"
                        )
                        cursor = conn.cursor()

                        cursor.execute("""
                        SELECT pergunta, alternativa_a, alternativa_b, alternativa_c,
                               alternativa_d, resposta_correta,explicacao
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

                    escolha = chr(65 + i)

                    if escolha == perguntas[current][5]:
                        score += 1
                    else:
                        mostrar_explicacao(perguntas[current][6])

                    current += 1
                    pygame.time.wait(200)

    clock.tick(60)


