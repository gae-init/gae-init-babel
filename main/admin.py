# -*- coding: utf-8 -*-

from google.appengine.api import app_identity
import flask
from flask_wtf import Form
import wtforms
import wtforms.validators
from flask_babel import lazy_gettext as _
from flask_babel import gettext as __

import auth
import util
import model
import config

from main import app


class ConfigUpdateForm(Form):
  analytics_id = wtforms.TextField('Analytics ID', filters=[util.strip_filter])
  announcement_html = wtforms.TextAreaField('Announcement HTML', filters=[util.strip_filter])
  announcement_type = wtforms.SelectField('Announcement Type', choices=[(t, t.title()) for t in model.Config.announcement_type._choices])
  brand_name = wtforms.TextField('Brand Name', [wtforms.validators.required()], filters=[util.strip_filter])
  facebook_app_id = wtforms.TextField('Facebook App ID', filters=[util.strip_filter])
  facebook_app_secret = wtforms.TextField('Facebook App Secret', filters=[util.strip_filter])
  feedback_email = wtforms.TextField('Feedback Email', [wtforms.validators.optional(), wtforms.validators.email()], filters=[util.email_filter])
  flask_secret_key = wtforms.TextField('Flask Secret Key', [wtforms.validators.required()], filters=[util.strip_filter])
  locale = wtforms.SelectField('Default Locale', choices=config.LOCALE_SORTED)
  twitter_consumer_key = wtforms.TextField('Twitter Consumer Key', filters=[util.strip_filter])
  twitter_consumer_secret = wtforms.TextField('Twitter Consumer Secret', filters=[util.strip_filter])


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

  instances_url = None
  if config.PRODUCTION:
    instances_url = '%s?app_id=%s&version_id=%s' % (
        'https://appengine.google.com/instances',
        app_identity.get_application_id(),
        config.CURRENT_VERSION_ID,
      )

  return flask.render_template(
      'admin/config_update.html',
      title=_('Admin Config'),
      html_class='admin-config',
      form=form,
      config_db=config_db,
      instances_url=instances_url,
      has_json=True,
    )
