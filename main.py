from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, KeyboardButton, ReplyKeyboardMarkup
from config import TOKEN
from questions import python_questions, django_questions


def start_command(update, context):
    first_name = update.message.from_user.first_name
    commands = [
        BotCommand(command='start', description='Ishga tushirish'),
        BotCommand(command='help', description='Yordam')
    ]

    buttons = [
        [KeyboardButton(text='Python'), KeyboardButton('Django')]
    ]

    context.bot.set_my_commands(commands=commands)
    update.message.reply_text(text=f"Xush kelibsiz! <b>{first_name}</b>\nTanlang:",
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True),
                              parse_mode='HTML')

def help_command(update,context):
    update.message.reply_text(
        text='Bu bot sizlarga python va django dan bilimlaringizni tekshirib ko\'rishingizga yordam beradi.'
    )


def python_questions_func(update, context):
    if context.user_data['language'] == 'Python':
        buttons = [
            [InlineKeyboardButton(text=f"{python_questions[0]['a']}", callback_data='a')],
            [InlineKeyboardButton(text=f"{python_questions[0]['b']}", callback_data='b')],
            [InlineKeyboardButton(text=f"{python_questions[0]['c']}", callback_data='c')],
            [InlineKeyboardButton(text="Testni tugatish", callback_data='test_finished')],
        ]

        context.user_data['question_index'] = 0
        context.user_data['true'] = 0
        update.message.reply_text(
            text=f"{python_questions[0]['Savol']}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [
            [InlineKeyboardButton(text=f"{django_questions[0]['a']}", callback_data='a')],
            [InlineKeyboardButton(text=f"{django_questions[0]['b']}", callback_data='b')],
            [InlineKeyboardButton(text=f"{django_questions[0]['c']}", callback_data='c')],
            [InlineKeyboardButton(text="Testni tugatish", callback_data='test_finished')],
        ]

        context.user_data['question_index'] = 0
        context.user_data['true'] = 0
        update.message.reply_text(
            text=f"{django_questions[0]['Savol']}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


def question_amount(update, context):
    buttons = [
        [KeyboardButton(text='10'), KeyboardButton(text='15')],
        [KeyboardButton(text='25'), KeyboardButton(text='50')]
    ]
    update.message.reply_text(text='Testlar sonini tanlang:',
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


def message_handler(update, context):
    message = update.message.text
    context.user_data['count'] = 0
    if message == 'Python':
        context.user_data['language'] = 'Python'
        question_amount(update, context)
    elif message == 'Django':
        context.user_data['language'] = 'Django'
        question_amount(update, context)
    elif str(message).isdigit():
        python_questions_func(update, context)
        if str(message) == '10':
            context.user_data['count'] = 10
        elif str(message) == '15':
            context.user_data['count'] = 15
        elif str(message) == '20':
            context.user_data['count'] = 20
        elif str(message) == '50':
            context.user_data['count'] = 50


def inline_message(update, context):
    query = update.callback_query
    first_name = update.callback_query.from_user.first_name

    if context.user_data['language'] == 'Python':
        if query.data in ['a', 'b', 'c']:
            global question_index
            question_index = context.user_data.get('question_index', 0)
            if query.data == python_questions[question_index]['Javob']:
                context.user_data['true'] += 1
            if question_index < int(context.user_data['count']) - 1:
                buttons = [
                    [InlineKeyboardButton(text=f"{python_questions[question_index + 1]['a']}", callback_data="a")],
                    [InlineKeyboardButton(text=f"{python_questions[question_index + 1]['b']}", callback_data="b")],
                    [InlineKeyboardButton(text=f"{python_questions[question_index + 1]['c']}", callback_data="c")],
                    [InlineKeyboardButton(text="Testni tugatish", callback_data='test_finished')],
                ]
                query.message.edit_text(
                    text=f"{python_questions[question_index + 1]['Savol']}",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                context.user_data['question_index'] = question_index + 1
            else:
                query.message.edit_text(
                    text=f"<b>Test tugadi {first_name}!</b>\n<b>Savollar soni:</b> {question_index+1}\n<b>To'g'r javoblar soni:</b> {context.user_data['true']}",
                    parse_mode='HTML')
        elif query.data == 'test_finished':
            query.message.edit_text(
                text=f"<b>Test tugadi {first_name}!</b>\n<b>Savollar soni:</b> {question_index+1}\n<b>To'g'r javoblar soni:</b> {context.user_data['true']}",
                parse_mode='HTML')

    elif context.user_data['language'] == 'Django':
        if query.data in ['a', 'b', 'c']:
            question_index = context.user_data.get('question_index', 0)
            if query.data == django_questions[question_index]['Javob']:
                context.user_data['true'] += 1

            if question_index < int(context.user_data['count']) - 1:
                buttons = [
                    [InlineKeyboardButton(text=f"{django_questions[question_index + 1]['a']}", callback_data="a")],
                    [InlineKeyboardButton(text=f"{django_questions[question_index + 1]['b']}", callback_data="b")],
                    [InlineKeyboardButton(text=f"{django_questions[question_index + 1]['c']}", callback_data="c")],
                    [InlineKeyboardButton(text="Testni tugatish", callback_data='test_finished')],
                ]
                query.message.edit_text(
                    text=f"{django_questions[question_index + 1]['Savol']}",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                context.user_data['question_index'] = question_index + 1
            else:
                query.message.edit_text(
                    text=f"<b>Test tugadi {first_name}!</b>\n<b>Savollar soni:</b> {question_index+1}\n<b>To'g'r javoblar soni:</b> {context.user_data['true']}",
                    parse_mode='HTML')
        elif query.data == 'test_finished':
            query.message.edit_text(
                text=f"<b>Test tugadi {first_name}!</b>\n<b>Savollar soni:</b> {question_index+1}\n<b>To'g'r javoblar soni:</b> {context.user_data['true']}",
                parse_mode='HTML')


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help',help_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
