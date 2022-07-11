FROM node
WORKDIR /usr/src/app

# Install dependencies
COPY ./frontend/package.json .
COPY ./frontend/next.config.js .
RUN npm install

# Copy files
COPY ./frontend/components ./components
COPY ./frontend/styles ./styles
COPY ./frontend/pages ./pages
COPY ./frontend/public ./public

RUN npm install @prisma/client
RUN npx prisma generate

# Run dev server
CMD [ "npm", "run", "dev" ]