from flask import redirect, url_for
from flask_login import current_user

class AddThreat:
  def post(self):
    if current_user.is_admin:
        return redirect(url_for('/admin/attacks'))