FROM nginx:alpine

# Copy static files to Nginx web root
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
