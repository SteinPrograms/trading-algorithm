# Using python latest docker image
FROM node
# Defining the working directory
WORKDIR /usr/src

# Adding files
ADD . .

# Installing dependencies 
RUN npm i
RUN npm run build

# Finally running the script
CMD [ "npm", "run" ,"start" ]