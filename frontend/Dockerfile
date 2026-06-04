# frontend/Dockerfile

# Stage 1: Build the React application
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
# Copy the built Vite assets to Nginx's web folder
COPY --from=build /app/dist /usr/share/nginx/html
# Expose port 80 for the Nginx web server inside the container
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]