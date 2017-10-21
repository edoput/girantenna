from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, InputRequired


class PolarForm(FlaskForm):
    """
    Form for handling polar positioning
    
    TODO: add validation on thread locking
    """
    degree = IntegerField(
            'degree',
            validators=[
                DataRequired(),
                InputRequired(),
                NumberRange(min=0, max=359),
            ]
            )

    minutes = IntegerField(
            'minutes',
            validators=[
                DataRequired(),
                InputRequired(),
                NumberRange(min=0, max=59)
            ],
            )


class PositionForm(PolarForm):
    """
    Handle setting position from web interface
    """
    submit = SubmitField('Set position')


class OffsetForm(PolarForm):
    """
    Handle setting position offset from web interface
    """
    submit = SubmitField('Set offset')
