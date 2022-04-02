from aiogram import types


# This function for edit call message text if this impossible sends new message
async def edit_text_call(call: types.CallbackQuery, text: str, k_board=None):
    try:
        await call.message.edit_text(text=text, reply_markup=k_board)
    except Exception as _ex:
        await call.message.answer(text=text, reply_markup=k_board)
