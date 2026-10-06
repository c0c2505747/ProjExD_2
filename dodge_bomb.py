import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) ->tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾のRect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  #横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  #縦方向判定
        tate = False
    return yoko,tate


def gameover(screen: pg.Surface) -> None:  # 演習1：ゲームオーバー画面
    """
    引数：Surface
    戻り値：なし
    ゲームオーバー画面の設定
    """
    blackout = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(blackout, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))  # 黒の画面の作成

    blackout.set_alpha(180)  # 透明度の設定

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH//2, HEIGHT//2)
    blackout.blit(txt, txt_rct)  # 白文字GameOverの表示

    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,1)
    kk_img3 = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,1)
    kk_img2_rct = kk_img2.get_rect()
    kk_img2_rct.center = (WIDTH//4, HEIGHT//2)
    kk_img3_rct = kk_img3.get_rect()
    kk_img3_rct.center = (WIDTH//4*3, HEIGHT//2)
    blackout.blit(kk_img2, kk_img2_rct)
    blackout.blit(kk_img3, kk_img3_rct)  # こうかとんの表示

    screen.blit(blackout, [0,0])
    pg.display.update()
    time.sleep(5)  # 5秒間暗い画面のまま


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:  # 演習2：時間とともに爆弾が拡大,加速する
    """
    引数：なし
    戻り値：爆弾の大きさリストのタプル,加速度リストのタプル
    """
    bb_imgs = []
    for r in range(1, 11):  # 爆弾の大きさのリスト
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]  # 爆弾の加速度のリスト
    return tuple(bb_imgs),tuple(bb_accs)
     



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  #空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  #練習2：四隅の黒い部分を透過
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  #横座標の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  #縦座標の乱数
    vx, vy = +5, +5  #練習2：爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    imgs, accs = init_bb_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        avx = vx*accs[min(tmr//500, 9)]
        avy = vy*accs[min(tmr//500, 9)]
        bb_img = imgs[min(tmr//500, 9)]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height  # 演習2：時間とともに爆弾が拡大,加速する　の実装
            
        if kk_rct.colliderect(bb_rct):  #練習4：kkとbbのrectが重なっていたら
            print("Game Over")
            gameover(screen)
            return(screen)

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向移動量
                sum_mv[1] += tpl[1]  # 縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #練習3：どこかしらはみ出ているならば
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #先ほどの動きをキャンセルする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)  #練習2：爆弾が動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  #練習2：爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

# コメントアウト
"""
複数行コメントアウト
"""
