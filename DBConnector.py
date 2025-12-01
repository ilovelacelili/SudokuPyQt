# Connect to a SQLite database (or create it if it doesn't exist)
import sqlite3

class DBConnector:
    def __init__(self):
        self.conn = sqlite3.connect('sudoku.db')
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                puzzle TEXT NOT NULL,
                                steps TEXT NOT NULL,
                                time INTEGER NOT NULL,
                                difficulty TEXT NOT NULL
                              )''')
        self.conn.commit()

    def guardar_juego(self, name, puzzle, steps, time, difficulty):
        """Saves a Sudoku puzzle to the database."""
        puzzle_str = ','.join(str(num) for row in puzzle for num in row)
        self.cursor.execute('INSERT INTO games (name, puzzle, steps, time, difficulty) VALUES (?, ?, ?, ?, ?)', (name, puzzle_str, steps, time, difficulty))
        self.conn.commit()

    def cargar_juegos(self, difficulty):
        """Loads all games of a given difficulty from the database."""
        self.cursor.execute('SELECT name, puzzle, steps, time FROM games WHERE difficulty = ? ORDER BY time', (difficulty,))
        rows = self.cursor.fetchall()
        games = []
        for name, puzzle_str, steps, time in rows:
            puzzle = []
            nums = list(map(int, puzzle_str.split(',')))
            for i in range(9):
                puzzle.append(nums[i*9:(i+1)*9])
            games.append((name, puzzle, steps, time))

        return games

    def close(self):
        """Closes the database connection."""
        self.conn.close()