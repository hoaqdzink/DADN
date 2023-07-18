from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from db.db import session
from entity.users import Users
from pkg import hash


def get_user_by_email(email: str) -> Users:
    results = session.query(Users.email, Users.password, Users.is_suspended).filter_by(email=email).all()
    return results[0] if len(results) > 0 else None


def get_user_by_id(user_id: int) -> Users:
    result = (
        session.query(
            Users.id,
            Users.company_name,
            Users.address,
            Users.phone_number,
            Users.email,
            Users.can_download_csv,
            Users.can_download_raw_data,
            Users.is_suspended,
            Users.name,
            Users.department,
            Users.memo,
        )
        .filter_by(id=user_id)
        .one()
    ) 
    return result 


def get_user_list() -> List[Users]:
    results = (
        session.query(
            Users.id,
            Users.company_name,
            Users.address,
            Users.phone_number,
            Users.email,
            Users.memo,
            Users.can_download_csv,
            Users.can_download_raw_data,
            Users.is_suspended,
            Users.last_seen_at,
            Users.created_at,
            Users.updated_at,
        )
        .order_by(Users.company_name, Users.email)
        .all()
    )
    return results


def update_user(
    user_id: int,
    company_name: str,
    address: str,
    phone_number: str,
    is_suspended: bool,
    can_download_csv: bool,
    can_download_raw_data: bool,
    name: str,
    department: str,
    email: str,
    password: Optional[str],
    memo: str,
):
    try:
        query = (
            update(Users)
            .values(
                company_name=company_name,
                address=address,
                phone_number=phone_number,
                is_suspended=is_suspended,
                can_download_csv=can_download_csv,
                can_download_raw_data=can_download_raw_data,
                name=name,
                department=department,
                email=email,
                memo=memo,
            )
            .where(Users.id == user_id)
        )
        if password:
            query = query.values(password=hash.get_hash(password))

        session.execute(query)
        session.commit()

    except IntegrityError as e:
        raise Exception(e.orig.args[1])


def add_user(
    company_name: str,
    address: str,
    phone_number: str,
    is_suspended: bool,
    can_download_csv: bool,
    can_download_raw_data: bool,
    name: str,
    department: str,
    email: str,
    password: str,
    memo: str,
) -> str:
    try:
        password = hash.get_hash(password)
        new_user = Users(
            company_name=company_name,
            address=address,
            phone_number=phone_number,
            is_suspended=is_suspended,
            can_download_csv=can_download_csv,
            can_download_raw_data=can_download_raw_data,
            name=name,
            department=department,
            email=email,
            password=password,
            memo=memo,
        )
        session.add(new_user)
        session.commit()
        return new_user.id
    except IntegrityError as e:
        raise Exception(e.orig.args[1])


def get_id_by_email(email: str) -> int:
    results = session.query(Users.id).filter_by(email=email).one()
    user_id = results.id
    return user_id


def get_permission_by_email(email: str) -> Users:
    result = (
        session.query(Users.id, Users.can_download_csv, Users.can_download_raw_data)
        .filter_by(email=email)
        .one()
    )
    return result
