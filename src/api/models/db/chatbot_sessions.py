import uuid

from tortoise import Model, fields


class ChatbotSession(Model):
    id = fields.TextField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255, default="New session")
    profile = fields.ForeignKeyField(model_name="backend.Profile", null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chatbot_sessions"