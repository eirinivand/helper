1. docker-compose up --build -d

{or
1.a. docker-compose build
1.b. docker-compose up -d
}

and

2. docker-compose run web /usr/local/bin/python create_db.py