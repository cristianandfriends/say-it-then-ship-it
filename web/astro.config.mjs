import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import remarkMermaid from "./remark-mermaid.mjs";
import remarkMaterialLinks from "./remark-material-links.mjs";
import { base, site, withBase } from "./site.config.mjs";

export default defineConfig({
  site,
  base,
  trailingSlash: "always",
  redirects: {
    "/files/lab/level-4-review/": withBase("files/lab/level-5-review/"),
    "/files/lab/level-5-context/": withBase("files/lab/level-6-context/"),
    "/files/lab/level-6-tools/": withBase("files/lab/level-7-tools/"),
  },
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMermaid, remarkMaterialLinks],
      smartypants: false,
    }),
    shikiConfig: {
      theme: "github-dark",
      wrap: false,
    },
  },
});
