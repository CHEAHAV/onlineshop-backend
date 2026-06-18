from core.db import engine
from core.model import Base
from api.role.models import TBL_ROLE
from api.user.models import TBL_USER
from core.db import db
import core.lib as core_lib
# from core.security import get_password_hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

def generate_admin_role():
    role_obj = db.query(TBL_ROLE).filter(TBL_ROLE.id=='ADMIN').first()
    if not role_obj:
        print('create role')
        role_obj = TBL_ROLE(
            id           = 'ADMIN',
            name         = 'Administrator',
            name_lc      = 'Administrator',
            description  = 'Administrator Role with all permissions',
            is_superuser = False,
            branch_id    = 'HQ',
            company_id   = 'SYSTEM',
            re_is_public = False
        )
        db.add(role_obj)

    module_obj = db.query(TBL_MODULE).all()
    count = 1
    for m in module_obj:
        role_permission_obj = db.query(TBL_ROLE_MODULE).filter(
            TBL_ROLE_MODULE.parent_id == 'ADMIN',
            TBL_ROLE_MODULE.module_id == m.id
        ).first()
        if not role_permission_obj:
            count = count + 1
            role_permission_obj = TBL_ROLE_MODULE(
                id           = f'{count}_ADMIN',
                parent_id    = 'ADMIN',
                module_id    = m.id,
                permission   = 'ALL',
                branch_id    = 'HQ',
                company_id   = 'SYSTEM',
                re_is_public = False
            )
            db.add(role_permission_obj)

    db.add(role_obj)
    # db.commit()


def create_user_and_role():
    r_obj = db.query(TBL_ROLE).filter(TBL_ROLE.id == 'SUPERUSER').first()
    u_obj = db.query(TBL_USER).filter(TBL_USER.id == 'SUPERUSER').first()
    l_obj = db.query(TBL_USER_LOCATION_ASSIGNMENT).filter(
        TBL_USER_LOCATION_ASSIGNMENT.id == '1_SUPERUSER'
    ).first()

    if r_obj and u_obj and l_obj:
        print('Skipping — all records already exist.')
        return
    else :
        print('create role=============')
        r_obj = TBL_ROLE(
            id           = 'SUPERUSER',
            name         = 'SUPERUSER',
            name_lc      = 'SUPERUSER',
            is_superuser = True,
            description  = 'Superuser',
            branch_id    = 'HQ',
            company_id   = 'SYSTEM'
        )
        db.add(r_obj)
        print('create user=============')
        u_obj = TBL_USER(
            id               = 'SUPERUSER',
            first_name       = 'SUPERUSER',
            last_name        = 'SUPERUSER',
            email            = 'SUPERUSER',
            username         = 'SuperUser',
            phone            = '088888888',
            password         = get_password_hash('1qaz!QAZ'),
            pin              = '',
            photo            = '',
            is_active        = True,
            notification     = True,
            two_factor       = False,
            language         = 'en',
            last_activity_at = None,
            attempt          = 0,
            branch_id        = 'HQ',
            company_id       = 'SYSTEM',
            store_id         = 'HS',
        )
        db.add(u_obj)
        print('create location=============')
        l_obj = TBL_USER_LOCATION_ASSIGNMENT(
            id                    = '1_SUPERUSER',
            user_id               = 'SUPERUSER',
            accessible_company_id = 'SYSTEM',
            accessible_branch_ids = 'HQ',
            default_branch_id     = 'HQ',
            default_store_id      = 'HS',
            store_id              = 'HS',
            role_id               = 'SUPERUSER',
            is_default            = True,
            branch_id             = 'HQ',
            company_id            = 'SYSTEM'
        )
        db.add(l_obj)

from sqlalchemy.orm import Session as SASession
from core.db import engine
from core.model import Base

# Create ONE session at module level
db = SASession(engine)

def run():
    try:
        Base.metadata.create_all(bind=engine)
        db.rollback()
        create_user_and_role()
        generate_module()
        generate_admin_role()
        db.commit()
        print('Done! All data committed.')
    except Exception as e:
        db.rollback()
        print(f'Error: {e}')
        raise

'''
# python
#> from migrations.generate_module import *
#> run()
#> db.commit()
'''    