import swaggerJsDoc from "swagger-jsdoc";

/**
 * @swagger
 * components:
 *   schemas:
 *     User:
 *       type: object
 *       required:
 *         - name
 *         - email
 *         - username
 *       properties:
 *         id:
 *           type: integer
 *           description: ID do usuário
 *         name:
 *           type: string
 *           description: Nome do usuário
 *         email:
 *           type: string
 *           description: Email do usuário
 *         username:
 *           type: string
 *           description: Apelido do usuário
 *         created_at:
 *           type: string
 *           format: date-time
 *           description: Data de criação do usuário
 *         updated_at:
 *           type: string
 *           format: date-time
 *           description: Data de atualização do usuário
 *       example:
 *         id: 1
 *         name: João Silva
 *         email: joao@example.com
 *         username: joao_silva
 *         created_at: "2025-01-01T12:00:00.000Z"
 *         updated_at: "2025-01-10T14:30:00.000Z"
 *
 *     UserCreate:
 *       type: object
 *       required:
 *         - name
 *         - email
 *         - username
 *         - password
 *       properties:
 *         name:
 *           type: string
 *           description: Nome do usuário
 *         email:
 *           type: string
 *           description: Email do usuário
 *         username:
 *           type: string
 *           description: Apelido do usuário
 *         password:
 *           type: string
 *           description: Senha do usuário
 *       example:
 *         name: Maria Souza
 *         email: maria@example.com
 *         username: maria_souza
 *         password: "minhasenha123"
 *
 *     UserUpdate:
 *       type: object
 *       properties:
 *         name:
 *           type: string
 *           description: Nome do usuário
 *         email:
 *           type: string
 *           description: Email do usuário
 *         username:
 *           type: string
 *           description: Apelido do usuário
 *         password:
 *           type: string
 *           description: Senha do usuário
 *       example:
 *         name: Maria Souza Atualizada
 *         email: maria.atualizada@example.com
 *         username: maria_souza
 *         password: "novaSenha456"
 *
 * @swagger
 * tags:
 *   name: Users
 *   description: Endpoints de usuários
 */

const swaggerSpec = swaggerJsDoc({
  definition: {
    openapi: "3.0.0",
    info: {
      title: "User API Node + Express",
      version: "1.0.0",
      description: "CRUD de Usuários",
    },
  },
  apis: [
    `${__dirname}/routes/*.js`,
    `${__dirname}/routes/*.ts`,
    `${__dirname}/swagger.js`,
    `${__dirname}/swagger.ts`,
  ],
});

export default swaggerSpec;
