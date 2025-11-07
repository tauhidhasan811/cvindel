from asset.database_manage.userRepo import insert_user

def register(user_info):
    #id = insert_user(user_info)

    #return f'registered user {id} successfully'
    data = insert_user(user_info)
    return data