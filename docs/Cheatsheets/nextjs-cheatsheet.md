# Next.js App Router Cheatsheet

A modern master reference for Next.js (version 13, 14, and 15+) using the **App Router**, React Server Components (RSC), data fetching models, and optimized deployment architectures.

---

## 1. Directory Structure (App Router)

The App Router works via file-system-based routing rooted inside the `app/` folder.

```text
app/
├── layout.tsx         # Root layout (required, holds html & body)
├── page.tsx           # Home page route (/)
├── loading.tsx        # Suspense fallback wrapper for page load
├── error.tsx          # Error boundary wrapper for route segment
├── not-found.tsx      # Custom 404 handler
├── about/
│   └── page.tsx       # Sub-route (/about)
├── blog/
│   ├── [slug]/        # Dynamic path segment
│   │   └── page.tsx   # Individual blog post route (/blog/hello-world)
│   └── page.tsx       # Blog list route (/blog)
└── api/
    └── route.ts       # Backend route handler (/api)
```

---

## 2. Server Components vs. Client Components

In the App Router, components are **React Server Components (RSC)** by default unless prefixed with `"use client"`.

| Feature | React Server Component (RSC) | Client Component |
| :--- | :--- | :--- |
| **Default** | Yes | No (requires `"use client"` at top) |
| **Execution** | Server-only (HTML rendered & streamed) | Pre-rendered on server, hydrated on client |
| **Access to Hooks** | No (no `useState`, `useEffect`, etc.) | Yes (can use React state & effects) |
| **Direct DB queries** | Yes | No |
| **Browser API access** | No (no `window`, `document`, etc.) | Yes |
| **Bundle Size Impact** | Zero (only the final markup is sent) | Includes bundle scripts for hydration |

### Mixing Server and Client Components
- Keep Client Components at the leaves of your component tree.
- Pass Server Components as children to Client Components rather than importing them directly.
  ```tsx
  // GOOD:
  import ClientWrapper from "./ClientWrapper";
  import ServerChild from "./ServerChild";

  export default function Parent() {
    return (
      <ClientWrapper>
        <ServerChild />
      </ClientWrapper>
    );
  }
  ```

---

## 3. Data Fetching & Caching

Data fetching in Next.js builds on the native Web `fetch` API, providing native memoization, cache control, and revalidation.

### Server-Side Data Fetching (Static / SSR)
```tsx
// This fetch runs on the server inside a Server Component
async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  if (!res.ok) throw new Error('Failed to fetch posts');
  return res.json();
}

export default async function Blog() {
  const posts = await getPosts();
  return (
    <ul>
      {posts.map((post: any) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Fetch Strategies & Configurations

```tsx
// 1. Force Cache (Static Site Generation - SSG)
fetch('https://api.example.com', { cache: 'force-cache' });

// 2. Bypass Cache (Server-Side Rendering - SSR)
fetch('https://api.example.com', { cache: 'no-store' });

// 3. Incremental Static Regeneration (ISR)
fetch('https://api.example.com', { next: { revalidate: 3600 } }); // revalidate hourly
```

### Segment Route Parameters (RSC Config)
Place these variable definitions directly at the top of any route file (`page.tsx`, `layout.tsx` or `route.ts`) to configure behavior:
```typescript
export const dynamic = 'force-dynamic'; // Force SSR
export const revalidate = 60;           // Revalidate page every 60 seconds
export const fetchCache = 'force-cache';
```

---

## 4. Routing & Navigation

### File-System Routes

- **Dynamic Segments:** `app/blog/[slug]/page.tsx` resolves to `/blog/some-slug`.
  - Inside `page.tsx`, parameters are accessed via `params.slug` (in async params context).
- **Catch-All Segments:** `app/shop/[...slug]/page.tsx` resolves to `/shop/clothes`, `/shop/clothes/shirts`.
- **Optional Catch-All:** `app/shop/[[...slug]]/page.tsx` also resolves to `/shop`.

### Client-Side Navigation
```tsx
import Link from 'next/link';

export default function Home() {
  return (
    <Link href="/about" prefetch={true}>
      About Page
    </Link>
  );
}
```

### Imperative Navigation (Client Hooks)
```tsx
"use client";

import { useRouter, usePathname, useSearchParams } from 'next/navigation';

export default function SearchForm() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const handleSearch = (term: string) => {
    router.push(`${pathname}?q=${term}`);
  };

  return <button onClick={() => handleSearch('react')}>Search</button>;
}
```

---

## 5. API Routes (Route Handlers)

Create custom request handlers for HTTP requests using the `route.ts` file name inside the API folder.

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  return NextResponse.json({ message: `Fetching user ${id}` });
}

export async function POST(request: Request) {
  const body = await request.json();
  // Perform database insert here
  return NextResponse.json({ success: true, data: body }, { status: 201 });
}
```

---

## 6. Metadata API

Optimize SEO by defining static or dynamic metadata headers inside server layouts or pages.

### Static Metadata
```typescript
// app/about/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us | Enterprise Solutions',
  description: 'Learn more about our advanced tech stack and architecture.',
};
```

### Dynamic Metadata
```typescript
// app/blog/[slug]/page.tsx
import { Metadata } from 'next';

interface Props {
  params: { slug: string };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.slug);
  return {
    title: `${product.title} - Company Store`,
    description: product.summary,
  };
}
```
