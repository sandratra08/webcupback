from tortoise.models import Model
from tortoise import fields, timezone


class User(Model):

    id = fields.IntField(pk=True, primary_key=True)
    name = fields.CharField(max_length=100, null=True)
    first_name = fields.CharField(max_length=100, null=True)
    gender = fields.CharField(max_length=6, null=True)
    birth_date = fields.DatetimeField(null=True)
    email = fields.CharField(max_length=100, null=False)
    password = fields.CharField(max_length=300, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = "users"


class AccessToken(Model):
    access_token = fields.CharField(pk=True, max_length=255)
    user = fields.ForeignKeyField("models.User", null=False)
    expiration_date = fields.DatetimeField(null=False)

    class Meta:
        table = "access_tokens"


class Dream(Model):
    id = fields.IntField(pk=True, primary_key=True)
    description = fields.TextField(null=False)
    prediction = fields.CharField(max_length=40, null=True)
    advice = fields.TextField(null=True)
    user = fields.ForeignKeyField("models.User", null=False)

    class Meta:
        table = "dreams"
