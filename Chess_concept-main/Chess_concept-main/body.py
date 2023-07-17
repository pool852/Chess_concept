import chess
import chess.engine

# Создаем экземпляр движка Stockfish
engine = chess.engine.SimpleEngine.popen_uci('C:\\Users\dania\Downloads\stockfish_15.1_win_x64_popcnt')

# Создаем доску
board = chess.Board()

# Определяем, кто играет первым
human_color = input("Выберите цвет: 'w' для белых, 'b' для черных: ")
if human_color == 'w':
    is_human_turn = True
else:
    is_human_turn = False

# Играем до конца игры
while not board.is_game_over():
    if is_human_turn:
        print("Ход человека:")
        move_str = input("Введите свой ход (например, e2e4): ")
        move = chess.Move.from_uci(move_str)

        # Проверяем, является ли ход допустимым
        if move in board.legal_moves:
            board.push(move)
            is_human_turn = False
        else:
            print("Недопустимый ход. Попробуйте еще раз.")
            continue
    else:
        print("Ход компьютера:")
        result = engine.play(board, chess.engine.Limit(time=2.0))
        board.push(result.move)
        is_human_turn = True

# Выводим результат игры
print("Игра окончена. Результат:", board.result())