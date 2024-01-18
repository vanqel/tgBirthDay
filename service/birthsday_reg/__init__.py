from .utils import *
from .filter import *


async def isRegister(user_id):
    await utils.service.isRegistration(user_id)
