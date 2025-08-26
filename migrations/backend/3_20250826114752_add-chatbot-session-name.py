from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chatbot_sessions" ADD "name" VARCHAR(255) NOT NULL DEFAULT 'New session';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chatbot_sessions" DROP COLUMN "name";"""
