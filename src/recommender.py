import pandas as pd

GAME_DATA = "./data/game_list.tsv"

def get_column_set(column):
    """指定したcolumnの要素の集合を取得する

    Args:
        column (str):target column of DataFrame

    Returns:
        list: set of column

    """
    rows = pd.read_csv(GAME_DATA, sep="\t")[column].dropna()
    # rows = rows.map(lambda line: line.split(' '))
    rows = rows.map(lambda line: line.split(' ')).to_list()
    return list(set(sum(rows, [])))

def get_tag_list():
    return get_column_set("mechanism")

def get_artist_list():
    return get_column_set("artists")


def pickup_games(name:str, players:int, best_players:int, mechanism:str, premium:int, n=1):
    """n件のランダムなゲームを取得します。

    Args:
        name: part of game title
        players: number of players
        best_players: number of best players
        machanism: tag of game mechanism
        prenium: limited game or free（free:0, premium:1）

    Returns:
        DataFrame: rows of randomly recommended games

    """
    df = pd.read_csv(GAME_DATA, sep="\t")
    df = filter_games(df, name, players, best_players, mechanism, premium)
    return df.sample(n=n)

def filter_games(df, name:str, players:int, best_players:int, mechanism:str, premium:int):
    if name:
        df = df.dropna()
        df = df[df['name'].str.contains(name)]
    if players and players.isdigit():
        df = df[df['players'].str.contains(players)]
    if best_players and best_players.isdigit():
        df = df[df['best_players'].str.contains(best_players)]
    if mechanism:
        df = df.dropna()
        df = df[df['mechanism'].str.contains(mechanism)]
    if premium and premium.isdigit():
        df = df[df['premium'] == int(premium)]
    
    return df

# if __name__=="__main__":

#     pd.set_option('display.max_rows', 200)
#     # print(len(get_tag_list()))
#     # print(len(get_artist_list()))

#     params = {
#         'name':'',
#         'players':'',
#         'best_players':'4',
#         'mechanism':'',
#         'premium':'1',
#     }
#     print([pickup_games(**params).values])