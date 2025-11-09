import { AppDataSource } from "./src/data-source";
import app from "./src/app";
import dotenv from "dotenv";
dotenv.config();

const PORT = parseInt(process.env.API_PORT || '3000');

AppDataSource.initialize()
  .then(() => {
    console.log("📦 Entidades carregadas:", AppDataSource.entityMetadatas.map(e => e.name));
    app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
  })
  .catch((error) => console.error("❌ Database connection failed:", error));
