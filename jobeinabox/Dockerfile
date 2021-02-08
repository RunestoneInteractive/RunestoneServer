FROM trampgeek/jobeinabox:latest

COPY include/* /usr/include/
RUN rm -rf /var/www/html/jobe && \
    git clone https://github.com/RunestoneInteractive/jobe.git /var/www/html/jobe && \
    apache2ctl start && \
    cd /var/www/html/jobe && ./install

# Healthcheck, minimaltest.py should complete within 2 seconds
HEALTHCHECK --interval=5m --timeout=2s \
    CMD /usr/bin/python3 /var/www/html/jobe/minimaltest.py || exit 1

# Start apache
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
