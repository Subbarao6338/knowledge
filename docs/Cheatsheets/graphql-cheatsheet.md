---
layout: default
title: "GraphQL Reference Cheatsheet"
---

# GraphQL Cheatsheet

A developer reference guide for GraphQL Schema Definition Language (SDL), query syntax, mutations, subscriptions, fragments, and client-side integration models.

---

## 1. Schema Definition Language (SDL)

GraphQL uses a strongly typed schema to define what operations are allowed.

```graphql
# Custom Type definitions
type User {
  id: ID!
  username: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String
  author: User!
  likes: Int!
}

# The root Query type definition
type Query {
  users: [User!]!
  user(id: ID!): User
  posts(limit: Int): [Post!]!
}

# The root Mutation type definition
type Mutation {
  createUser(username: String!, email: String!): User!
  createPost(title: String!, content: String, authorId: ID!): Post!
}

# The root Subscription type definition (real-time updates)
type Subscription {
  postAdded: Post!
}
```

---

## 2. GraphQL Queries

Queries are used by clients to fetch specific fields from the server.

### Basic Query
```graphql
query GetUsers {
  users {
    id
    username
    email
  }
}
```

### Query with Variables & Directives
```graphql
query GetUserPosts($userId: ID!, $includeLikes: Boolean!) {
  user(id: $userId) {
    username
    posts {
      title
      likes @include(if: $includeLikes)
    }
  }
}
```

### Variables JSON Payload
```json
{
  "userId": "usr_48293",
  "includeLikes": true
}
```

---

## 3. GraphQL Mutations

Mutations are used by clients to modify data on the server (Create, Update, Delete).

```graphql
mutation NewUser($username: String!, $email: String!) {
  createUser(username: $username, email: $email) {
    id
    username
    email
  }
}
```

---

## 4. Fragments & Inline Fragments

Fragments allow reusing sets of fields across multiple queries.

```graphql
fragment PostFields on Post {
  id
  title
  content
  likes
}

query FetchFeed {
  posts {
    ...PostFields
    author {
      username
    }
  }
}
```

### Inline Fragments (for Unions / Interfaces)
```graphql
union SearchResult = User | Post

query SearchAll($text: String!) {
  search(q: $text) {
    ... on User {
      username
    }
    ... on Post {
      title
      content
    }
  }
}
```

---

## 5. Apollo / GraphQL Client Integration

Example using Apollo Client in modern React/TypeScript:

```typescript
import { ApolloClient, InMemoryCache, gql, useQuery } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://api.example.com/graphql',
  cache: new InMemoryCache(),
});

const GET_POSTS = gql`
  query GetPosts {
    posts {
      id
      title
    }
  }
`;

function PostsList() {
  const { loading, error, data } = useQuery(GET_POSTS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error : {error.message}</p>;

  return (
    <ul>
      {data.posts.map((post: any) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```
