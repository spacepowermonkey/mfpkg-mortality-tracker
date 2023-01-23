FROM python:3.10

RUN mkdir -p /srv/mortality_tracker
RUN mkdir -p /data
RUN mkdir -p /docs

COPY data /data
COPY src /srv/mortality_tracker

#####
# Custom Section
RUN pip install pandas matplotlib numpy
RUN pip install cairosvg colorcet
#####

WORKDIR /srv
ENTRYPOINT [ "python3" ]
CMD [ "-m", "mortality_tracker"]
