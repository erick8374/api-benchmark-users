import { Request, Response } from "express";
import { UserService } from "../services/UserService";

const service = new UserService();

export class UserController {
  async list(req: Request, res: Response) {
    const users = await service.findAll();
    return res.json(users);
  }

  async create(req: Request, res: Response) {
    const userToCreate = req.body;
    const user = await service.create(userToCreate);
    return res.status(201).json(user);
  }

  async getById(req: Request, res: Response) {
    const id = parseInt(req.params.id);
    const user = await service.findById(id);
    return res.json(user);
  }
  async update(req: Request, res: Response) {
    const id = parseInt(req.params.id);
    const userToUpdate = req.body;

    const updatedUser = await service.update(id, userToUpdate);
      if (!updatedUser) {
        return res.status(404).send('User not found');
      } else {
        return res.status(200).json(updatedUser);
      }  
  }
  async delete (req: Request, res: Response) {
      const id = parseInt(req.params.id);
      const success = await service.delete(id);
      if (!success) {
        return res.status(404).send('User not found');
      } else {
        return res.status(204).send();
      }
  };
}
