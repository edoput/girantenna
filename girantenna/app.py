import os
import threading

from flask import Flask, render_template, redirect, request
from flask import jsonify

from .forms import OffsetForm, PositionForm
# from .stepper import Stepper

version = '0.0.0'
app = Flask(__name__)
app.version = version
app.secret_key = 'pippopippo'

stepper = {
    'offset': 0,
    'position': 0,
}

# stepper = Stepper([7, 0, 2, 3])
lock = threading.Lock()


class Movement(threading.Thread):
    """
    Execute the movevment in a non-blocking
    thread and acquire a lock on the stepper
    """
    def __init__(self, target):
        self.target = target

    def run(target):
        """
        Here happens magic
        """
        lock.acquire()
        # stepper.move()
        lock.release()
        pass


"""
Send some information to the
client about the application
"""
meta = {
    'version': app.version,
    'debug': bool(os.environ.get('DEBUG', False)),
}


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Show a bare ui that can set `position` and `offset`
    for the device

    When asked to move acquire a lock on the stepper
    """
    position_form = PositionForm(prefix='position')
    offset_form = OffsetForm(prefix='offset')

    submissions = [
        position_form.validate_on_submit(),
        offset_form.validate_on_submit(),
    ]

    if any(submissions):
        """
        The position form has prefix `position` and the
        offset form has prefix `offset` for every key
        """
        if position_form.validate():
            stepper['position'] = int(request.form['position-degree'], 10) + int(request.form['position-minutes'], 10) / 60
            Movement(stepper).start()
        if offset_form.validate():
            stepper['offset'] = int(request.form['offset-degree'], 10) + int(request.form['offset-minutes']) / 60
        return redirect('/')

    return render_template(
                        'index.html',
                        position_form=position_form,
                        offset_form=offset_form,
                        )


@app.route('/status')
def status():
    """
    Return the sensor values and
    known values

    - orientation value
    - zero offset from north
    """
    data = {
        'orientation': stepper.get('position', 0),
        'offset': stepper.get('offset', 0),
        'meta': meta,
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp
