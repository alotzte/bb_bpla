import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.bd.crud import UserCRUD, UserSettingsCRUD


async def mute_all_notifications(user_id, ):
    if await UserCRUD.user_exists(user_id):
        settings = await UserSettingsCRUD.get_user_settings_by_telegram_id(
            user_id
        )
        for idx in range(5):
            settings.settings[idx]["checked"] = False

        await UserSettingsCRUD.update_settings_by_telegram_id(
            user_id,
            settings.settings
        )
