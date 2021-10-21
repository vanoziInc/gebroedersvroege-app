# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:16-alpine

WORKDIR /app

COPY package.json /app/

RUN npm install

COPY ./ /app/

ARG FRONTEND_ENV=production

ENV NUXT_APP_ENV=${FRONTEND_ENV}

# Un-comment the next line to enable tests after implementing them
# RUN npm run test

RUN npm run build

ENV HOST 0.0.0.0

EXPOSE 3000

CMD ["npm", "run", "start"]