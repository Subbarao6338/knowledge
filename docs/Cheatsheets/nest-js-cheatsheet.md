---
layout: default
title: "NestJS Cheatsheet"
---

# NestJS Cheatsheet

NestJS is a progressive Node.js framework for building efficient, reliable, and scalable server-side applications, heavily inspired by Angular's architecture.

---

## 1. Core Architecture Patterns

Every NestJS application contains at least three core elements:
1. **Controllers:** Handle incoming HTTP requests and map them to service operations.
2. **Providers / Services:** Contain the main business and database query logic.
3. **Modules:** Organize application features into distinct encapsulation packages.

```
Incoming Request ──> Controller ──> Service ──> Database / Orm
```

---

## 2. Controllers & Routing Decorators

### Example: Users Controller (`users.controller.ts`)
```typescript
import { Controller, Get, Post, Body, Param, Query, Put, Delete, HttpCode, HttpStatus, UseGuards } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UsersService } from './users.service';
import { User } from './interfaces/user.interface';
import { AuthGuard } from '../auth/auth.guard';

@Controller('users') // Base route prefix: http://localhost:3000/users
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get() // GET /users?role=admin
  async findAll(@Query('role') role?: string): Promise<User[]> {
    return this.usersService.findAll(role);
  }

  @Get(':id') // GET /users/42
  async findOne(@Param('id') id: string): Promise<User> {
    return this.usersService.findOne(id);
  }

  @Post() // POST /users
  @HttpCode(HttpStatus.CREATED) // Explicit status returns
  @UseGuards(AuthGuard) // Protect endpoint with authentication guard
  async create(@Body() createUserDto: CreateUserDto): Promise<User> {
    return this.usersService.create(createUserDto);
  }

  @Delete(':id') // DELETE /users/42
  @HttpCode(HttpStatus.NO_CONTENT)
  async remove(@Param('id') id: string): Promise<void> {
    await this.usersService.delete(id);
  }
}
```

---

## 3. Providers, Services & Dependency Injection

Providers are decorated with `@Injectable()`, allowing Nest to instantiate them and inject them into controllers or other services.

### Example Service (`users.service.ts`)
```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { User } from './interfaces/user.interface';
import { CreateUserDto } from './dto/create-user.dto';

@Injectable()
export class UsersService {
  private readonly users: User[] = [];

  async create(dto: CreateUserDto): Promise<User> {
    const newUser = { id: Date.now().toString(), ...dto };
    this.users.push(newUser);
    return newUser;
  }

  async findAll(role?: string): Promise<User[]> {
    if (role) {
      return this.users.filter(user => user.role === role);
    }
    return this.users;
  }

  async findOne(id: string): Promise<User> {
    const user = this.users.find(u => u.id === id);
    if (!user) {
      // Automatic conversion to HTTP 404 response
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }
}
```

---

## 4. Feature Modules Configuration

Modules group together related components. Each file in the module must be declared in imports or providers.

### Example Module (`users.module.ts`)
```typescript
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService] // Allows other modules to use UsersService on import
})
export class UsersModule {}
```

---

## 5. Request Validation & Data Transfer Objects (DTOs)

To validate input, NestJS utilizes decorators from the `class-validator` package matched with the global `ValidationPipe`.

### Enabling Validation Globals (`main.ts`)
```typescript
import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Enable automatic validation globally
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,         // Strip away properties not defined in the DTO schema
    forbidNonWhitelisted: true, // Fail request if extra properties are sent
    transform: true,         // Auto-cast request parameters to actual DTO types
  }));

  await app.listen(3000);
}
bootstrap();
```

### DTO Definition Schema (`dto/create-user.dto.ts`)
```typescript
import { IsString, IsEmail, IsEnum, IsInt, Min, Max, IsNotEmpty } from 'class-validator';

export enum UserRole {
  USER = 'user',
  MODERATOR = 'moderator',
  ADMIN = 'admin'
}

export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  username: string;

  @IsEmail()
  email: string;

  @IsEnum(UserRole)
  role: UserRole;

  @IsInt()
  @Min(18)
  @Max(120)
  age: number;
}
```

---

## 6. Guards, Interceptors & Middleware

NestJS applications process pipelines sequentially:
```
Middleware ──> Guards ──> Interceptors ──> Pipes ──> Controller Route Handler ──> Interceptors (Response)
```

### 1. Guards (Authentication & Authorization)
```typescript
import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/core';
import { Observable } from 'rxjs';

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = request.headers.authorization?.split(' ')[1];

    if (!token || token !== 'valid-session-token') {
      throw new UnauthorizedException('Access denied. Invalid session token.');
    }

    return true;
  }
}
```

### 2. Interceptors (Logging, Formatting)
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/core';
import { Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';

@Injectable()
export class TransformResponseInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      // Wrap all responses in a standard JSON envelope
      map(data => ({
        success: true,
        statusCode: context.switchToHttp().getResponse().statusCode,
        data: data
      }))
    );
  }
}
```
