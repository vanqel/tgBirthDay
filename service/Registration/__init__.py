from .filter import *
from .utils import *


async def isRegister(user_id):
    await utils.service.isRegistration(user_id)
