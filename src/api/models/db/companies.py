import uuid

from tortoise import Model, fields

class Company(Model):
    id = fields.TextField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255, null=False, unique=True)
    website = fields.CharField(max_length=255, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "companies"
