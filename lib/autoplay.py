def bgm_val(sec,starcnt,TIME):
    sec -= TIME.MOVEMOUSE * starcnt + TIME.FADE * 2 * starcnt
    sec /= starcnt
    if sec > 4 or sec < 1:
        return -1,0
    return 5 - sec - 1 / sec,sec