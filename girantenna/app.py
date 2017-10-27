import os
import threading

from flask import Flask, render_template, redirect, request
from flask import jsonify

from .forms import OffsetForm, PositionForm
from .stepper import Stepper

version = '0.0.0'
app = Flask(__name__)
app.version = version
app.secret_key = 'pippopippo'

stepper = {
    'offset': 0,
    'position': 0,
}

stepper = Stepper([7, 11, 13, 15])
lock = threading.Lock()


class Movement(threading.Thread):
    """
    Execute the movevment in a non-blocking
    thread and acquire a lock on the stepper
    """
    def __init__(self, target):
        super(Movement, self).__init__()
        self.target = target

    def run(self):
        """
        Here happens magic
        """
        steps = round(self.target / 0.0878906)
        lock.acquire()
        stepper.move(steps=steps)
        lock.release()


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
            target = int(request.form['position-degree'], 10) + int(request.form['position-minutes'], 10) / 60
            app.logger.info('Target set to {target}'.format(target=target))
            Movement(target).start()
        if offset_form.validate():
            offset = int(request.form['offset-degree'], 10) + int(request.form['offset-minutes']) / 60
            app.logger.info('Offset set to {offset}'.format(offset=offset))
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
        'meta': meta,
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp
