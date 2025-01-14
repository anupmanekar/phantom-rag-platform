# Use node:14-alpine as the base image
FROM node:14-alpine

# Set the working directory
WORKDIR /app

# Copy the frontend directory into the Docker image
COPY . .

# Install the required dependencies using npm
RUN npm install

# Set the entrypoint to run the Next.js application using npm run dev
CMD ["npm", "run", "dev"]
