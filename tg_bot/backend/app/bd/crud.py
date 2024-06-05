from typing import Optional
from bd.models.user import User
from bd.models.user_settings import UserSettings


class UserCRUD:
    @staticmethod
    async def create_user(telegram_id: int, name: str):
        user = await User.create(telegram_id=telegram_id, name=name)
        return user

    @staticmethod
    async def get_user(telegram_id: int):
        user = await User.get_or_none(telegram_id=telegram_id)
        if user:
            return user
        return False

    @staticmethod
    async def update_user(telegram_id: int, name: Optional[str] = None):
        user = await UserCRUD.get_user(telegram_id)
        if name is not None:
            user.name = name
        await user.save()
        return user

    @staticmethod
    async def delete_user(telegram_id: int):
        user = await UserCRUD.get_user(telegram_id)
        await user.delete()
        return {"message": "User deleted"}

    @staticmethod
    async def user_exists(telegram_id: int) -> bool:
        user = await User.get_or_none(telegram_id=telegram_id)
        return user is not None


class UserSettingsCRUD:
    @staticmethod
    async def create_user_settings(telegram_id: int, settings: dict):
        user = await UserCRUD.get_user(telegram_id)
        user_settings = await UserSettings.create(user=user, settings=settings)
        return user_settings

    @staticmethod
    async def get_user_settings(settings_id: int):
        user_settings = await UserSettings.get_or_none(id=settings_id)
        if user_settings:
            return user_settings
        return False

    @staticmethod
    async def update_user_settings(settings_id: int, settings: dict):
        user_settings = await UserSettingsCRUD.get_user_settings(settings_id)
        user_settings.settings = settings
        await user_settings.save()
        return user_settings

    @staticmethod
    async def delete_user_settings(settings_id: int):
        user_settings = await UserSettingsCRUD.get_user_settings(settings_id)
        await user_settings.delete()
        return {"message": "User settings deleted"}

    @staticmethod
    async def update_settings_by_telegram_id(telegram_id: int, settings: dict):
        user = await UserCRUD.get_user(telegram_id)
        user_settings = await UserSettings.get(user=user)
        user_settings.settings = settings
        await user_settings.save()
        return user_settings

    @staticmethod
    async def get_user_settings_by_telegram_id(telegram_id: int):
        user = await UserCRUD.get_user(telegram_id)
        user_settings = await UserSettings.get_or_none(user=user)
        if user_settings:
            return user_settings
        return False
