import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import remarkMermaid from "./remark-mermaid.mjs";
import { base, site } from "./site.config.mjs";

export default defineConfig({
  site,
  base,
  trailingSlash: "always",
  markdown: {
    processor: unified({ remarkPlugins: [remarkMermaid], smartypants: false }),
    shikiConfig: {
      theme: "github-dark",
      wrap: false,
    },
  },
});
