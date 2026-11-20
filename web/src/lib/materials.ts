import { getCollection, type CollectionEntry } from "astro:content";
import { repositoryUrl, withBase } from "../../site.config.mjs";
import { materialRoute } from "../../material-paths.mjs";

export function materialInfo(entry: CollectionEntry<"materials">) {
  const sourcePath = `${entry.id}.md`;
  const route = materialRoute(sourcePath);
  const filename = entry.id.slice(entry.id.lastIndexOf("/") + 1);

  return {
    title: entry.data.title ?? entry.data.name ?? filename,
    description: entry.data.description,
    level: entry.data.level,
    sourcePath,
    href: withBase(`files/${route.split("/").map(encodeURIComponent).join("/")}/`),
    route,
    sourceUrl: `${repositoryUrl}/blob/HEAD/${sourcePath.split("/").map(encodeURIComponent).join("/")}`,
  };
}

export async function getMaterials() {
  const entries = await getCollection("materials");
  return entries.sort(
    (a, b) => a.data.order - b.data.order || a.id.localeCompare(b.id),
  );
}
