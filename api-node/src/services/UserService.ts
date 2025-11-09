import { AppDataSource } from "../data-source";
import { User } from "../entities/User";

export class UserService {
  private userRepository = AppDataSource.getRepository(User);

  async findAll() {
    return this.userRepository.find();
  }
  async findById(id: number) {
    const user = this.userRepository.findOneBy({id});
    return user || undefined
  }
  async create(newUser: Partial<Omit<User, 'id'>>) {
    const user = this.userRepository.create(newUser);
    return this.userRepository.save(user);
  }
  async update(id: number, user: Partial<Omit<User, 'id'>>){
        const userToUpdate = await this.findById(id)

        if (!userToUpdate) {
            return undefined
        }
        this.userRepository.merge(userToUpdate, user);
        return await this.userRepository.save(userToUpdate);  
  }
  async delete(id: number) {
    const result = await this.userRepository.delete(id);
    return result?.affected ? result.affected > 0 : false;
  }
}
