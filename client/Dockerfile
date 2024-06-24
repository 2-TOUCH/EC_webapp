# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory to
WORKDIR /ecocar_webapp/client

# Copy everything to the container
COPY . ./

# Install any needed packages
RUN npm install

# Run the command to start the server
CMD [ "npm", "start" ]
