import typing as tp
import argparse

CONFORMITY_TABLE = {
    ' ': -1,
    '☒': 0,
    '☺': 1,
    '☼': 2,
    '.': 3
}
CONFORMITY_TABLE_REVERSE = {
    -1: ' ',
    0: '☒',
    1: '☺',
    2: '☼',
    3: '.'
}


def file_reader(file_name: str = '1.map') -> tp.Tuple[tp.List[tp.List[int]], tp.Tuple[int, int]]:
    game_map: tp.List[tp.List[int]] = []
    start_pos = (0, 0)
    with open(file_name) as f:
        for ind_line, line in enumerate(map(lambda s: s.strip(), f.readlines())):
            game_map.append([])
            for ind_col, char in enumerate(line):
                game_map[-1].append(CONFORMITY_TABLE[char])
                if CONFORMITY_TABLE[char] == 1:
                    start_pos = (ind_line, ind_col)
    return game_map, start_pos


def relax_and_print(game_map: tp.List[tp.List[int]], map_to_relax: tp.Dict[tp.Tuple[int, int], tp.Tuple[int, int]],
                    start_pos: tp.Tuple[int, int], end_pos: tp.Tuple[int, int]):
    curr_pos = map_to_relax[end_pos]
    while curr_pos != start_pos:
        game_map[curr_pos[0]][curr_pos[1]] = 1
        curr_pos = map_to_relax[curr_pos]
    for i in game_map:
        print(''.join(map(lambda x: CONFORMITY_TABLE_REVERSE[x], i)))


def solve(game_map: tp.List[tp.List[int]], start_pos: tp.Tuple[int, int]):
    que = [start_pos]
    map_to_relax = {start_pos: start_pos}
    while que:
        curr_checking_pos = que.pop(0)
        for k in range(-1, 2):
            for o in range(-1, 2):
                if k != 0 and o != 0:
                    continue
                if curr_checking_pos[0] - k < 0 or curr_checking_pos[1] - o < 0:
                    continue
                try:
                    i, j = curr_checking_pos[0] - k, curr_checking_pos[1] - o
                    if game_map[i][j] == 3:
                        if not (i, j) in map_to_relax:
                            map_to_relax.update({(i, j): curr_checking_pos})
                            que.append((i, j))
                    if game_map[i][j] == 2:
                        map_to_relax.update({(i, j): curr_checking_pos})
                        relax_and_print(game_map, map_to_relax, start_pos, (i, j))
                        return
                except IndexError:
                    pass
    for i in game_map:
        print(''.join(map(lambda x: CONFORMITY_TABLE_REVERSE[x], i)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='For exam-winter')
    parser.add_argument('file_name', help='Path to file', type=str)
    args = parser.parse_args()
    solve(*file_reader(args.file_name))
