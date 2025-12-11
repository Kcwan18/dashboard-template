from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User, ScoreEvent

def init_routes(app):
    """Initialize all application routes"""
    
    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            
            if not user:
                # Auto-register for simplicity if user doesn't exist
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('dashboard'))
                
            if user.password == password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Please check your login details and try again.')
                
        return render_template('login.html')

    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        if request.method == 'POST':
            url = request.form.get('url')
            api_url = request.form.get('api_url')
            
            if url is not None:
                current_user.url = url
            if api_url is not None:
                current_user.api_url = api_url
                
            db.session.commit()
            flash('URLs updated successfully!')
        return render_template('dashboard.html', user=current_user)

    @app.route('/score-history')
    @login_required
    def score_history():
        events = ScoreEvent.query.filter_by(user_id=current_user.id).order_by(ScoreEvent.timestamp.desc()).all()
        return render_template('score_history.html', events=events)

    @app.route('/leaderboard')
    def leaderboard():
        users = User.query.order_by(User.score.desc()).all()
        return render_template('leaderboard.html', users=users)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
