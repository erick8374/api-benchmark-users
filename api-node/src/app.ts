import express from "express";
import userRoutes from "./routes/userRoute";
import swaggerUi from "swagger-ui-express"
import swaggerSpec from "./swagger";

const app = express();

app.use(express.json());
app.use("/users", userRoutes);
app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

export default app;

