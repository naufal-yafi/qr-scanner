import express from "express";
import {
  getAll,
  getProductByBarcode,
} from "../controllers/ProductController.js";

const router = express.Router();

router.get("/", getAll);
router.get("/product", getAll);
router.get("/product/:barcode", getProductByBarcode);

export default router;
