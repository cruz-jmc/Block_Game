import pygame

# 1. CORREÇÃO: Inicialização correta do módulo
pygame.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 100
jogador = pygame.Rect(350, 750, tamanho_jogador, 15) # Começa no meio (X=350)

quantidade_blocos_linha = 8
quantidade_linhas_blocos = 5
quantidade_total_blocos = quantidade_blocos_linha * quantidade_linhas_blocos

def criar_blocos(quantidade_blocos_linha, quantidade_linhas_blocos):
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / quantidade_blocos_linha - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = []
    for linha in range(quantidade_linhas_blocos):
        # 2. CORREÇÃO: Usando 'i' no loop para o cálculo do X não quebrar
        for i in range(quantidade_blocos_linha):
            novo_bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), 50 + linha * distancia_entre_linhas, largura_bloco, altura_bloco)
            blocos.append(novo_bloco)
    return blocos

cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0)
}

fim_jogo = False
# 4. CORREÇÃO: Mudado o nome para evitar conflito com a função
velocidade_bola = [5, -5] 

def desenhar_inicio_jogo():
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

def movimentar_jogador(evento):
    if evento.type == pygame.KEYDOWN:
        # 5. OTIMIZAÇÃO: Aumentado o passo de 5 para 30 para o jogador responder rápido
        if evento.key == pygame.K_RIGHT:
            if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
                jogador.x = jogador.x + 50
        if evento.key == pygame.K_LEFT:
            if jogador.x > 0:
                jogador.x = jogador.x - 50

def movimentar_bola(bola, blocos):
    movimento = velocidade_bola
    bola.x = bola.x + movimento[0]
    bola.y = bola.y + movimento[1]

    if bola.x <= 0 or bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = -movimento[0]

    if bola.y <= 0:
        movimento[1] = -movimento[1]

    # Se a bola cair no chão, o jogo acaba
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        return None

    # Colisão com o jogador
    if jogador.colliderect(bola):
        movimento[1] = -movimento[1]

    # Colisão com os blocos
    for bloco in blocos:
        if bloco.colliderect(bola):
            blocos.remove(bloco)
            movimento[1] = -movimento[1]
            break # Evita remover dois blocos no mesmo frame
            
    return movimento

def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuacao: {pontuacao}", True, cores["amarela"])
    tela.blit(texto, (10, 770))
    return pontuacao >= quantidade_total_blocos

blocos = criar_blocos(quantidade_blocos_linha, quantidade_linhas_blocos)

# Loop Principal
while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    fim_jogo = atualizar_pontuacao(quantidade_total_blocos - len(blocos))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True
        # 3. CORREÇÃO: Movimentação agora é checada a cada novo evento gerado
        movimentar_jogador(evento)
    
    velocidade_bola = movimentar_bola(bola, blocos)

    if not velocidade_bola:
        fim_jogo = True

    pygame.time.wait(10) # Controla a taxa de atualização do frame
    pygame.display.flip()

pygame.quit()