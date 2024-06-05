from tortoise import fields
from tortoise.models import Model


class User(Model):
    telegram_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    class Meta:
        table = "users"
