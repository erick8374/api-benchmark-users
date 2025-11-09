import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn } from "typeorm";

@Entity("users")
export class User {
  @PrimaryGeneratedColumn("increment")
  id?: number;

  @Column()
  name?: string;

  @Column({ unique: true })
  email?: string;

  @Column({ unique: true })
  username?: string;

  @Column()
  passoword?: string;

  @CreateDateColumn()
  created_at?: Date;

  @UpdateDateColumn()
  updated_at?: Date;
}
