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


def file_reader(file_name: str = '1.map') -> tp.Tuple[tp.List[tp.List[int], tp.Tuple[int, int]]]:
    game_map: tp.List[tp.List[int]] = []
    start_pos = (0, 0)
    with open(file_name) as f:
        for ind_line, line in enumerate(map(lambda s: s.split(), f.readlines())):
            game_map.append([])
            for ind_col, char in enumerate(line):
                game_map[-1].append(CONFORMITY_TABLE[char])
                if CONFORMITY_TABLE[char] == 1:
                    start_pos = (ind_line, ind_col)
    return game_map


def solve(game_map: tp.List[tp.List[int]], start_pos: tp.Tuple[int, int]):
    que = [start_pos]
    map_of_min_vals = {start_pos: 0}
    map_to_relax = {start_pos: start_pos}
    while que:
        curr_checking_pos = que.pop()
        for k in range(-1, 2):
            for o in range(-1, 2):
                try:
                    i, j = curr_checking_pos[0] - k, curr_checking_pos[1] - o
                    if game_map[i][j] == 3:
                        map_of_min_vals.setdefault((i, j), map_of_min_vals[curr_checking_pos] + 1)
                        if map_of_min_vals[curr_checking_pos] + 1 <= map_of_min_vals[(i, j)]:
                            map_of_min_vals[(i, j)] = curr_checking_pos + 1
                            map_to_relax

                        que.append((i, j))
                    if
                except IndexError:
                    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='For exam-winter')
    parser.add_argument('file_name', help='Path to file', type=str)
    args = parser.parse_args()
    solve(*file_reader(args.file_name))
