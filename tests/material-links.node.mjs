import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { resolveMaterialLink } from "../web/remark-material-links.mjs";
import { repositoryUrl, withBase } from "../web/site.config.mjs";

const source = fileURLToPath(new URL("../lab/start-here.md", import.meta.url));

test("resolves source-relative Markdown links and preserves fragments", () => {
  assert.equal(
    resolveMaterialLink("two-agents.md#keep-the-loop-short", source),
    withBase("files/lab/two-agents/#keep-the-loop-short"),
  );
  assert.equal(
    resolveMaterialLink("../.agents/skills/bootstrap-lab/SKILL.md", source),
    withBase("files/agents/skills/bootstrap-lab/SKILL/"),
  );
});

test("links source code to GitHub without routing it through Markdown", () => {
  assert.equal(
    resolveMaterialLink("../web/astro.config.mjs", source),
    `${repositoryUrl}/blob/HEAD/web/astro.config.mjs`,
  );
});

test("preserves external links and document anchors", () => {
  for (const url of ["https://example.com/doc.md#part", "#evidence", "/site-path/", "mailto:teacher@example.com"]) {
    assert.equal(resolveMaterialLink(url, source), url);
  }
});

test("rejects missing local files and paths outside the repository", () => {
  assert.throws(() => resolveMaterialLink("missing-material.md", source), /has no target/);
  assert.throws(() => resolveMaterialLink("../../outside.md", source), /escapes the repository/);
});
