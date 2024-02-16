from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")], render_kw={"placeholder": "Email"})
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")], render_kw={"placeholder": "Пароль"})
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    name = StringField("ФИО: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")], render_kw={"placeholder": "ФИО"})
    email = StringField("Email: ", validators=[Email("Некорректный email")], render_kw={"placeholder": "Email"})
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")], render_kw={"placeholder": "Пароль"})

    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")], render_kw={"placeholder": "Повтор пароля"})
    submit = SubmitField("Регистрация")

class StatementForm(FlaskForm):
    title = StringField("Заглавие ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")], render_kw={"placeholder": "О проблеме"})
    number = IntegerField(render_kw={"placeholder": "Номер телефона"})
    text = TextAreaField("Опишите проблему",validators=[DataRequired(), Length(min=10, max=10000)], render_kw={"placeholder": "Опишите проблему"})
    submit = SubmitField("Оставить заявку")