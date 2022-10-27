from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class FSMPurchase(StatesGroup):
    reason = State()
