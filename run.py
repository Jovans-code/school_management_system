from app import create_app, db
app = create_app()

if __name__ == 'main':
    with app.app_contex():
        db.create_all()
        print("Database tables created (or already exist)")
    app.run(debug=True)