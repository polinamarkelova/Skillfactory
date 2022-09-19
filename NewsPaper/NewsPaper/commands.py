# 1. создание пользователей

from django.contrib.auth.models import User

user_1 = User.objects.create_user(username='petr', password='123456')
user_2 = User.objects.create_user(username='daria', password='654321')
user_3 = User.objects.create_user(username='polina', password='090302')
user_4 = User.objects.create_user(username='sonya')

# 2. Привязка к авторам

from news.models import Author

author_1 = Author.objects.create(user=User.objects.get(username='polina'))
author_2 = Author.objects.create(user=User.objects.get(username='sonya'))

# 3. Создание категорий

from news.models import Category

category_1 = Category.objects.create(category_name='Наука и технологии')
category_2 = Category.objects.create(category_name='Спорт')
category_3 = Category.objects.create(category_name='Культура')
category_4 = Category.objects.create(category_name='Путешествия')
category_5 = Category.objects.create(category_name='Интересное')

# 4. Создание постов

from news.models import Post

post_1 = Post.objects.create(atutor=Author.objects.get(pk=1), title='The Sims 4 станет бесплатной', text='Уже в октябре The Sims 4 '
                                                                                         'станет полностью '
                                                                                         'бесплатной игрой, однако '
                                                                                         'это может стать не '
                                                                                         'единственным подарком для '
                                                                                         'фанатов серии. Как '
                                                                                         'утверждает авторитетный '
                                                                                         'инсайдер Джефф '
                                                                                         'Грабб, компания готовится к '
                                                                                         'скорому анонсу '
                                                                                         'The Sims 5.', post_type='NW')
post_2 = Post.objects.create(author=Author.objects.get(pk=1), title='Лучшие города Германии, где нужно попробовать пиво', text='Пиво '
                                                                                                               '— '
                                                                                                               'важная часть немецкой культуры, и в этих пяти городах вы получите аутентичный опыт его дегустации. Эти города - Мюнхен(Октоберфест), Берлин(Berliner Weisse), Дюссельдорф(Альтбир), Кёльн(Кёльш), Нюрнберг', post_type='AR')
post_3 = Post.objects.create(author=Author.objects.get(pk=2), title='Почему спортсмены жуют жвачку во время игры?', text='Жвачка увеличивает время реакции и улучшает концентрацию внимания. Также она снижает уровень стресса. Жевательная резинка сохраняет влагу во рту', post_type='AR')

# 5. Присваивание поста к категории


post_1.category.add(category_1)
post_2.category.add(category_4)
post_3.category.add(category_1, category_2)

# 6. Написание комментариев

from news.models import Comment

comment_1 = Comment.objects.create(comment_post=post_1, comment_text='Очень давно ждал новостей о новой части симса!')
comment_2 = Comment.objects.create(comment_post=post_1, comment_text='Ура, бесплатный симс 4!')
comment_3 = Comment.objects.create(comment_post=post_2, comment_text='Как раз собралась в Германию, обязательно посетим одну из пивоварнь')
comment_4 = Comment.objects.create(comment_post=post_3, comment_text='Ничего нового не узнал...')

# 7. Применение методов лайк/дизлайк

post_1.like()
post_1.like()
post_1.like()
post_2.like()
post_2.like()
post_3.like()
comment_1.like()
comment_3.like()
comment_4.dislike()
post_1.like()
post_1.like()
post_2.like()
post_2.like()
post_2.dislike()


# 8. Обновление рейтинга

author_1 = Author.objects.get(pk=1)
author_1.update_rating()

author_2 = Author.objects.get(pk=2)

