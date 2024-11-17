from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)',
                     (title, ingredients, instructions))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_recipe.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        
        conn.execute('UPDATE recipes SET title = ?, ingredients = ?, instructions = ? WHERE id = ?',
                     (title, ingredients, instructions, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete/<int:id>')
def delete_recipe(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)