import { AppDataSource } from "./src/data-source";
import app from "./src/app";
import dotenv from "dotenv";
import { QueryRunner } from "typeorm";
dotenv.config();

const PORT = parseInt(process.env.API_PORT || "3000");

async function ensureSchema() {
  const schemaName = "api_node";
  const queryRunner = AppDataSource.createQueryRunner();
  try {
    await queryRunner.connect();
    await queryRunner.query(`CREATE SCHEMA IF NOT EXISTS ${schemaName};`);
    console.log(`🏗️ Schema "${schemaName}" garantido com sucesso!`);
  } catch (error) {
    console.error("❌ Erro ao criar schema:", error);
  } finally {
    await queryRunner.release();
  }
}

AppDataSource.initialize()
  .then(async () => {
    console.log("📦 Entidades carregadas:", AppDataSource.entityMetadatas.map(e => e.name));
    await ensureSchema();
    app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
  })
  .catch((error) => console.error("❌ Database connection failed:", error));
