import express from "express";
import cors from "cors";
import ProductRoute from "./routes/ProductRoute.js";
import LoggingMiddleware from "./middleware/LoggingMiddleware.js";

const app = express();

app.use(cors());
app.use(LoggingMiddleware);
app.use(ProductRoute);

app.listen(2000, () => console.log("Server running on http://localhost:2000/"));
