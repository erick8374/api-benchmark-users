import express from "express";
import userRoutes from "./routes/userRoute";
// import cors from "cors";

const app = express();

app.use(express.json());
// app.use(cors())
app.use("/users", userRoutes);

export default app;
