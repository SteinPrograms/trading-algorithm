FROM node

WORKDIR /usr/src/
# Install dependencies based on the preferred package manager
COPY . .
RUN npm i
RUN npm run build
ENV NODE_ENV production
EXPOSE 3000
ENV PORT 3000
CMD ["npm", "start"]