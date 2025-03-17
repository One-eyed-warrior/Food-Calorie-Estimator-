# Dockerfile
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first (for better caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application files
COPY . .

# Build the app
RUN npm run build

# Use a lightweight web server to serve the built files
FROM node:18-alpine AS runtime
WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built files from the previous stage
COPY --from=build /app/dist /app/dist

# Expose port 3000
EXPOSE 3000

# Start the server
CMD ["serve", "-s", "dist", "-l", "3000"]