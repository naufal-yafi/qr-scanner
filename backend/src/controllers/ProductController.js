import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const getAll = async (req, res) => {
  try {
    const response = await prisma.product.findMany();

    res.status(200).json(response);
  } catch (error) {
    req.status(500).json(error.message);
  }
};

export const getProductByBarcode = async (req, res) => {
  try {
    const { barcode } = req.params;
    const response = await prisma.product.findUnique({
      where: {
        barcode: barcode,
      },
    });

    response
      ? res
          .status(200)
          .json({ status: 200, message: "Successfully", data: response })
      : res
          .status(200)
          .json({ status: 404, message: "Product not found", data: null });
  } catch (error) {
    res.status(500).json(error.message);
  }
};
