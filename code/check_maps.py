def check_maps(maps:dict,qnt):
    playable = 0
    for i in range(qnt):
        map = maps[f"map_{i}"]

        if (map[9][0] or map[10][0]) == 1:
            print(f"map_{i} = PLAY")
            playable += 1
        else:
            print((f"map_{i} = UN"))

    print(f"Playable: ({playable}/{qnt}) = {(playable/qnt*100)}%",)