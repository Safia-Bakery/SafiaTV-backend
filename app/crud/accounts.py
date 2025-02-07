from sqlalchemy.orm import Session
from app.models.Accounts import Accounts
from app.utils.utils import hash_password



def create_account(db:Session, password, role_id, accountgroup_id):
    query = Accounts(
        password=password,
        role_id=role_id,
        accountgroup_id=accountgroup_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_account_by_password(db:Session, password):
    query = db.query(Accounts).filter(Accounts.password == password).first()
    return query


def get_account_list(db:Session):
    query = db.query(Accounts).all()
    return  query



# def create_client(db:Session,username,full_name):
#     query = Accounts(username=username,full_name=full_name)
#     db.add(query)
#     db.commit()
#     db.refresh(query)
#     return query