import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from helpdesk import create_app
from helpdesk.actions import get_clients, get_users, get_user, get_client, add_ticket

class TicketStates(StatesGroup):
    title = State()
    assignee = State()
    client = State()
    body = State()

async def main():
    app = create_app()
    bot = Bot(token="bot")
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        await message.answer("Добавлять новые заявки вы можете при помощи /add_ticket")

    @dp.message(Command("cancel"))
    async def cmd_cancel(message: Message, state: FSMContext):
        if await state.get_state() is None:
            await message.answer("Отменять нечего.")
            return

        await state.clear()
        await message.answer("Действие отменено.")

    @dp.message(Command("add_ticket"))
    async def cmd_add_ticket(message: Message, state: FSMContext):
        await message.answer("Заполните название новой заявки.")

        await state.set_state(TicketStates.title)

    @dp.message(TicketStates.title)
    async def process_title(message: Message, state: FSMContext):
        await state.update_data(title=message.text.strip())

        text = "Кто будет ответственным? Необходимо ввести число.\n\n"

        with app.app_context():
            for user in get_users():
                text += f"{user.id}: {user.username}\n"

        await message.answer(text)
        await state.set_state(TicketStates.assignee)

    @dp.message(TicketStates.assignee)
    async def process_assignee(message: Message, state: FSMContext):
        with app.app_context():
            if not message.text.isdigit():
                await message.answer("Введите число.")
                return
            elif get_user(int(message.text)) is None:
                await message.answer("Ответственного с таким номером не существует.")
                return
        
        await state.update_data(assignee=int(message.text))

        text = "На какого клиента? Необходимо ввести число.\n\n"

        with app.app_context():
            for client in get_clients():
                text += f"{client.id}: {client.name}\n"

        await message.answer(text)
        await state.set_state(TicketStates.client)

    @dp.message(TicketStates.client)
    async def process_client(message: Message, state: FSMContext):
        with app.app_context():
            if not message.text.isdigit():
                await message.answer("Введите число.")
                return
            elif get_client(int(message.text)) is None:
                await message.answer("Клиента с таким номером не существует.")
                return
        
        await state.update_data(client=int(message.text))

        await message.answer("Теперь заполните описание. Текст должен быть не менее 100 символов.")
        await state.set_state(TicketStates.body)

    @dp.message(TicketStates.body)
    async def process_body(message: Message, state: FSMContext):
        if len(message.text) < 100:
            await message.answer("Текст имеет меньше 100 символов.")
            return

        await state.update_data(body=message.text)

        data = await state.get_data()

        with app.app_context():
            add_ticket(
                assignee_id=data.get("assignee"),
                client_id=data.get("client"),
                title=data.get("title"),
                body=data.get("body"),
                sent_via=4 # Специальный номер для Telegram.
            )

        await message.answer("Заявка отправлена.")
        await state.clear()

    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
