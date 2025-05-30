TOKEN = open("token.txt").readline()
ALPHABET = " 0123456789-йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm?%.,()!:;"

INTENTS_DICTIONARY = {'hello': {'examples': ['Здравствуй', 'Здравствуйте', 'Привет', 'Приветик', 'Хай'],
                           'answers': ['Здравствуйте! Чем могу вам помочь?', 'Доброго времени суток!', 'Приветствую!']},
                      'whatsup': {'examples': ['Как у тебя дела', 'Как поживаешь', 'Как жизнь', 'Как дела', 'Как ты'],
                                  'answers': ['Всё замечательно! Лежу, отдыхаю на диванчике', 'Хорошо) Собираю шкаф для папы...', 'Всё отлично. Спасибо, что поинтересовались!']},
                      'name': {'examples': ['Кто ты', 'Как тебя зовут'],
                               'answers': ['Я SofaShopBot - ваш бот-помощник с выбором мебели!', 'Меня зовут SofaShopBot, и я очень люблю мягкие диваны)']},
                      'thanks': {'examples': ['Спасибо', 'Большое спасибо', 'Спасибочки', 'Благодарствую'],
                                 'answers': ['Всегда пожалуйста)', 'Всегда рад помочь!', 'Обращайтесь!']},
                      'goodbye':
                          {'examples': ['Пока', 'До свидания', 'До связи', 'До скорой встречи'],
                           'answers': ['До свидания!', 'Приходите ещё!', 'Буду рад вам помочь вновь)']},
                      'order': {'examples': ['Хочу сделать заказ', 'Заказ', 'Оформи заказ', 'Нужно сделать заказ'],
                                'answers': ['Нажмите /order, чтобы сделать заказ']},
                      'cart': {'examples': ['Хочу глянуть корзину', 'Что у меня в корзине', 'Моя корзина'],
                               'answers': ['#view_cart']},
                      'add': {'examples': ['Добавить предмет в корзину', 'Хочу добавить предмет в корзину', 'Добавить'],
                              'answers': ['Нажмите /cart, чтобы сделать заказ']},
                      'catalog': {'examples': ['Что у вас есть', 'Ваш каталог', 'Хочу ознакомиться с ассортиментом', 'Нужно увидеть ваш каталог'],
                                  'answers': ['#catalog']},
                      'faq': {"examples": ['Я ничего не понимаю', 'У меня есть вопросы', 'Есть вопросы', 'Поясни'],
                             'answers': ['#faq']},
                      'help': {"examples": ['Я ничего не понимаю', 'Помоги', 'Помогите мне', 'Помоги мне'],
                               'answers': ['#help']},
                      'contacts': {"examples": ['Дайте ваши контакты', 'Дай контакты', 'Контакты', 'Как с вами связаться', 'Куда вам можно написать'],
                                   'answers': ['#info']},
                      'furniture':
                          {'examples': ['Очень нужна новая мебель', 'Хочу купить мебель', 'Мне нужна обновка', 'Планирую переезжать', 'У меня сломалась кровать'],
                           'answers': ['Значит, вам нужна помощь в подборе и покупке мебели?'],
                           'theme_gen': 'furniture_q_demand',
                           'theme_app': ['furniture', '*']},
                      'yes': {'examples': ['Да', 'Мне нужна новая мебель', 'Я хочу заказать новую мебель'],
                              'answers': ['Прекрасно, тогда подскажите, что именно вы бы хотели приобрести? У нас в наличии есть:\n-диваны;\n-кресла;\n-кровати;\n-офисные стулья;\n-обеденные столы;\n-книжные полки;\n-шкафы'],
                              'theme_gen': "furniture_q_choice",
                              'theme_app': ['furniture_q_demand', "*"]},
                      'no': {'examples': ['Нет', 'Нет, мне не нужна помощь с выбором', 'Я не собираюсь заказывать мебель', 'Я не хочу заказывать мебель'],
                             'answers': ['Хорошо. Но, если что, знайте - я всегда тут)', 'Как скажете, кэп) Однако помните, что у меня всегда для вас есть хорошие предложения!'],
                             'theme_app': ['furniture_q_demand']},
                      'sofa': {'examples': ['Мне нужен новый диван', 'Диван', 'Хочу диван', 'Помоги выбрать диван', 'Afina'],
                               'answers': ['У меня как раз есть для вас предложение: раскладной диван Afina. Современный дизайнерский диван, на котором удобно не только гостей встречать, но и отсыпаться после долгой рабочей смены! В комплекте идут мягкие подушки - настолько мягкие, что плакать в них после расставания одно удовольствие. И стоит это чудо всего 11900 рублей!\nЧтобы оформить заказ, введите команду /order - и мы приступим к оформлению заявки\n/cart - чтобы добавить предмет в корзину'],
                               'theme_gen': 'Afina',
                               'theme_app': ['furniture_q_demand_advert']},
                      'bed': {'examples': ['Кровать', 'Мне нужна кровать', 'Нуждаюсь в кровати', 'Хочу кровать', 'Помоги выбрать кровать', 'Sakura'],
                              'answers': ['Вам прекрасно подойдёт кровать Sakura - отличный вариант для тех, кто ценит комфорт, а также уникальный стиль, вдохновлённый японскими пагодами! Стоит всего 15999 рублей. Поторопитесь оформить заказ!\nЧтобы оформить заказ, введите команду /order - и мы приступим к оформлению заявки\n/cart - чтобы добавить предмет в корзину'],
                              'theme_gen': 'Sakura',
                              'theme_app': ['furniture_q_demand_advert']},
                      'chair': {'examples': ['Нужен стул', 'Стул', 'Присесть', 'Стульчик', 'Хочу стул', 'Помоги выбрать стул', 'Veronna'],
                                'answers': ['Я знаю один подходящий вам стул - офисный стул Veronna с газовым лифтом. Дизайн этого стула поможет вашей спине меньше уставать, а вам - чувствовать себя прекрасно на протяжение всего рабочего дня. Цена вопроса - всего 6700 рублей.\nЧтобы оформить заказ, введите команду /order - и мы приступим к оформлению заявки\n/cart - чтобы добавить предмет в корзину'],
                                'theme_gen': 'Veronna',
                                'theme_app': ['furniture_q_demand_advert']},
                      'table': {'examples': ['Обеденный стол', 'Нужен стол', 'Стол', 'Мне нужен обеденный стол', 'Хочу стол', 'Помоги выбрать стол', 'Arial'],
                                'answers': ['Как насчёт стола Arial? Стильный, компактный, но в то же время вмещающий за собой до 7 человек. Легко моется и устанавливается. И проверить этот факт можно за 4000 рублей!\nЧтобы оформить заказ, введите команду /order - и мы приступим к оформлению заявки'],
                                'theme_gen': 'Arial', 'theme_app': ['furniture_q_demand_advert']},
                      'armchair': {'examples': ['Кресло', 'Нужно кресло', 'Мне нужно кресло', 'Хочу кресло', 'Jasmine'],
                                   'answers': ['В кресле Jasmine вы забудете обо всех проблемах! Мягкая, но прочная обивка приятна на ощупь и сохраняет свой внешний вид даже после самой агрессивной чистки. Удобство кресла Jasmine было не раз проверено спинами наших коллег. Спешите оформить заказ - всего за 6890 рублей!\nЧтобы оформить заказ, введите команду /order - и мы приступим к оформлению заявки\n/cart - чтобы добавить предмет в корзину'],
                                   'theme_gen': 'Jasmine', 'theme_app': ['furniture_q_demand_advert']},
                      'wardrobe': {'examples': ['Шкаф', 'Гардеробный шкаф', 'Мне нужен шкаф', 'Нужен шкаф', 'Хочу шкаф', 'Diana'],
                                   'answers': ['Шкаф Diana - вместительный и компактный шкаф, который впишется в интерьер любой комнаты. Дверцы с доводчиками обеспечивают бесшумное закрытие, а надёжная штанга выдержит вес даже самых причудливых и дорогих нарядов. Цена этого чудного шкафа - всего лишь 106700 рублей.\nЧтобы оформить заказ, введите команду /order - и мы приступим к оформлению заявки\n/cart - чтобы добавить предмет в корзину'],
                                   'theme_gen': 'Diana', 'theme_app': ['furniture_q_demand_advert']},
                      'shelf': {'examples': ['Полка', 'Книжная полка', 'Мне нужна книжная полка', 'Нужна полка для книг', 'Хочу книжную полку', 'Anthony'],
                                'answers': ['Ищете идеальную книжную полку? Не нужно искать - полка Anthony прекрасно вам подойдёт. Сочетает в себе хорошую вместительность и роскошный вид, напоминающий старинные книжные шкафы. Всё ещё размышляете? Поторопитесь, ведь за 14600 рублей полка Anthony будет раскуплена моментально!\nЧтобы оформить заказ, введите команду /order - и мы приступим к оформлению заявки\n/cart - чтобы добавить предмет в корзину'],
                                'theme_gen': 'Anthony', 'theme_app': ['furniture_q_demand_advert']}
                      }
FAILURE = ['Простите, я вас понимаю(', 'Слишком сложно. Попробуйте переформулировать запрос', 'Мне кажется, вы имели в виду что-то другое...', 'Кажется, у вас кот на клавиатуру сел...']
CATOLOG = ["Диван раскладной Afina", "Кровать Sakura двуместная", "Офисный стул Veronna", "Обеденный стол Arial", "Кресло Jasmine", "Книжная полка Anthony", "Шкаф Diana"]
GOODS = ['Afina', 'Sakura', 'Veronna', 'Arial', 'Jasmine', 'Diana', 'Anthony']