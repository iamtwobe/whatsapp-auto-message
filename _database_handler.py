import sqlite3

class AppDatabase():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Cria a tabela contacts se ela não existir
        self.create_contacts_table()

        # Cria a tabela text_models se ela não existir
        self.create_models_table()

        # Adiciona CONSTRAINTs após a criação das tabelas
        self.add_constraints()
        
        self.conn.commit()

    def create_contacts_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS contacts (
                contact_id      INTEGER             PRIMARY KEY AUTOINCREMENT,
                contact_name    VARCHAR(42)         NOT NULL,
                contact_number  VARCHAR(18)         NOT NULL,
                contact_email   VARCHAR(40)         NULL

            )
            """
        )
    
    def create_models_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS text_models(
                text_id         INTEGER             PRIMARY KEY AUTOINCREMENT,
                text_name       VARCHAR(50)         NULL,
                model_text      TEXT                NOT NULL
            )
            """
        )
    
    def add_constraints(self):
        self.cursor.execute(
            """
                CREATE UNIQUE INDEX IF NOT EXISTS contact_number_un_idx ON contacts (contact_number);
            """
        )
        self.cursor.execute(
            """
                CREATE UNIQUE INDEX IF NOT EXISTS text_name_un_idx ON text_models (text_name)
            """
        )
        self.conn.commit()

    def insert_contact(self, name: str=None, number: str=None, email: str=None) -> None:
        if not number:
            return "Missing number"
        if not name:
            return "Missing name"
        
        try:
            self.cursor.execute("INSERT INTO contacts (contact_name, contact_number, contact_email) VALUES (?, ?, ?)", (name, number, email))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return print("Contact already exists")

    def get_contact(self, name: str=None, number: str=None) -> any:
        if number:
            self.cursor.execute("SELECT * FROM contacts WHERE contact_number=?", (number,))
            selection = self.cursor.fetchone()
            return self.verify_db(selection)
        elif name:
            self.cursor.execute("SELECT * FROM contacts WHERE contact_name=?", (name,))
            selection = self.cursor.fetchone()
            return self.verify_db(selection)

        return "Missing infos"
    
    def get_all_table(self, table) -> list:
        table_data = self.cursor.execute(f"SELECT * FROM {table}")
        selection = table_data.fetchall()
        return self.verify_db(selection)
    
    def verify_db(self, selection) -> dict:
        if selection:
            # Se for mais que um item
            if type(selection) is list:
                results = []
                for i in selection:
                    column_names = [description[0] for description in self.cursor.description]
                    result = dict(zip(column_names, i))
                    results.append(result)
                return results
            # Se for apenas um item
            column_names = [description[0] for description in self.cursor.description]
            result = dict(zip(column_names, selection))
            return result
        else:
            return None

    def close(self):
        self.conn.close()
        
    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    # Abre o banco de dados
    db = AppDatabase("test_database.db")
    # # Insere um contato
    # db.insert_contact(name="Teste", number="+55 18 23805205")
    # # Busca um contato
    # print(db.get_contact("Teste"))
    # print(db.get_all_table(table='text_models'))

    contatos = db.get_all_table(table='contacts')

    #texto = main_text_box.get('1.0', 'end-1c')


        

    # Fecha
    db.close()