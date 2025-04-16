from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['STATIC_FOLDER'] = 'static'
app.config['DEBUG'] = True

print("Démarrage de l'application...")

# Configuration des emojis
app.jinja_env.globals.update(
    add_emoji="✅ ",  # Emoji pour l'ajout d'une tâche
    delete_emoji="🗑️ ",  # Emoji pour la suppression
    update_emoji="📝 ",  # Emoji pour la modification
    task_emoji="📋 ",  # Emoji pour les tâches listées
    status_todo="📝",      # Pour les tâches à faire
    status_progress="🔄",  # Pour les tâches en cours
    status_done="✅"       # Pour les tâches terminées
)

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='à faire')  # 'à faire', 'en cours', 'terminé'

# Création du dossier static s'il n'existe pas
if not os.path.exists('static'):
    os.makedirs('static')
    print("Dossier static créé")

@app.route('/', methods=['POST', 'GET'])
def index():
    print("Accès à la page d'accueil")
    theme = request.cookies.get('theme', 'light-theme')
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            print(f"Nouvelle tâche ajoutée : {task_content}")
            return redirect('/')
        except Exception as e:
            print(f"Erreur lors de l'ajout de la tâche : {str(e)}")
            return 'Une erreur est survenue'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, theme=theme)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Une erreur est survenue'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    theme = request.cookies.get('theme', 'light-theme')
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Une erreur est survenue'
    else:
        return render_template('update.html', task=task, theme=theme)

@app.route('/change_status/<int:id>', methods=['POST'])
def change_status(id):
    task = Todo.query.get_or_404(id)
    new_status = request.form['status']
    if new_status in ['à faire', 'en cours', 'terminé']:
        task.status = new_status
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Une erreur est survenue lors du changement de statut'
    return 'Statut invalide'

@app.route('/filter/<status>')
def filter_tasks(status):
    theme = request.cookies.get('theme', 'light-theme')
    if status == 'all':
        tasks = Todo.query.order_by(Todo.date_created).all()
    else:
        tasks = Todo.query.filter_by(status=status).order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks, theme=theme)

@app.route('/search', methods=['GET'])
def search_tasks():
    theme = request.cookies.get('theme', 'light-theme')
    query = request.args.get('query', '')
    tasks = Todo.query.filter(Todo.content.contains(query)).all()
    return render_template('index.html', tasks=tasks, theme=theme)

@app.route('/sort/<criteria>')
def sort_tasks(criteria):
    theme = request.cookies.get('theme', 'light-theme')
    if criteria == 'date':
        tasks = Todo.query.order_by(Todo.date_created).all()
    elif criteria == 'status':
        tasks = Todo.query.order_by(Todo.status).all()
    else:
        tasks = Todo.query.order_by(Todo.content).all()
    return render_template('index.html', tasks=tasks, theme=theme)

@app.route('/stats')
def get_stats():
    theme = request.cookies.get('theme', 'light-theme')
    total_tasks = Todo.query.count()
    todo_tasks = Todo.query.filter_by(status='à faire').count()
    in_progress_tasks = Todo.query.filter_by(status='en cours').count()
    done_tasks = Todo.query.filter_by(status='terminé').count()
    
    stats = {
        'total': total_tasks,
        'todo': todo_tasks,
        'in_progress': in_progress_tasks,
        'done': done_tasks
    }
    return render_template('stats.html', stats=stats, theme=theme)

@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    current_theme = request.cookies.get('theme', 'light-theme')
    new_theme = 'dark-theme' if current_theme == 'light-theme' else 'light-theme'
    
    response = make_response(redirect(request.referrer or url_for('index')))
    response.set_cookie('theme', new_theme)
    return response

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    with app.app_context():
        db.create_all()
        print("Base de données créée avec succès")
    
    print("Démarrage du serveur sur le port 8080...")
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8080)
