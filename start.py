from flask import Flask, render_template, request, jsonify
from sh import Command, cat
app = Flask(__name__)

translation_dict = {
    'out': 'on',
    'in': 'off',
}


def toggle_lights(state):
    """
    Simply call the trigger script that's located in the path
    """
    if state == 'on':
        turn_on = Command('/bin/bash')
        turn_on('/var/scripts/on.sh')
    if state == 'off':
        turn_off = Command('/bin/bash')
        turn_off('/var/scripts/off.sh')
    #current_state = cat('/sys/class/gpio/gpio67/direction')
    return get_current_state()


def get_current_state():
    current_state =  cat('/sys/class/gpio/gpio67/direction')
    return translation_dict[current_state.stdout[:-1]]


@app.route('/', methods=["GET", "POST"])
def index():
    """
    This is the page which the user will see if they
    fetch it. It has simply two buttons ON and OFF

    The template has a form that passes either ON or OFF
    and that is available in the translation dict

    There is a very simple validation on this point.
    If we receive anything other than ON or OFF, don't do anything.
    """
    if request.method == "POST":
        state = request.form['lights']
        if state in translation_dict.values():
            toggle_lights(state)
    current_state = get_current_state()
    return render_template("toggle.html", current_state=current_state)

@app.route('/remote', methods=["GET", "POST"])
def remote_trigger():
    """
    This is to toggle the lights from a remote url.
    It's different because it doesn't serve any templates but instead
    sends back an HTTPResponse with the state if GET is received.

    POST does the exact same thing as the one above.
    """
    if request.method == "GET":
        return get_current_state()
    elif request.method == "POST":
        state = request.form['lights']
        new_state = toggle_lights(state if state in translation_dict.values() else None)
        return new_state 

app.debug = True

if __name__ == "__main__":
    app.run('0.0.0.0')
