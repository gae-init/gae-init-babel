# -*- coding: utf-8 -*-

import flask
from flaskext import wtf
from flaskext.babel import lazy_gettext as _
from flaskext.babel import gettext as __

import auth
import util
import model
import config

from main import app


class ConfigUpdateForm(wtf.Form):
  analytics_id = wtf.TextField(
    _('Google Analytics ID'),
    filters=[util.strip_filter])
  announcement_html = wtf.TextAreaField(
    _('Announcement HTML'),
    filters=[util.strip_filter])
  announcement_type = wtf.SelectField(
    _('Announcement Type'),
    choices=[(t, t.title()) for t in model.Config.announcement_type._choices])
  brand_name = wtf.TextField(
    _('Brand Name'),
    [wtf.validators.required()], filters=[util.strip_filter])
  facebook_app_id = wtf.TextField(
    _('Facebook App ID'),
    filters=[util.strip_filter])
  facebook_app_secret = wtf.TextField(
    _('Facebook App Secret'),
    filters=[util.strip_filter])
  feedback_email = wtf.TextField(
    _('Feedback Email'),
    [wtf.validators.optional(), wtf.validators.email()], filters=[util.strip_filter])
  flask_secret_key = wtf.TextField(
    _('Flask Secret Key'),
    [wtf.validators.required()], filters=[util.strip_filter])
  locale = wtf.SelectField(
    _('Default Locale'),
    choices=config.LOCALE_SORTED)
  twitter_consumer_key = wtf.TextField(
    _('Twitter Consumer Key'),
    filters=[util.strip_filter])
  twitter_consumer_secret = wtf.TextField(
    _('Twitter Consumer Secret'),
    filters=[util.strip_filter])


@app.route('/_s/admin/config/', endpoint='admin_config_update_service')
@app.route('/admin/config/', methods=['GET', 'POST'])
@auth.admin_required
def admin_config_update():
  config_db = model.Config.get_master_db()
  form = ConfigUpdateForm(obj=config_db)
  if form.validate_on_submit():
    form.populate_obj(config_db)
    config_db.put()
    reload(config)
    app.config.update(CONFIG_DB=config_db)
    return flask.redirect(flask.url_for('welcome'))

  if flask.request.path.startswith('/_s/'):
    return util.jsonify_model_db(config_db)

  return flask.render_template(
      'admin/config_update.html',
      title=_('Admin Config'),
      html_class='admin-config',
      form=form,
      config_db=config_db,
      has_json=True,
    )
