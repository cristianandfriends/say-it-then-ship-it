import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";
import { materialPatterns } from "../material-paths.mjs";

const materials = defineCollection({
  loader: glob({
    base: "..",
    pattern: materialPatterns,
    generateId: ({ entry }) => entry.replace(/\.md$/, ""),
  }),
  schema: z.object({
    title: z.string().optional(),
    name: z.string().optional(),
    description: z.string().optional(),
    order: z.number().default(100),
    level: z.number().int().min(0).optional(),
  }),
});

export const collections = { materials };
