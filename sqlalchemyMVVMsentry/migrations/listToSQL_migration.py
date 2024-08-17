userDrop = "DROP TABLE users"
userTable = """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email VARCHAR NOT NULL UNIQUE,
                username VARCHAR DEFAULT '',
                password VARCHAR NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                verifymail VARCHAR DEFAULT 'true',
                create_at TIMESTAMP DEFAULT NOW(),
                update_at TIMESTAMP DEFAULT NOW()
            );
            """
