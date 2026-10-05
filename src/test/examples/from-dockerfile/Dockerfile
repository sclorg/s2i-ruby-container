FROM {{ spec.readme_ref_image }}

ADD --chown=default:root app-src ./

{# bundler in Ruby >= 3.3 should use the 'config set'. #}
{# earlier rubies have either limited support or different CLI usage. #}
{% if spec.stream == "2.5" %}
RUN bundle install --path bundle
{% else %}
RUN bundle config set --local path ./bundle && \
      bundle install
{% endif %}

CMD exec bundle exec "rackup -P /tmp/rack.pid --host 0.0.0.0 --port 8080"
