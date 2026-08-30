---
layout: default
title: "GraphQL & gRPC Architecture Cheatsheet"
---

# GraphQL & gRPC Architecture Cheatsheet

A comparative and technical cheat sheet covering API protocols, GraphQL schemas, resolvers, DataLoader batching, gRPC Protobuf definitions, HTTP/2 multiplexing, streaming RPCs, and performance benchmarks.

---

## 1. Protocol Comparison Matrix

| Metric / Feature | REST (JSON) | GraphQL | gRPC |
| :--- | :--- | :--- | :--- |
| **Transport Layer** | HTTP/1.1 or HTTP/2 | HTTP/1.1 or HTTP/2 | HTTP/2 Exclusive (Multiplexed) |
| **Payload Format** | JSON (Text) | JSON (Text) | Protocol Buffers (Binary) |
| **Schema Definition** | OpenAPI / Swagger (Optional)| GraphQL SDL (Strict) | `.proto` Files (Strict Binary Schema) |
| **Over/Under-Fetching**| Common issue | Eliminated (Client specifies fields) | Eliminated (Fixed proto contract) |
| **Streaming Support** | SSE / WebSockets | Subscriptions (WebSockets/SSE) | Native Server, Client, & Bi-Directional |
| **Performance Speed** | Standard | Medium (Query parsing overhead)| Extremely Fast (Binary serialization)|

---

## 2. GraphQL Schema & DataLoader N+1 Prevention

### GraphQL Schema SDL

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  user(id: ID!): User
  feed(limit: Int = 10): [Post!]!
}

type Mutation {
  createPost(title: String!, content: String!, authorId: ID!): Post!
}
```

### Preventing N+1 Resolver Queries with DataLoader (Node.js/TypeScript)

```typescript
import DataLoader from 'dataloader';
import { db } from './database';

// Batch function receives array of user IDs and fetches them in 1 SQL query
const userBatchLoader = new DataLoader<string, User>(async (userIds: readonly string[]) => {
  const users = await db.query(
    'SELECT * FROM users WHERE id IN ($1)',
    [userIds]
  );

  // Map users back to match requested order
  const userMap = new Map(users.map(u => [u.id, u]));
  return userIds.map(id => userMap.get(id) || new Error(`User ${id} not found`));
});

// GraphQL Resolver
export const resolvers = {
  Post: {
    author: (post: Post) => userBatchLoader.load(post.authorId),
  },
};
```

---

## 3. gRPC Protobuf Definition & Bi-Directional Streaming

### Protobuf v3 Service Definition (`user_service.proto`)

```protobuf
syntax = "proto3";

package users;

option go_package = "github.com/example/users/v1;usersv1";

service UserService {
  // Unary RPC
  rpc GetUser (GetUserRequest) returns (UserResponse);

  // Bi-Directional Streaming RPC
  rpc LiveUserChat (stream ChatMessage) returns (stream ChatMessage);
}

message GetUserRequest {
  string user_id = 1;
}

message UserResponse {
  string id = 1;
  string name = 2;
  string email = 3;
  int64 created_at_epoch = 4;
}

message ChatMessage {
  string sender_id = 1;
  string text_payload = 2;
  int64 timestamp = 3;
}
```

---

## Best Practices & Production Standards

1. **GraphQL Query Depth Limits**: Always install query depth limiters and complexity analyzers (e.g. `graphql-depth-limit`) to prevent malicious nested queries from crashing your database.
2. **gRPC HTTP/2 Load Balancing**: Traditional L4 load balancers fail with gRPC due to persistent long-lived HTTP/2 TCP streams. Use L7 proxy load balancing (e.g. Envoy, Traefik).
3. **Protobuf Field Numbers**: Never renumber field tags in `.proto` files once published. Deprecate old fields using `reserved` keywords.

---

## Common Mistakes & Troubleshooting

1. **GraphQL N+1 Query Antipattern**: Resolving nested relations without batching results in $1 + N$ SQL queries. Always wrap nested field resolvers in DataLoader.
2. **gRPC Web Proxy Requirement**: Browsers cannot initiate direct raw gRPC HTTP/2 connections. Use `grpc-web` proxy adapters for frontend web integration.

---

## Core Interview Questions

1. **Q: How does gRPC achieve faster serialization and lower network bandwidth compared to REST JSON?**
   - **A**: gRPC uses Protocol Buffers, a compact binary format that omits field name strings from network payloads, encoding values using varints and field tags instead of verbose UTF-8 JSON text.

---

## Related Cheatsheets & References

- [REST API Cheatsheet](rest-api-cheatsheet.md)
- [Microservices Architecture Cheatsheet](microservices-cheatsheet.md)
- [Computer Networking Cheatsheet](networking-cheatsheet.md)
- [TypeScript Cheatsheet](typescript-cheatsheet.md)
