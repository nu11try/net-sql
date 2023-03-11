from db import DataBase

if __name__ == "__main__":
    db = DataBase(database='test', login='', password='')

    db.create_db()

    db.create_client(
        f_name='Test',
        s_name='Testov',
        email='test@test.ru',
        phones=['880005553535', '890005555555']
    )

    print(db.search_client(f_name='Test'))

    client_id = db.create_client(
        f_name='Test2',
        s_name='Testov2',
        email='test2@test.ru'
    )

    db.add_phone(client_id=client_id, phones=['89705556446'])

    print(db.search_client(f_name='Test2'))

    client_id = db.create_client(
        f_name='Test3',
        s_name='Testov3',
        email='test3@test.ru',
        phones=['880005553535', '890005555555']
    )

    db.change_client(client_id=client_id, f_name='TEST3', email='TEST3@TEST.com', phones=['880005553535'])

    print(db.search_client(f_name='TEST3'))

    client_id = db.create_client(
        f_name='Test4',
        s_name='Testov4',
        email='test4@test.ru',
        phones=['880005553535', '890005555555']
    )

    db.delete_phone(client_id=client_id, phones=['880005553535'])

    print(db.search_client(f_name='Test4'))

    client_id = db.create_client(
        f_name='Test5',
        s_name='Testov5',
        email='test5@test.ru',
        phones=['880005553535', '890005555555']
    )

    db.delete_client(client_id=client_id)

    print(db.search_client(f_name='Test5'))
