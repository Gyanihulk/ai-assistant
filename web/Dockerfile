# Use a base image with Node.js installed
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Install necessary system dependencies for native builds
# Ensure all package installation commands are on a single line or properly use the backslash to continue lines
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    python3

# Clean up the apt cache by removing /var/lib/apt/lists to reduce the image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the required dependencies with more verbosity for troubleshooting
RUN npm install --verbose

# Copy the entire project into the container
COPY . .

# Expose the port that the React app will run on (default 3000)
EXPOSE 5173

# Start the Vite development server
CMD ["npm", "run", "dev"]
