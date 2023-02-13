import unittest

from app.tgbot.models.MyUser import MyUserBuilder, Direction, Course, Interest, MyUser


class MyUserBuilderTest(unittest.TestCase):

    def test_valid_set(self):
        user_builder = MyUserBuilder()

        user_builder.set_t_user_id(10000000000000)
        user_builder.set_email("sesh@niuitmo.ru")
        user_builder.set_full_name("Alex Andreev")
        user_builder.set_user_name("Alex_andrv")
        user_builder.set_direction(Direction.CPO)
        user_builder.set_course(Course.PHD)
        # user_builder.set_interest([Interest.ART, Interest.MARKETING, Interest.POLICY])
        # user_builder.set_interest([])
        user_builder.set_user_info("lorem lorem lorem")

        self.assertTrue(True)

    def test_invalid_mail(self):
        user_builder = MyUserBuilder()

        self.assertRaises(TypeError, user_builder.set_t_user_id, None)
        self.assertRaises(TypeError, user_builder.set_t_user_id, 'error')

        self.assertRaises(TypeError, user_builder.set_email, None)
        self.assertRaises(TypeError, user_builder.set_email, 10)

        self.assertRaises(TypeError, user_builder.set_full_name, None)
        self.assertRaises(TypeError, user_builder.set_full_name, 10)

        self.assertRaises(TypeError, user_builder.set_user_name, None)
        self.assertRaises(TypeError, user_builder.set_user_name, 10)

        self.assertRaises(TypeError, user_builder.set_direction, None)
        self.assertRaises(TypeError, user_builder.set_direction, 'error')

        self.assertRaises(TypeError, user_builder.set_course, None)
        self.assertRaises(TypeError, user_builder.set_course, 'error')

        # self.assertRaises(TypeError, user_builder.set_interest, None)
        # self.assertRaises(TypeError, user_builder.set_interest, 'error')

        self.assertRaises(TypeError, user_builder.set_user_info, None)
        self.assertRaises(TypeError, user_builder.set_user_info, 10)

    def test_convert(self):
        my_user = MyUser(t_user_id=10000000000000,
                         email="sesh@niuitmo.ru",
                         full_name="Alex Andreev",
                         user_name="Alex_andrv",
                         direction=Direction.CPO,
                         course=Course.PHD,
                         user_info="lorem lorem lorem")

        my_builder = MyUserBuilder.from_user(my_user)

        self.assertTrue(my_builder.t_user_id == 10000000000000)
        self.assertTrue(my_builder.email == "sesh@niuitmo.ru")
        self.assertTrue(my_builder.full_name == "Alex Andreev")
        self.assertTrue(my_builder.user_name == "Alex_andrv")
        self.assertTrue(my_builder.direction == Direction.CPO)
        self.assertTrue(my_builder.course == Course.PHD)
        self.assertTrue(my_builder.interest == [Interest.ART, Interest.MARKETING, Interest.POLICY])
        self.assertTrue(my_builder.user_info == "lorem lorem lorem")

    def test_enum(self):
        self.assertRaises(ValueError, Direction, None)
        self.assertRaises(ValueError, Direction, "error")
        Direction("ИВИТШ")
        Direction("ЦПО")

        self.assertRaises(ValueError, Course, None)
        self.assertRaises(ValueError, Course, "error")
        Course("3 курс")
        Course("Выпускник")

        self.assertRaises(ValueError, Interest, None)
        self.assertRaises(ValueError, Interest, "error")
        Interest("Маркетинг")
        Interest("Машинное обучение")


if __name__ == '__main__':
    unittest.main()
