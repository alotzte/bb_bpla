from tortoise import fields
from tortoise.models import Model


class UserSettings(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='settings', to_field='telegram_id') 
    settings = fields.JSONField()

    class Meta:
        table = "user_settings"
