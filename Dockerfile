FROM stevenmburns/tally_image as kenken_image

RUN \
    mkdir -p /kenken

ADD . /kenken

RUN \
    bash -c "source general/bin/activate && cd /kenken/ && pip install ."







