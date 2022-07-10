import express, { Application, Request, Response } from 'express';
import { PrismaClient } from '@prisma/client'

const app: Application = express();
const prisma = new PrismaClient()

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const port: number = 3000;

 // testing route
app.get("/", (_req, res: Response) => {
    res.send(`Server is running on port: ${port}`);
});

// Getting todos route
app.get('/api/todos', async (req: Request, res: Response) => {
    try {
        const allUsers = await prisma.positions.findMany();
        return res.json({
            success: true,
            data: allUsers
        });
    } catch (error) {
        return res.json({
            success: false,
            message: error
        });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
})