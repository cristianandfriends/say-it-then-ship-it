import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

const materials = defineCollection({
  loader: glob({
    base: "..",
    pattern: [
      "lab/**/*.md",
      ".github/agents/**/*.md",
      ".github/instructions/**/*.md",
      ".github/skills/**/*.md",
      ".agents/skills/**/*.md",
      ".opencode/**/*.md",
      "AGENTS.md",
      ".github/copilot-instructions.md",
    ],
    generateId: ({ entry }) => entry.replace(/\.md$/, ""),
  }),
  schema: z.object({
    title: z.string().optional(),
    name: z.string().optional(),
    description: z.string().optional(),
    order: z.number().default(100),
  }),
});

export const collections = { materials };
