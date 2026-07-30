---
layout: default
title: "Astro Cheatsheet"
---

# Astro Cheatsheet

A master reference for **Astro**, the modern web framework focused on content-driven sites, fast static generation, and Islands Architecture.

---

## 1. Directory Layout & Architecture

Astro enforces file-based routing and a separation between public static assets and server components.

```text
src/
├── components/        # Layout and reusable UI components (.astro, .tsx, .vue)
├── layouts/           # HTML skeleton templates
├── pages/             # File-system router pages (/index.astro, /blog/index.astro)
│   ├── index.astro
│   └── blog/
│       └── [slug].astro # Dynamic routing template
├── content/           # Content Collections (Markdown/MDX schema databases)
│   ├── config.ts
│   └── posts/         # Markdown post files
└── env.d.ts           # Types definition
public/                # Static assets served at root (images, robots.txt, etc.)
astro.config.mjs       # Astro configuration & integration plugins
```

---

## 2. Astro Component Syntax (`.astro`)

Astro components contain a **Component Script** (frontmatter fenced with `---`) and a **Component Template** (JSX-like HTML skeleton underneath).

```astro
---
// src/components/Card.astro
// Frontmatter executes exclusively on the server at compile/request time.
import Button from './Button.astro';

interface Props {
  title: string;
  body: string;
  href: string;
  isNew?: boolean;
}

const { title, body, href, isNew = false } = Astro.props;
---

<li class="link-card border border-slate-200 p-4 rounded-lg flex flex-col gap-2">
  <a href={href} class="text-indigo-600 font-semibold hover:underline">
    {title} {isNew && <span class="bg-red-100 text-red-700 px-1.5 py-0.5 rounded text-xs font-bold">NEW</span>}
  </a>
  <p class="text-slate-600 text-sm">{body}</p>
  <slot /> <!-- Allows dynamic nested HTML injection -->
</li>

<style>
  /* Astro styles are strictly scoped to this component template by default! */
  .link-card {
    transition: transform 0.2s ease;
  }
  .link-card:hover {
    transform: translateY(-2px);
  }
</style>
```

---

## 3. Client Directives (Islands Architecture)

Astro is **zero-JS by default**. Interactive components built with UI frameworks (React, Vue, Svelte, Preact) must be explicitly hydrated using **Client Directives**.

| Directive | Description | Example |
| :--- | :--- | :--- |
| **`client:load`** | Hydrates immediately on page load | `<Counter client:load />` |
| **`client:idle`** | Hydrates once main thread is idle | `<Newsletter client:idle />` |
| **`client:visible`** | Hydrates once component enters viewport | `<Comments client:visible />` |
| **`client:media`** | Hydrates matching viewport media query | `<Sidebar client:media="(max-width: 50em)" />` |
| **`client:only`** | Skips server pre-rendering, hydrates only on client | `<Dashboard client:only="react" />` |

---

## 4. Content Collections

Content Collections are the safest, most performant way to load local Markdown/MDX content with complete TypeScript validation.

### Defining Schema Database (`src/content/config.ts`)
```typescript
import { defineCollection, z } from 'astro:content';

const postsCollection = defineCollection({
  type: 'content', // 'content' (Markdown) or 'data' (JSON/YAML)
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string(),
    author: z.string(),
    tags: z.array(z.string()),
    draft: z.boolean().default(false),
  }),
});

export const collections = {
  'posts': postsCollection,
};
```

### Fetching & Querying Collections inside Astro Page
```astro
---
// src/pages/blog.astro
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';

// Fetch non-draft posts and sort by publication date
const allPosts = await getCollection('posts', ({ data }) => !data.draft);
allPosts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---

<BaseLayout title="My Blog Portal">
  <h1>Blog Posts Archive</h1>
  <ul class="space-y-4">
    {allPosts.map((post) => (
      <li>
        <a href={`/blog/${post.slug}`} class="font-bold text-lg">{post.data.title}</a>
        <p class="text-sm text-gray-500">{post.data.pubDate.toDateString()}</p>
      </li>
    ))}
  </ul>
</BaseLayout>
```

---

## 5. Routing & Static vs. SSR

Configure whether routes are statically compiled (SSG - default) or dynamically compiled on the fly (SSR).

### Static Dynamic Routes Generation (`getStaticPaths`)
```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('posts');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render(); // Parse markdown to components
---

<h1>{post.data.title}</h1>
<p>Written by {post.data.author}</p>
<article class="prose">
  <Content />
</article>
```

### Activating SSR in Configuration
```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server', // 'server' for complete SSR, 'hybrid' for optional SSR
  adapter: node({
    mode: 'standalone',
  }),
});
```
