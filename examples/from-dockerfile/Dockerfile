FROM ubi8/ruby-27

ADD --chown=default:root app-src ./

RUN bundle install --path ./bundle

CMD exec bundle exec "rackup -P /tmp/rack.pid --host 0.0.0.0 --port 8080"
