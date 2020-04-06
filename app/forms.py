from wtforms import Form, StringField, SelectField


class SearchForm(Form):
    choices = [('Piazza', 'Piazza'),
               ('Online', 'Online')]
    select = SelectField('Enter Your Search:', choices=choices)
    search = StringField('')
