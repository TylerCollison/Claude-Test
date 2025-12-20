FROM node:20-alpine

RUN apk update
RUN apk add bash
RUN apk add git

RUN npm install -g @anthropic-ai/claude-code
RUN npm install -g @musistudio/claude-code-router

COPY config.json /config.json
COPY config.json /root/.claude-code-router/config.json

ENV SHELL=/bin/bash
ENTRYPOINT ["/bin/bash"]