FROM python:3.9-buster

# Set pip to have no saved cache
ENV PIP_NO_CACHE_DIR=false

# Create the working directory
WORKDIR /qubit

# Install sources for bot
RUN git clone https://github.com/pycord-development/pycord.git && pip install ./pycord


# Delete pycord source after package install
RUN rm -rf pycord/


# Install project dependencies
COPY requirements.txt .

# Update pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# Install deps
RUN pip install -r requirements.txt


# Define Git SHA build argument
ARG git_sha="development"

# Set Git SHA environment variable for Sentry
ENV GIT_SHA=$git_sha

# Copy the source code in last to optimize rebuilding the image
COPY . .

