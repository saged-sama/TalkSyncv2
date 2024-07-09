FROM node:22-alpine3.20

WORKDIR /frontend

COPY . .

RUN npm install

ENV PUBLIC_API_ROOT="http://localhost:8000/api/v1"
RUN npm run build

EXPOSE 3000

CMD ["node", "build", "--", "--host", "0.0.0.0"]