# --- Banco de dados ---
import psycopg2
import pygame, sys

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="yuuta123"
)
cursor = conn.cursor()

#buscar asperguntas antes da interface pygame
cursor.execute("SELECT DISTINCT assunto FROM quiz;")
assuntos = [row[0] for row in cursor.fetchall()]

# --- Pygame ---
pygame.init()
tela = pygame.display.set_mode((800,700))
pygame.display.set_caption("Quiz Zona A4")
font = pygame.font.SysFont(None,28)
clock = pygame.time.Clock()

# Tela de escolha de assunto
def escolher_assunto():
    rodando = True
    while rodando:
        tela.fill((30,30,30))
        tela.blit(font.render("Escolha um assunto:", True, (255,255,255)), (50,50))
        botoes = []
        for i, assunto in enumerate(assuntos):
            ret = pygame.Rect(50, 150+i*70, 700, 50)
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

assunto_escolhido = escolher_assunto()

# pegar a pergunta do assunto inforrmado pelo usuario
cursor.execute("""
SELECT pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta
FROM quiz
WHERE assunto = %s
""", (assunto_escolhido,))
perguntas = cursor.fetchall()

# fechar o banco
cursor.close()
conn.close()

# loop(preciso consertar aqui )
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
    return botoes

rodando = True
while rodando:
    if current > len(perguntas):
        tela.fill((30,30,30))
        tela.blit(font.render(f"Quiz concluído! Pontuação: {score}/{len(perguntas)}", True, (255,255,255)), (50,200))
        pygame.display.flip()
        pygame.time.wait(5000)
        break

    botoes = desenhar_pergunta(perguntas[current])
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, ret in enumerate(botoes):
                if ret.collidepoint(event.pos):
                    escolha = chr(65+i)
                    if escolha == perguntas[current][5]:
                        score += 1
                    current += 1
    clock.tick(60)