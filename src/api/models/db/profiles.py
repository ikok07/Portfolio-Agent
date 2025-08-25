from tortoise import Model, fields

class Profile(Model):
    id = fields.TextField(primary_key=True)
    first_name = fields.TextField(null=False)
    last_name = fields.TextField(null=False)
    email = fields.TextField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "profiles"