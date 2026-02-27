from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Role, User
from app.core.security import hash_password
from app.core.config import settings
async def seed_roles_and_admin(db: AsyncSession):

    roles = ["ADMIN", "CREATOR", "VIEWER"]

    # setup roles
    for role_name in roles:
        result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        if not result.scalar_one_or_none():
            db.add(Role(name=role_name))

    await db.commit()

    # init admin if missing
    result = await db.execute(
        select(User).where(User.email == settings.DEFAULT_ADMIN_EMAIL)
    )
    existing_admin = result.scalar_one_or_none()

    if not existing_admin:

        role_result = await db.execute(
            select(Role).where(Role.name == "ADMIN")
        )
        admin_role = role_result.scalar_one()

        admin_user = User(
            email=settings.DEFAULT_ADMIN_EMAIL,
            hashed_password=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
            role_id=admin_role.id
        )

        db.add(admin_user)
        await db.commit()

    print("\n🚀 Default Admin Created")
    print(f"Email: {settings.DEFAULT_ADMIN_EMAIL}")
    print(f"Password: {settings.DEFAULT_ADMIN_PASSWORD}\n") 