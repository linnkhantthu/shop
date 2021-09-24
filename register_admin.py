from shop import db, bcrypt, create_app
from shop.user.models import User

app = create_app()

pass_code = input('Unlock passcode: ')
if pass_code == app.config.get('PASS_CODE'):
    username = input('Username: ')
    email = input('Email: ')
    password = input('Password: ')
    confirm_password = input("Confirm password: ")
    if username and email and password and confirm_password == password:
        with app.app_context():
            queried_user_by_username = User.query.filter_by(username=username).first()
            queried_user_by_email = User.query.filter_by(email=email).first()
        if queried_user_by_username:
            print("Username already exists.")
        elif queried_user_by_email:
            print("Email already exists.")
        else:
            hashed_password = bcrypt.generate_password_hash(password)
            print('- Hashed password')
            user = User(username=username, email=email, password=hashed_password, account_type='admin')
            print('- Collected data, ready to comitt')
            ready = input('Confirm to commit[y/n]: ')
            if ready == 'y':
                with app.app_context():
                    db.session.add(user)
                    db.session.commit()
                print("Operation successfully")
            else:
                print('Operation cancelled')
    else:
        print("All inputs can't be empty")
else:
    print("Passcode incorrect")



