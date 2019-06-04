from flask import flash


def raise_flash_messages(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'danger')