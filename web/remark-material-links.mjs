import { existsSync, statSync } from "node:fs";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { visit } from "unist-util-visit";
import { isMaterialPath, materialRoute } from "./material-paths.mjs";
import { repositoryUrl, withBase } from "./site.config.mjs";

const root = fileURLToPath(new URL("../", import.meta.url));

export function resolveMaterialLink(url, sourceFile) {
  if (/^(?:[a-z][a-z\d+.-]*:|\/|#)/i.test(url) || url === "") return url;

  const [, pathname, suffix = ""] = url.match(/^([^?#]*)(.*)$/);
  if (!pathname) return url;

  const target = resolve(dirname(sourceFile), decodeURIComponent(pathname));
  const relativePath = relative(root, target);
  if (isAbsolute(relativePath) || relativePath === ".." || relativePath.startsWith(`..${sep}`)) {
    throw new Error(`Local link escapes the repository: ${url}`);
  }
  if (!existsSync(target)) {
    throw new Error(`Local link has no target: ${url} (from ${relative(root, sourceFile)})`);
  }

  const sourcePath = relativePath.split(sep).join("/");
  if (isMaterialPath(sourcePath)) {
    const route = materialRoute(sourcePath).split("/").map(encodeURIComponent).join("/");
    return `${withBase(`files/${route}/`)}${suffix}`;
  }

  const kind = statSync(target).isDirectory() ? "tree" : "blob";
  const encoded = sourcePath.split("/").map(encodeURIComponent).join("/");
  return `${repositoryUrl}/${kind}/HEAD/${encoded}${suffix}`;
}

export default function remarkMaterialLinks() {
  return (tree, file) => {
    visit(tree, (node) => {
      if (node.type !== "link" && node.type !== "definition") return;
      try {
        node.url = resolveMaterialLink(node.url, file.path);
      } catch (error) {
        file.fail(error instanceof Error ? error.message : String(error), node);
      }
    });
  };
}
