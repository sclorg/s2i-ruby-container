FROM ubi8/ruby-33

ADD --chown=default:root app-src ./

RUN bundle config set --local path ./bundle && \
      bundle install

CMD exec bundle exec "rackup -P /tmp/rack.pid --host 0.0.0.0 --port 8080"
