from typing import Optional

from pydantic import BaseModel

class ClerkUserEmails(BaseModel):
    id: str
    email_address: str

class ClerkUserPhoneNumbers(BaseModel):
    id: str
    phone_number: str

class ClerkUserCreatedData(BaseModel):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    email_addresses: list[ClerkUserEmails]
    phone_numbers: list[ClerkUserPhoneNumbers]

class ClerkUserCreatedBody(BaseModel):
    data: ClerkUserCreatedData