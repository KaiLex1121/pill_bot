from aiogram.fsm.context import FSMContext


async def find_message_to_delete(state: FSMContext) -> int:
    state_dict = await state.get_data()
    return state_dict['message_to_delete']
